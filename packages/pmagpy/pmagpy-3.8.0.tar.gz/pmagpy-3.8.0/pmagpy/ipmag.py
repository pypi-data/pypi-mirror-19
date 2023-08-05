import pmag
import pmagplotlib
import data_model3 as data_model
from new_builder import Contribution
import validate_upload3 as val_up3
import copy
import numpy as np
import random
import matplotlib
import matplotlib.pyplot as plt
import os
import sys
import time
import re
import math
#from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
#from matplotlib.backends.backend_wx import NavigationToolbar2Wx
from matplotlib.figure import Figure
from mapping import map_magic


def igrf(input_list):
    """
    Determine Declination, Inclination, Intensity from the IGRF model.
    (http://www.ngdc.noaa.gov/IAGA/vmod/igrf.html)

    Parameters
    ----------
    input_list : list with format [Date, Altitude, Latitude, Longitude]
    Date must be in format XXXX.XXXX with years and decimals of a year (A.D.)

    Returns
    ----------
    igrf_array : array of IGRF values (0: dec; 1: inc; 2: intensity)
    """
    x,y,z,f = pmag.doigrf(input_list[3]%360.,input_list[2],input_list[1],input_list[0])
    igrf_array = pmag.cart2dir((x,y,z))
    return igrf_array


def igrf_print(igrf_array):
    """
    Print out Declination, Inclination, Intensity from an array returned from
    the igrf function.
    """

    print "Declination: %0.3f"%(igrf_array[0])
    print "Inclination: %0.3f"%(igrf_array[1])
    print "Intensity: %0.3f nT"%(igrf_array[2])


def fisher_mean(dec=None, inc=None, di_block=None):
    """
    Calculates the Fisher mean and associated parameters from either a list of
    declination values and a separate list of inclination values or from a
    di_block (a nested list a nested list of [dec,inc,1.0]). Returns a
    dictionary with the Fisher mean and statistical parameters.

    Parameters
    ----------
    dec: list of declinations (or longitudes)
    inc: list of inclinations (or latitudes)

    or

    di_block: a nested list of [dec,inc,1.0]

    A di_block can be provided instead of dec, inc lists in which case it will
    be used. Either dec, inc lists or a di_block need to passed to the function.
    """
    if di_block is None:
        di_block = make_di_block(dec,inc)
        return pmag.fisher_mean(di_block)
    else:
        return pmag.fisher_mean(di_block)


def bingham_mean(dec=None, inc=None, di_block=None):
    """
    Calculates the Bingham mean and associated parameters from either a list of
    declination values and a separate list of inclination values or from a
    di_block (a nested list a nested list of [dec,inc,1.0]). Returns a
    dictionary with the Bingham mean and statistical parameters.

    Parameters
    ----------
    dec: list of declinations
    inc: list of inclinations

    or

    di_block: a nested list of [dec,inc,1.0]

    A di_block can be provided instead of dec, inc lists in which case it will
    be used. Either dec, inc lists or a di_block need to passed to the function.
    """
    if di_block is None:
        di_block = make_di_block(dec,inc)
        return pmag.dobingham(di_block)
    else:
        return pmag.dobingham(di_block)


def kent_mean(dec=None, inc=None, di_block=None):
    """
    Calculates the Kent mean and associated parameters from either a list of
    declination values and a separate list of inclination values or from a
    di_block (a nested list a nested list of [dec,inc,1.0]). Returns a
    dictionary with the Kent mean and statistical parameters.

    Parameters
    ----------
    dec: list of declinations
    inc: list of inclinations

    or

    di_block: a nested list of [dec,inc,1.0]

    A di_block can be provided instead of dec, inc lists in which case it will
    be used. Either dec, inc lists or a di_block need to passed to the function.
    """
    if di_block is None:
        di_block = make_di_block(dec,inc)
        return pmag.dokent(di_block,len(di_block))
    else:
        return pmag.dokent(di_block,len(di_block))


def print_direction_mean(mean_dictionary):
    """
    Does a pretty job printing a Fisher mean and associated statistics for
    directional data.

    Parameters
    ----------
    mean_dictionary: output dictionary of pmag.fisher_mean
    """
    print 'Dec: ' + str(round(mean_dictionary['dec'],1)) + '  Inc: ' + str(round(mean_dictionary['inc'],1))
    print 'Number of directions in mean (n): ' + str(mean_dictionary['n'])
    print 'Angular radius of 95% confidence (a_95): ' + str(round(mean_dictionary['alpha95'],1))
    print 'Precision parameter (k) estimate: ' + str(round(mean_dictionary['k'],1))


def print_pole_mean(mean_dictionary):
    """
    Does a pretty job printing a Fisher mean and associated statistics for
    mean paleomagnetic poles.

    Parameters
    ----------
    mean_dictionary: output dictionary of pmag.fisher_mean
    """
    print 'Plon: ' + str(round(mean_dictionary['dec'],1)) + '  Plat: ' + str(round(mean_dictionary['inc'],1))
    print 'Number of directions in mean (n): ' + str(mean_dictionary['n'])
    print 'Angular radius of 95% confidence (A_95): ' + str(round(mean_dictionary['alpha95'],1))
    print 'Precision parameter (k) estimate: ' + str(round(mean_dictionary['k'],1))


def fishrot(k=20, n=100, dec=0, inc=90, di_block=True):
    """
    Generates Fisher distributed unit vectors from a specified distribution
    using the pmag.py fshdev and dodirot functions.

    Parameters
    ----------
    k : kappa precision parameter (default is 20)
    n : number of vectors to determine (default is 100)
    dec : mean declination of distribution (default is 0)
    inc : mean inclination of distribution (default is 90)
    di_block : this function returns a nested of [dec,inc,1.0] as the default
    if di_block = False it will return a list of dec and a list of inc
    """
    directions=[]
    declinations=[]
    inclinations=[]
    if di_block == True:
        for data in range(n):
            d,i=pmag.fshdev(k)
            drot,irot=pmag.dodirot(d,i,dec,inc)
            directions.append([drot,irot,1.])
        return directions
    else:
        for data in range(n):
            d,i=pmag.fshdev(k)
            drot,irot=pmag.dodirot(d,i,dec,inc)
            declinations.append(drot)
            inclinations.append(irot)
        return declinations, inclinations


def tk03(n=100,dec=0,lat=0,rev='no',G2=0,G3=0):
    """
    Generates vectors drawn from the TK03.gad model of secular
    variation (Tauxe and Kent, 2004) at given latitude and rotated
    about a vertical axis by the given declination. Return a nested list of
    of [dec,inc,intensity].

    Parameters
    ----------
    n : number of vectors to determine (default is 100)
    dec : mean declination of data set (default is 0)
    lat : latitude at which secular variation is simulated (default is 0)
    rev : if reversals are to be included this should be 'yes' (default is 'no')
    G2 : specify average g_2^0 fraction (default is 0)
    G3 : specify average g_3^0 fraction (default is 0)
    """
    tk_03_output=[]
    for k in range(n):
        gh=pmag.mktk03(8,k,G2,G3) # terms and random seed
        long=random.randint(0,360) # get a random longitude, between 0 and 359
        vec= pmag.getvec(gh,lat,long)  # send field model and lat to getvec
        vec[0]+=dec
        if vec[0]>=360.:
            vec[0]-=360.
        if k%2==0 and rev=='yes':
           vec[0]+=180.
           vec[1]=-vec[1]
        tk_03_output.append([vec[0],vec[1],vec[2]])
    return tk_03_output


def unsquish(incs,f):
    """
    This function applies an unflattening factor (f) to inclination data
    (incs) and returns 'unsquished' values.

    Parameters
    ----------
    incs : list of inclination values or a single value
    f : unflattening factor (between 0.0 and 1.0)
    """
    try:
        length = len(incs)
        incs_unsquished = []
        for n in range(0,length):
            inc_rad = np.deg2rad(incs[n]) # convert to radians
            inc_new_rad = (1./f)*np.tan(inc_rad)
            inc_new = np.rad2deg(np.arctan(inc_new_rad)) # convert back to degrees
            incs_unsquished.append(inc_new)
        return incs_unsquished
    except:
        inc_rad = np.deg2rad(incs) # convert to radians
        inc_new_rad = (1./f)*np.tan(inc_rad)
        inc_new = np.rad2deg(np.arctan(inc_new_rad)) # convert back to degrees
        return inc_new


def squish(incs,f):
    """
    This function applies an flattening factor (f) to inclination data
    (incs) and returns 'squished' values.

    Parameters
    ----------
    incs : list of inclination values or a single value
    f : flattening factor (between 0.0 and 1.0)
    """
    try:
        length = len(incs)
        incs_squished = []
        for n in range(0,length):
            inc_rad = incs[n]*np.pi/180. # convert to radians
            inc_new_rad = f*np.tan(inc_rad)
            inc_new = np.arctan(inc_new_rad)*180./np.pi # convert back to degrees
            incs_squished.append(inc_new)
        return incs_squished
    except:
        inc_rad = incs*np.pi/180. # convert to radians
        inc_new_rad = f*np.tan(inc_rad)
        inc_new = np.arctan(inc_new_rad)*180./np.pi # convert back to degrees
        return inc_new


def do_flip(dec=None, inc=None, di_block=None):
    """
    This function returns the antipode (i.e. it flips) of directions.

    The function can take dec and inc as seperate lists if they are of equal
    length and explicitly specified or are the first two arguments. It will then
    return a list of flipped decs and a list of flipped incs. If a di_block (a
    nested list of [dec,inc,1.0]) is specified then it is used and the function
    returns a di_block with the flipped directions.

    Parameters
    ----------
    dec: list of declinations
    inc: list of inclinations

    or

    di_block: a nested list of [dec,inc,1.0]

    A di_block can be provided instead of dec, inc lists in which case it will
    be used. Either dec, inc lists or a di_block need to passed to the function.
    """
    if di_block is None:
        dec_flip = []
        inc_flip = []
        for n in range(0,len(dec)):
            dec_flip.append((dec[n]-180.)%360.0)
            inc_flip.append(-inc[n])
        return dec_flip, inc_flip
    else:
        dflip=[]
        for rec in di_block:
            d, i = (rec[0]-180.)%360., -rec[1]
            dflip.append([d, i, 1.0])
        return dflip


def bootstrap_fold_test(Data,num_sims=1000,min_untilt=-10,max_untilt=120, bedding_error=0, save = False, save_folder = '.',fmt = 'svg',ninety_nine=False):
    """
    Conduct a bootstrap fold test (Tauxe and Watson, 1994)

    Three plots are generated: 1) equal area plot of uncorrected data;
    2) tilt-corrected equal area plot; 3) bootstrap results showing the trend
    of the largest eigenvalues for a selection of the pseudo-samples (red
    dashed lines), the cumulative distribution of the eigenvalue maximum (green
    line) and the confidence bounds that enclose 95% of the pseudo-sample
    maxima. If the confidence bounds enclose 100% unfolding, the data "pass"
    the fold test.

    Required Parameters
    ----------
    Data : a numpy array of directional data [dec,inc,dip_direction,dip]

    Optional Parameters (defaults are used if not specified)
    ----------
    NumSims : number of bootstrap samples (default is 1000)
    min_untilt : minimum percent untilting applied to the data (default is -10%)
    max_untilt : maximum percent untilting applied to the data (default is 120%)
    bedding_error : (circular standard deviation) for uncertainty on bedding poles
    """

    print 'doing ',num_sims,' iterations...please be patient.....'

    if bedding_error!=0:
        kappa=(81./bedding_error)**2
    else:
        kappa=0

    plt.figure(figsize=[5,5])
    plot_net(1)
    pmagplotlib.plotDI(1,Data)  # plot directions
    plt.text(-1.1,1.15,'Geographic')
    if save==True:
        plt.savefig(os.path.join(save_folder, 'eq_geo') + '.' + fmt)

    D,I=pmag.dotilt_V(Data)
    TCs=np.array([D,I]).transpose()

    plt.figure(figsize=[5,5])
    plot_net(2)
    pmagplotlib.plotDI(2,TCs)  # plot directions
    plt.text(-1.1,1.15,'Tilt-corrected')
    if save==True:
        plt.savefig(os.path.join(save_folder, 'eq_tc') + '.' + fmt)
    plt.show()

    Percs = range(min_untilt,max_untilt)
    Cdf = []
    Untilt = []
    plt.figure()

    for n in range(num_sims): # do bootstrap data sets - plot first 25 as dashed red line
            #if n%50==0:print n
            Taus=[] # set up lists for taus
            PDs=pmag.pseudo(Data)
            if kappa!=0:
                for k in range(len(PDs)):
                    d,i=pmag.fshdev(kappa)
                    dipdir,dip=pmag.dodirot(d,i,PDs[k][2],PDs[k][3])
                    PDs[k][2]=dipdir
                    PDs[k][3]=dip
            for perc in Percs:
                tilt=np.array([1.,1.,1.,0.01*perc])
                D,I=pmag.dotilt_V(PDs*tilt)
                TCs=np.array([D,I]).transpose()
                ppars=pmag.doprinc(TCs) # get principal directions
                Taus.append(ppars['tau1'])
            if n<25:plt.plot(Percs,Taus,'r--')
            Untilt.append(Percs[Taus.index(np.max(Taus))]) # tilt that gives maximum tau
            Cdf.append(float(n)/float(num_sims))
    plt.plot(Percs,Taus,'k')
    plt.xlabel('% Untilting')
    plt.ylabel('tau_1 (red), CDF (green)')
    Untilt.sort() # now for CDF of tilt of maximum tau
    plt.plot(Untilt,Cdf,'g')
    lower=int(.025*num_sims)
    upper=int(.975*num_sims)
    plt.axvline(x=Untilt[lower],ymin=0,ymax=1,linewidth=1,linestyle='--')
    plt.axvline(x=Untilt[upper],ymin=0,ymax=1,linewidth=1,linestyle='--')
    title = '%i - %i %s'%(Untilt[lower],Untilt[upper],'percent unfolding')
    if ninety_nine is True:
        print 'tightest grouping of vectors obtained at (99% confidence bounds):'
        print int(.005*num_sims), ' - ', int(.995*num_sims),'percent unfolding'
    print ""
    print 'tightest grouping of vectors obtained at (95% confidence bounds):'
    print title
    print 'range of all bootstrap samples: '
    print Untilt[0], ' - ', Untilt[-1],'percent unfolding'
    plt.title(title)
    if save == True:
        plt.savefig(os.path.join(save_folder, 'bootstrap_CDF') + '.' + fmt)
    plt.show()


def common_mean_bootstrap(Data1,Data2,NumSims=1000, save=False, save_folder = '.', fmt = 'svg',figsize=(7,2.3), x_tick_bins = 4):
    """
    Conduct a bootstrap test (Tauxe, 2010) for a common mean on two declination,
    inclination data sets

    This function modifies code from PmagPy for use calculating and plotting
    bootstrap statistics. Three plots are generated (one for x, one for y and
    one for z). If the 95 percent confidence bounds for each component overlap
    each other, the two directions are not significantly different.

    Parameters
    ----------
    Data1 : a nested list of directional data [dec,inc] (a di_block)
    Data2 : a nested list of directional data [dec,inc] (a di_block)

    Optional Parameters (defaults are used if not specified)
    ----------
    NumSims : number of bootstrap samples (default is 1000)
    save : optional save of plots (default is False)
    save_folder : path to directory where plots should be saved
    fmt : format of figures to be saved (default is 'svg')
    figsize : optionally adjust figure size (default is (7, 2.3))
    nbins : because they occasionally overlap depending on the data, this
        argument allows you adjust number of tick marks on the x axis of graphs
        (default is 4)
    """
    counter=0
    BDI1=pmag.di_boot(Data1)
    BDI2=pmag.di_boot(Data2)

    cart1= pmag.dir2cart(BDI1).transpose()
    X1,Y1,Z1=cart1[0],cart1[1],cart1[2]
    cart2= pmag.dir2cart(BDI2).transpose()
    X2,Y2,Z2=cart2[0],cart2[1],cart2[2]

    fignum = 1
    fig = plt.figure(figsize=figsize)
    fig = plt.subplot(1,3,1)

    minimum = int(0.025*len(X1))
    maximum = int(0.975*len(X1))

    X1,y=pmagplotlib.plotCDF(fignum,X1,"X component",'r',"")
    bounds1=[X1[minimum],X1[maximum]]
    pmagplotlib.plotVs(fignum,bounds1,'r','-')

    X2,y=pmagplotlib.plotCDF(fignum,X2,"X component",'b',"")
    bounds2=[X2[minimum],X2[maximum]]
    pmagplotlib.plotVs(fignum,bounds2,'b','--')
    plt.ylim(0,1)
    plt.locator_params(nbins=x_tick_bins)

    plt.subplot(1,3,2)

    Y1,y=pmagplotlib.plotCDF(fignum,Y1,"Y component",'r',"")
    bounds1=[Y1[minimum],Y1[maximum]]
    pmagplotlib.plotVs(fignum,bounds1,'r','-')

    Y2,y=pmagplotlib.plotCDF(fignum,Y2,"Y component",'b',"")
    bounds2=[Y2[minimum],Y2[maximum]]
    pmagplotlib.plotVs(fignum,bounds2,'b','--')
    plt.ylim(0,1)
    plt.locator_params(nbins=x_tick_bins)

    plt.subplot(1,3,3)

    Z1,y=pmagplotlib.plotCDF(fignum,Z1,"Z component",'r',"")
    bounds1=[Z1[minimum],Z1[maximum]]
    pmagplotlib.plotVs(fignum,bounds1,'r','-')

    Z2,y=pmagplotlib.plotCDF(fignum,Z2,"Z component",'b',"")
    bounds2=[Z2[minimum],Z2[maximum]]
    pmagplotlib.plotVs(fignum,bounds2,'b','--')
    plt.ylim(0,1)
    plt.locator_params(nbins=x_tick_bins)

    plt.tight_layout()
    if save == True:
        plt.savefig(os.path.join(save_folder, 'common_mean_bootstrap') + '.' + fmt)
    plt.show()


def common_mean_watson(Data1,Data2,NumSims=5000,plot='no', save=False, save_folder = '.', fmt = 'svg'):
    """
    Conduct a Watson V test for a common mean on two directional data sets.

    This function calculates Watson's V statistic from input files through
    Monte Carlo simulation in order to test whether two populations of
    directional data could have been drawn from a common mean. The critical
    angle between the two sample mean directions and the corresponding
    McFadden and McElhinny (1990) classification is printed.

    Required Parameters
    ----------
    Data1 : a nested list of directional data [dec,inc] (a di_block)
    Data2 : a nested list of directional data [dec,inc] (a di_block)

    Optional Parameters (defaults are used if not specified)
    ----------
    NumSims : number of Monte Carlo simulations (default is 5000)
    plot : the default is no plot ('no'). Putting 'yes' will the plot the CDF from
    the Monte Carlo simulations.
    save : optional save of plots (default is False)
    save_folder : path to directory where plots should be saved
    fmt : format of figures to be saved (default is 'svg')
    """
    pars_1=pmag.fisher_mean(Data1)
    pars_2=pmag.fisher_mean(Data2)
    cart_1=pmag.dir2cart([pars_1["dec"],pars_1["inc"],pars_1["r"]])
    cart_2=pmag.dir2cart([pars_2['dec'],pars_2['inc'],pars_2["r"]])
    Sw=pars_1['k']*pars_1['r']+pars_2['k']*pars_2['r'] # k1*r1+k2*r2
    xhat_1=pars_1['k']*cart_1[0]+pars_2['k']*cart_2[0] # k1*x1+k2*x2
    xhat_2=pars_1['k']*cart_1[1]+pars_2['k']*cart_2[1] # k1*y1+k2*y2
    xhat_3=pars_1['k']*cart_1[2]+pars_2['k']*cart_2[2] # k1*z1+k2*z2
    Rw=np.sqrt(xhat_1**2+xhat_2**2+xhat_3**2)
    V=2*(Sw-Rw)
    # keep weighted sum for later when determining the "critical angle"
    # let's save it as Sr (notation of McFadden and McElhinny, 1990)
    Sr=Sw

    # do monte carlo simulation of datasets with same kappas as data,
    # but a common mean
    counter=0
    Vp=[] # set of Vs from simulations
    for k in range(NumSims):

    # get a set of N1 fisher distributed vectors with k1,
    # calculate fisher stats
        Dirp=[]
        for i in range(pars_1["n"]):
            Dirp.append(pmag.fshdev(pars_1["k"]))
        pars_p1=pmag.fisher_mean(Dirp)
    # get a set of N2 fisher distributed vectors with k2,
    # calculate fisher stats
        Dirp=[]
        for i in range(pars_2["n"]):
            Dirp.append(pmag.fshdev(pars_2["k"]))
        pars_p2=pmag.fisher_mean(Dirp)
    # get the V for these
        Vk=pmag.vfunc(pars_p1,pars_p2)
        Vp.append(Vk)

    # sort the Vs, get Vcrit (95th percentile one)

    Vp.sort()
    k=int(.95*NumSims)
    Vcrit=Vp[k]

    # equation 18 of McFadden and McElhinny, 1990 calculates the critical
    # value of R (Rwc)

    Rwc=Sr-(Vcrit/2)

    # following equation 19 of McFadden and McElhinny (1990) the critical
    # angle is calculated. If the observed angle (also calculated below)
    # between the data set means exceeds the critical angle the hypothesis
    # of a common mean direction may be rejected at the 95% confidence
    # level. The critical angle is simply a different way to present
    # Watson's V parameter so it makes sense to use the Watson V parameter
    # in comparison with the critical value of V for considering the test
    # results. What calculating the critical angle allows for is the
    # classification of McFadden and McElhinny (1990) to be made
    # for data sets that are consistent with sharing a common mean.

    k1=pars_1['k']
    k2=pars_2['k']
    R1=pars_1['r']
    R2=pars_2['r']
    critical_angle=np.degrees(np.arccos(((Rwc**2)-((k1*R1)**2)
                                               -((k2*R2)**2))/
                                              (2*k1*R1*k2*R2)))
    D1=(pars_1['dec'],pars_1['inc'])
    D2=(pars_2['dec'],pars_2['inc'])
    angle=pmag.angle(D1,D2)

    print "Results of Watson V test: "
    print ""
    print "Watson's V:           " '%.1f' %(V)
    print "Critical value of V:  " '%.1f' %(Vcrit)

    if V<Vcrit:
        print '"Pass": Since V is less than Vcrit, the null hypothesis'
        print 'that the two populations are drawn from distributions'
        print 'that share a common mean direction can not be rejected.'
    elif V>Vcrit:
        print '"Fail": Since V is greater than Vcrit, the two means can'
        print 'be distinguished at the 95% confidence level.'
    print ""
    print "M&M1990 classification:"
    print ""
    print "Angle between data set means: " '%.1f'%(angle)
    print "Critical angle for M&M1990:   " '%.1f'%(critical_angle)

    if V>Vcrit:
        print ""
    elif V<Vcrit:
        if critical_angle<5:
            print "The McFadden and McElhinny (1990) classification for"
            print "this test is: 'A'"
        elif critical_angle<10:
            print "The McFadden and McElhinny (1990) classification for"
            print "this test is: 'B'"
        elif critical_angle<20:
            print "The McFadden and McElhinny (1990) classification for"
            print "this test is: 'C'"
        else:
            print "The McFadden and McElhinny (1990) classification for"
            print "this test is: 'INDETERMINATE;"

    if plot=='yes':
        CDF={'cdf':1}
        #pmagplotlib.plot_init(CDF['cdf'],5,5)
        plt.figure(figsize=(3.5,2.5))
        p1 = pmagplotlib.plotCDF(CDF['cdf'],Vp,"Watson's V",'r',"")
        p2 = pmagplotlib.plotVs(CDF['cdf'],[V],'g','-')
        p3 = pmagplotlib.plotVs(CDF['cdf'],[Vp[k]],'b','--')
        #pmagplotlib.drawFIGS(CDF)
        if save==True:
            plt.savefig(os.path.join(save_folder, 'common_mean_watson') + '.' + fmt)
        pmagplotlib.showFIG(CDF['cdf'])


def reversal_test_bootstrap(dec=None, inc=None, di_block=None, plot_stereo = False, save=False, save_folder='.',fmt='svg'):
    """
    Conduct a reversal test using bootstrap statistics (Tauxe, 2010) to
    determine whether two populations of directions could be from an antipodal
    common mean.

    Required Parameters
    ----------
    dec: list of declinations
    inc: list of inclinations

    or

    di_block: a nested list of [dec,inc]

    A di_block can be provided instead of dec, inc lists in which case it will
    be used. Either dec, inc lists or a di_block need to passed to the function.

    Optional Parameters (defaults are used if not specified)
    ----------
    plot_stereo : before plotting the CDFs, plot stereonet with the
    bidirectionally separated data (default is False)
    save : boolean argument to save plots (default is False)
    save_folder : directory where plots will be saved (default is current directory, '.')
    fmt : format of saved figures (default is 'svg')
    """
    if di_block is None:
        all_dirs = make_di_block(dec, inc)
    else:
        all_dirs = di_block

    directions1, directions2 = pmag.flip(all_dirs)

    if plot_stereo == True:
        # plot equal area with two modes
        plt.figure(num=0,figsize=(4,4))
        plot_net(0)
        plot_di(di_block = directions1,color='b'),
        plot_di(di_block = do_flip(di_block = directions2), color = 'r')

    common_mean_bootstrap(directions1, directions2, save=save, save_folder=save_folder, fmt=fmt)


def reversal_test_MM1990(dec=None, inc=None, di_block=None, plot_CDF=False, plot_stereo = False, save=False, save_folder='.', fmt='svg'):
    """
    Calculates Watson's V statistic from input files through Monte Carlo
    simulation in order to test whether normal and reversed populations could
    have been drawn from a common mean (equivalent to watsonV.py). Also provides
    the critical angle between the two sample mean directions and the
    corresponding McFadden and McElhinny (1990) classification.

    Required Parameters
    ----------
    dec: list of declinations
    inc: list of inclinations

    or

    di_block: a nested list of [dec,inc]

    A di_block can be provided instead of dec, inc lists in which case it will
    be used. Either dec, inc lists or a di_block need to passed to the function.

    Optional Parameters (defaults are used if not specified)
    ----------
    plot_CDF : plot the CDF accompanying the printed results (default is False)
    plot_stereo : plot stereonet with the bidirectionally separated data
        (default is False)
    save : boolean argument to save plots (default is False)
    save_folder : relative directory where plots will be saved
        (default is current directory, '.')
    fmt : format of saved figures (default is 'svg')
    """
    if di_block is None:
        all_dirs = make_di_block(dec, inc)
    else:
        all_dirs = di_block

    directions1, directions2 = pmag.flip(all_dirs)

    if plot_stereo == True:
        # plot equal area with two modes
        plt.figure(num=0,figsize=(4,4))
        plot_net(0)
        plot_di(di_block = directions1,color='b'),
        plot_di(di_block = do_flip(di_block = directions2), color = 'r')

    if plot_CDF == False:
        common_mean_watson(directions1, directions2, save=save, save_folder=save_folder, fmt=fmt)
    else:
        common_mean_watson(directions1, directions2, plot = 'yes', save=save, save_folder=save_folder, fmt=fmt)


def fishqq(lon=None, lat=None, di_block=None):
    """
    Test whether a distribution is Fisherian and make a corresponding Q-Q plot.
    The Q-Q plot shows the data plotted against the value expected from a
    Fisher distribution. The first plot is the uniform plot which is the
    Fisher model distribution in terms of longitude (declination). The second
    plot is the exponential plot which is the Fisher model distribution in terms
    of latitude (inclination). In addition to the plots, the test statistics Mu
    (uniform) and Me (exponential) are calculated and compared against the
    critical test values. If Mu or Me are too large in comparision to the test
    statistics, the hypothesis that the distribution is Fisherian is rejected
    (see Fisher et al., 1987).

    Parameters:
    -----------
    lon : longitude or declination of the data
    lat : latitude or inclination of the data

    or

    di_block: a nested list of [lon,lat,1.0] or [dec,inc,1.0]
    (di_block can be provided instead of lon, lat in which case it will be used)

    Output:
    -----------
    dictionary containing
    lon : mean longitude (or declination)
    lat : mean latitude (or inclination)
    N : number of vectors
    Mu : Mu test statistic value for the data
    Mu_critical : critical value for Mu
    Me : Me test statistic value for the data
    Me_critical : critical value for Me

    if the data has two modes with N >=10 (N and R)
    two of these dictionaries will be returned

    """
    if di_block is None:
        all_dirs = make_di_block(lon, lat)
    else:
        all_dirs = di_block

    ppars = pmag.doprinc(all_dirs) # get principal directions

    rDIs = []
    nDIs = []
    QQ_dict1 = {}
    QQ_dict2 = {}

    for rec in all_dirs:
        angle=pmag.angle([rec[0],rec[1]],[ppars['dec'],ppars['inc']])
        if angle>90.:
            rDIs.append(rec)
        else:
            nDIs.append(rec)

    if len(rDIs) >=10 or len(nDIs) >=10:
        D1,I1=[],[]
        QQ={'unf1':1,'exp1':2}
        if len(nDIs) < 10:
            ppars=pmag.doprinc(rDIs) # get principal directions
            Drbar,Irbar=ppars['dec']-180.,-ppars['inc']
            Nr=len(rDIs)
            for di in rDIs:
                d,irot=pmag.dotilt(di[0],di[1],Drbar-180.,90.-Irbar) # rotate to mean
                drot=d-180.
                if drot<0:drot=drot+360.
                D1.append(drot)
                I1.append(irot)
                Dtit='Mode 2 Declinations'
                Itit='Mode 2 Inclinations'
        else:
            ppars=pmag.doprinc(nDIs) # get principal directions
            Dnbar,Inbar=ppars['dec'],ppars['inc']
            Nn=len(nDIs)
            for di in nDIs:
                d,irot=pmag.dotilt(di[0],di[1],Dnbar-180.,90.-Inbar) # rotate to mean
                drot=d-180.
                if drot<0:drot=drot+360.
                D1.append(drot)
                I1.append(irot)
                Dtit='Mode 1 Declinations'
                Itit='Mode 1 Inclinations'
        Mu_n,Mu_ncr=pmagplotlib.plotQQunf(QQ['unf1'],D1,Dtit) # make plot
        Me_n,Me_ncr=pmagplotlib.plotQQexp(QQ['exp1'],I1,Itit) # make plot
        if Mu_n<=Mu_ncr and Me_n<=Me_ncr:
           F_n = 'consistent with Fisherian model'
        else:
           F_n = 'Fisherian model rejected'
        QQ_dict1['Mode'] = 'Mode 1'
        QQ_dict1['Dec'] = Dnbar
        QQ_dict1['Inc'] = Inbar
        QQ_dict1['N'] = Nn
        QQ_dict1['Mu'] = Mu_n
        QQ_dict1['Mu_critical'] = Mu_ncr
        QQ_dict1['Me'] = Me_n
        QQ_dict1['Me_critical'] = Me_ncr
        QQ_dict1['Test_result'] = F_n

    if len(rDIs)>10 and len(nDIs)>10:
        D2,I2=[],[]
        QQ['unf2']=3
        QQ['exp2']=4
        ppars=pmag.doprinc(rDIs) # get principal directions
        Drbar,Irbar=ppars['dec']-180.,-ppars['inc']
        Nr=len(rDIs)
        for di in rDIs:
            d,irot=pmag.dotilt(di[0],di[1],Drbar-180.,90.-Irbar) # rotate to mean
            drot=d-180.
            if drot<0:drot=drot+360.
            D2.append(drot)
            I2.append(irot)
            Dtit='Mode 2 Declinations'
            Itit='Mode 2 Inclinations'
        Mu_r,Mu_rcr=pmagplotlib.plotQQunf(QQ['unf2'],D2,Dtit) # make plot
        Me_r,Me_rcr=pmagplotlib.plotQQexp(QQ['exp2'],I2,Itit) # make plot

        if Mu_r<=Mu_rcr and Me_r<=Me_rcr:
           F_r = 'consistent with Fisherian model'
        else:
           F_r = 'Fisherian model rejected'
        QQ_dict2['Mode'] = 'Mode 2'
        QQ_dict2['Dec'] = Drbar
        QQ_dict2['Inc'] = Irbar
        QQ_dict2['N'] = Nr
        QQ_dict2['Mu'] = Mu_r
        QQ_dict2['Mu_critical'] = Mu_rcr
        QQ_dict2['Me'] = Me_r
        QQ_dict2['Me_critical'] = Me_rcr
        QQ_dict2['Test_result'] = F_r

    if QQ_dict2:
        return QQ_dict1, QQ_dict2
    elif QQ_dict1:
        return QQ_dict1
    else:
        print 'you need N> 10 for at least one mode'


def lat_from_inc(inc,a95=None):
    """
    Calculate paleolatitude from inclination using the dipole equation

    Required Parameter
    ----------
    inc: (paleo)magnetic inclination in degrees

    Optional Parameter
    ----------
    a95: 95% confidence interval from Fisher mean

    Returns
    ----------
    if a95 is provided paleo_lat, paleo_lat_max, paleo_lat_min are returned
    otherwise, it just returns paleo_lat
    """
    rad=np.pi/180.
    paleo_lat = np.arctan(0.5*np.tan(inc*rad))/rad
    if a95 is not None:
        paleo_lat_max = np.arctan(0.5*np.tan((inc+a95)*rad))/rad
        paleo_lat_min = np.arctan(0.5*np.tan((inc-a95)*rad))/rad
        return paleo_lat, paleo_lat_max, paleo_lat_min
    else:
        return paleo_lat


def lat_from_pole(ref_loc_lon,ref_loc_lat,pole_plon,pole_plat):
    """
    Calculate paleolatitude for a reference location based on a paleomagnetic pole

    Required Parameters
    ----------
    ref_loc_lon: longitude of reference location in degrees
    ref_loc_lat: latitude of reference location
    pole_plon: paleopole longitude in degrees
    pole_plat: paleopole latitude in degrees
    """

    ref_loc = (ref_loc_lon,ref_loc_lat)
    pole = (pole_plon, pole_plat)
    paleo_lat = 90-pmag.angle(pole,ref_loc)
    return float(paleo_lat)


def inc_from_lat(lat):
    """
    Calculate inclination predicted from latitude using the dipole equation

    Parameter
    ----------
    lat: latitude in degrees
    """
    rad=np.pi/180.
    inc=np.arctan(2*np.tan(lat*rad))/rad
    return inc





def plot_net(fignum):
    """
    Draws circle and tick marks for equal area projection.
    """

# make the perimeter
    plt.figure(num=fignum)
    plt.clf()
    plt.axis("off")
    Dcirc=np.arange(0,361.)
    Icirc=np.zeros(361,'f')
    Xcirc,Ycirc=[],[]
    for k in range(361):
        XY= pmag.dimap(Dcirc[k],Icirc[k])
        Xcirc.append(XY[0])
        Ycirc.append(XY[1])
    plt.plot(Xcirc,Ycirc,'k')

# put on the tick marks
    Xsym,Ysym=[],[]
    for I in range(10,100,10):
        XY=pmag.dimap(0.,I)
        Xsym.append(XY[0])
        Ysym.append(XY[1])
    plt.plot(Xsym,Ysym,'k+')
    Xsym,Ysym=[],[]
    for I in range(10,90,10):
        XY=pmag.dimap(90.,I)
        Xsym.append(XY[0])
        Ysym.append(XY[1])
    plt.plot(Xsym,Ysym,'k+')
    Xsym,Ysym=[],[]
    for I in range(10,90,10):
        XY=pmag.dimap(180.,I)
        Xsym.append(XY[0])
        Ysym.append(XY[1])
    plt.plot(Xsym,Ysym,'k+')
    Xsym,Ysym=[],[]
    for I in range(10,90,10):
        XY=pmag.dimap(270.,I)
        Xsym.append(XY[0])
        Ysym.append(XY[1])
    plt.plot(Xsym,Ysym,'k+')
    for D in range(0,360,10):
        Xtick,Ytick=[],[]
        for I in range(4):
            XY=pmag.dimap(D,I)
            Xtick.append(XY[0])
            Ytick.append(XY[1])
        plt.plot(Xtick,Ytick,'k')
    plt.axis("equal")
    plt.axis((-1.05,1.05,-1.05,1.05))


def plot_XY(X=None, Y=None,sym='ro'):
    plt.plot(X,Y,sym)

def plot_di(dec=None, inc=None, di_block=None, color='k', marker='o', markersize=20, legend='no', label='',title=''):
    """
    Plot declination, inclination data on an equal area plot.

    Before this function is called a plot needs to be initialized with code that looks
    something like:
    >fignum = 1
    >plt.figure(num=fignum,figsize=(10,10),dpi=160)
    >ipmag.plot_net(fignum)

    Required Parameters
    -----------
    dec : declination being plotted
    inc : inclination being plotted

    or

    di_block: a nested list of [dec,inc,1.0]
    (di_block can be provided instead of dec, inc in which case it will be used)

    Optional Parameters (defaults are used if not specified)
    -----------
    color : the default color is black. Other colors can be chosen (e.g. 'r')
    marker : the default marker is a circle ('o')
    markersize : default size is 20
    label : the default label is blank ('')
    legend : the default is no legend ('no'). Putting 'yes' will plot a legend.
    """
    X_down = []
    X_up = []
    Y_down = []
    Y_up = []

    if di_block is not None:
        di_lists = unpack_di_block(di_block)
        if len(di_lists) == 3:
            dec, inc, intensity = di_lists
        if len(di_lists) == 2:
            dec, inc = di_lists

    try:
        length = len(dec)
        for n in range(0,len(dec)):
            XY=pmag.dimap(dec[n],inc[n])
            if inc[n] >= 0:
                X_down.append(XY[0])
                Y_down.append(XY[1])
            else:
                X_up.append(XY[0])
                Y_up.append(XY[1])
    except:
        XY=pmag.dimap(dec,inc)
        if inc >= 0:
            X_down.append(XY[0])
            Y_down.append(XY[1])
        else:
            X_up.append(XY[0])
            Y_up.append(XY[1])

    if len(X_up)>0:
        plt.scatter(X_up,Y_up,facecolors='none', edgecolors=color,
                    s=markersize, marker=marker, label=label)

    if len(X_down)>0:
        plt.scatter(X_down,Y_down,facecolors=color, edgecolors=color,
                    s=markersize, marker=marker, label=label)
    if legend=='yes':
        plt.legend(loc=2)
    plt.tight_layout()
    if title!="":
        plt.title(title)


def plot_di_mean(dec,inc,a95,color='k',marker='o',markersize=20,label='',legend='no'):
    """
    Plot a mean direction (declination, inclination) with alpha_95 ellipse on
    an equal area plot.

    Before this function is called, a plot needs to be initialized with code
    that looks something like:
    >fignum = 1
    >plt.figure(num=fignum,figsize=(10,10),dpi=160)
    >ipmag.plot_net(fignum)

    Required Parameters
    -----------
    dec : declination of mean being plotted
    inc : inclination of mean being plotted
    a95 : a95 confidence ellipse of mean being plotted

    Optional Parameters (defaults are used if not specified)
    -----------
    color : the default color is black. Other colors can be chosen (e.g. 'r').
    marker : the default is a circle. Other symbols can be chosen (e.g. 's').
    markersize : the default is 20. Other sizes can be chosen.
    label : the default is no label. Labels can be assigned.
    legend : the default is no legend ('no'). Putting 'yes' will plot a legend.
    """
    DI_dimap=pmag.dimap(dec,inc)
    if inc < 0:
        plt.scatter(DI_dimap[0],DI_dimap[1],
        edgecolors=color ,facecolors='white',
        marker=marker,s=markersize,label=label)
    if inc >= 0:
        plt.scatter(DI_dimap[0],DI_dimap[1],
        edgecolors=color,facecolors=color,
        marker=marker,s=markersize,label=label)
    Xcirc,Ycirc=[],[]
    Da95,Ia95=pmag.circ(dec,inc,a95)
    if legend=='yes':
        plt.legend(loc=2)
    for k in range(len(Da95)):
        XY=pmag.dimap(Da95[k],Ia95[k])
        Xcirc.append(XY[0])
        Ycirc.append(XY[1])
    plt.plot(Xcirc,Ycirc,c=color)
    plt.tight_layout()

def plot_di_mean_bingham(bingham_dictionary,fignum=1,color='k',marker='o',markersize=20,label='',legend='no'):
    """
    Plot a mean direction (declination, inclination) bingham confidence ellipse.

    Required Parameters
    -----------
    bingham_dictionary : a dictionary generated by the pmag.dobingham function

    """
    pars = []
    pars.append(bingham_dictionary['dec'])
    pars.append(bingham_dictionary['inc'])
    pars.append(bingham_dictionary['Zeta'])
    pars.append(bingham_dictionary['Zdec'])
    pars.append(bingham_dictionary['Zinc'])
    pars.append(bingham_dictionary['Eta'])
    pars.append(bingham_dictionary['Edec'])
    pars.append(bingham_dictionary['Einc'])

    DI_dimap=pmag.dimap(bingham_dictionary['dec'],bingham_dictionary['inc'])
    if bingham_dictionary['inc'] < 0:
        plt.scatter(DI_dimap[0],DI_dimap[1],
        edgecolors=color ,facecolors='white',
        marker=marker,s=markersize,label=label)
    if bingham_dictionary['inc'] >= 0:
        plt.scatter(DI_dimap[0],DI_dimap[1],
        edgecolors=color,facecolors=color,
        marker=marker,s=markersize,label=label)
    pmagplotlib.plotELL(fignum,pars,color,0,1)

def plot_pole(mapname,plon,plat,A95,label='',color='k',marker='o',markersize=20,legend='no'):
    """
    This function plots a paleomagnetic pole and A95 error ellipse on whatever
    current map projection has been set using the basemap plotting library.

    Before this function is called, a plot needs to be initialized with code
    that looks something like:
    >from mpl_toolkits.basemap import Basemap
    >mapname = Basemap(projection='ortho',lat_0=35,lon_0=200)
    >plt.figure(figsize=(6, 6))
    >mapname.drawcoastlines(linewidth=0.25)
    >mapname.fillcontinents(color='bisque',lake_color='white',zorder=1)
    >mapname.drawmapboundary(fill_color='white')
    >mapname.drawmeridians(np.arange(0,360,30))
    >mapname.drawparallels(np.arange(-90,90,30))

    Required Parameters
    -----------
    mapname : the name of the current map that has been developed using basemap
    plon : the longitude of the paleomagnetic pole being plotted (in degrees E)
    plat : the latitude of the paleomagnetic pole being plotted (in degrees)
    A95 : the A_95 confidence ellipse of the paleomagnetic pole (in degrees)

    Optional Parameters (defaults are used if not specified)
    -----------
    color : the default color is black. Other colors can be chosen (e.g. 'r')
    marker : the default is a circle. Other symbols can be chosen (e.g. 's')
    markersize : the default is 20. Other size can be chosen
    label : the default is no label. Labels can be assigned.
    legend : the default is no legend ('no'). Putting 'yes' will plot a legend.
    """
    centerlon, centerlat = mapname(plon,plat)
    A95_km=A95*111.32
    mapname.scatter(centerlon,centerlat,marker=marker,color=color,s=markersize,label=label,zorder=101)
    equi(mapname, plon, plat, A95_km,color)
    if legend=='yes':
        plt.legend(loc=2)


def plot_pole_colorbar(mapname,plon,plat,A95,cmap,vmin,vmax,label='',color='k',marker='o',markersize='20',alpha='1.0',legend='no'):
    """
    This function plots a paleomagnetic pole and A95 error ellipse on whatever
    current map projection has been set using the basemap plotting library.

    Required Parameters
    -----------
    mapname : the name of the current map that has been developed using basemap
    plon : the longitude of the paleomagnetic pole being plotted (in degrees E)
    plat : the latitude of the paleomagnetic pole being plotted (in degrees)
    A95 : the A_95 confidence ellipse of the paleomagnetic pole (in degrees)

    Optional Parameters (defaults are used if not specified)
    -----------
    label : a string that is the label for the paleomagnetic pole being plotted
    color : the color desired for the symbol and its A95 ellipse (default is 'k' aka black)
    marker : the marker shape desired for the pole mean symbol (default is 'o' aka a circle)
    legend : the default is no legend ('no'). Putting 'yes' will plot a legend.
    """
    centerlon, centerlat = mapname(plon,plat)
    A95_km=A95*111.32
    mapname.scatter(centerlon,centerlat,c=cmap,vmin=vmin,vmax=vmax,s=markersize,marker=marker,color=color,alpha=alpha,label=label,zorder=101)
    equi_colormap(mapname, plon, plat, A95_km, color, alpha)
    if legend=='yes':
        plt.legend(loc=2)


def plot_vgp(mapname,vgp_lon=None,vgp_lat=None,di_block=None,label='',color='k',marker='o',legend='no'):
    """
    This function plots a paleomagnetic pole on whatever current map projection
    has been set using the basemap plotting library.

    Before this function is called, a plot needs to be initialized with code
    that looks something like:
    >from mpl_toolkits.basemap import Basemap
    >mapname = Basemap(projection='ortho',lat_0=35,lon_0=200)
    >plt.figure(figsize=(6, 6))
    >mapname.drawcoastlines(linewidth=0.25)
    >mapname.fillcontinents(color='bisque',lake_color='white',zorder=1)
    >mapname.drawmapboundary(fill_color='white')
    >mapname.drawmeridians(np.arange(0,360,30))
    >mapname.drawparallels(np.arange(-90,90,30))

    Required Parameters
    -----------
    mapname : the name of the current map that has been developed using basemap
    plon : the longitude of the paleomagnetic pole being plotted (in degrees E)
    plat : the latitude of the paleomagnetic pole being plotted (in degrees)

    Optional Parameters (defaults are used if not specified)
    -----------
    color : the color desired for the symbol and its A95 ellipse (default is 'k' aka black)
    marker : the marker shape desired for the pole mean symbol (default is 'o' aka a circle)
    label : the default is no label. Labels can be assigned.
    legend : the default is no legend ('no'). Putting 'yes' will plot a legend.
    """
    if di_block!=None:
        di_lists = unpack_di_block(di_block)
        if len(di_lists) == 3:
            vgp_lon,vgp_lat, intensity = di_lists
        if len(di_lists) == 2:
            vgp_lon,vgp_lat = di_lists
    centerlon, centerlat = mapname(vgp_lon,vgp_lat)
    mapname.scatter(centerlon,centerlat,20,marker=marker,color=color,label=label,zorder=100)
    if legend=='yes':
        plt.legend(loc=2)


def vgp_calc(dataframe,tilt_correction='yes', site_lon = 'site_lon', site_lat = 'site_lat', dec_is = 'dec_is', inc_is = 'inc_is', dec_tc = 'dec_tc', inc_tc = 'inc_tc'):
    """
    This function calculates paleomagnetic poles using directional data and site location data within a pandas.DataFrame. The function adds the columns 'paleolatitude', 'pole_lat', 'pole_lon', 'pole_lat_rev', and 'pole_lon_rev' to the dataframe. The '_rev' columns allow for subsequent choice as to which polarity will be used for the VGPs.

    Parameters
    -----------
    dataframe : the name of the pandas.DataFrame containing the data

    ----- the following default parameters can be changes by keyword argument -----
    tilt-correction : 'yes' is the default and uses tilt-corrected data (dec_tc, inc_tc), 'no' uses data that is not tilt-corrected and is in geographic coordinates
    dataframe['site_lat'] : the name of the Dataframe column containing the latitude of the site
    dataframe['site_lon'] : the name of the Dataframe column containing the longitude of the site
    dataframe['inc_tc'] : the name of the Dataframe column containing the tilt-corrected inclination (used by default tilt-correction='yes')
    dataframe['dec_tc'] : the name of the Dataframe column containing the tilt-corrected declination (used by default tilt-correction='yes')
    dataframe['inc_is'] : the name of the Dataframe column containing the insitu inclination (used when tilt-correction='no')
    dataframe['dec_is'] : the name of the Dataframe column containing the insitu declination (used when tilt-correction='no')
    """
    dataframe.is_copy = False
    if tilt_correction=='yes':
        #calculate the paleolatitude/colatitude
        dataframe['paleolatitude']=np.degrees(np.arctan(0.5*np.tan(np.radians(dataframe[inc_tc]))))
        dataframe['colatitude']=90-dataframe['paleolatitude']
        #calculate the latitude of the pole
        dataframe['vgp_lat']=np.degrees(np.arcsin(np.sin(np.radians(dataframe[site_lat]))*
                                                             np.cos(np.radians(dataframe['colatitude']))+
                                                             np.cos(np.radians(dataframe[site_lat]))*
                                                             np.sin(np.radians(dataframe['colatitude']))*
                                                             np.cos(np.radians(dataframe[dec_tc]))))
        #calculate the longitudinal difference between the pole and the site (beta)
        dataframe['beta']=np.degrees(np.arcsin((np.sin(np.radians(dataframe['colatitude']))*
                                          np.sin(np.radians(dataframe[dec_tc])))/
                                         (np.cos(np.radians(dataframe['vgp_lat'])))))
        #generate a boolean array (mask) to use to distinguish between the two possibilities for pole longitude
        #and then calculate pole longitude using the site location and calculated beta
        mask = np.cos(np.radians(dataframe['colatitude']))>np.sin(np.radians(dataframe[site_lat]))*np.sin(np.radians(dataframe['vgp_lat']))
        dataframe['vgp_lon']=np.where(mask,(dataframe[site_lon]+dataframe['beta'])%360.,(dataframe[site_lon]+180-dataframe['beta'])%360.)
        #calculate the antipode of the poles
        dataframe['vgp_lat_rev']=-dataframe['vgp_lat']
        dataframe['vgp_lon_rev']=(dataframe['vgp_lon']-180.)%360.
        #the 'colatitude' and 'beta' columns were created for the purposes of the pole calculations
        #but aren't of further use and are deleted
        del dataframe['colatitude']
        del dataframe['beta']
    if tilt_correction=='no':
        #calculate the paleolatitude/colatitude
        dataframe['paleolatitude']=np.degrees(np.arctan(0.5*np.tan(np.radians(dataframe[inc_is]))))
        dataframe['colatitude']=90-dataframe['paleolatitude']
        #calculate the latitude of the pole
        dataframe['vgp_lat']=np.degrees(np.arcsin(np.sin(np.radians(dataframe[site_lat]))*
                                                             np.cos(np.radians(dataframe['colatitude']))+
                                                             np.cos(np.radians(dataframe[site_lat]))*
                                                             np.sin(np.radians(dataframe['colatitude']))*
                                                             np.cos(np.radians(dataframe[dec_is]))))
        #calculate the longitudinal difference between the pole and the site (beta)
        dataframe['beta']=np.degrees(np.arcsin((np.sin(np.radians(dataframe['colatitude']))*
                                          np.sin(np.radians(dataframe['dec_is'])))/
                                         (np.cos(np.radians(dataframe['vgp_lat'])))))
        #generate a boolean array (mask) to use to distinguish between the two possibilities for pole longitude
        #and then calculate pole longitude using the site location and calculated beta
        mask = np.cos(np.radians(dataframe['colatitude']))>np.sin(np.radians(dataframe[site_lat]))*np.sin(np.radians(dataframe['vgp_lat']))
        dataframe['vgp_lon']=np.where(mask,(dataframe[site_lon]+dataframe['beta'])%360.,(dataframe[site_lon]+180-dataframe['beta'])%360.)
        #calculate the antipode of the poles
        dataframe['vgp_lat_rev']=-dataframe['vgp_lat']
        dataframe['vgp_lon_rev']=(dataframe['vgp_lon']-180.)%360.
        #the 'colatitude' and 'beta' columns were created for the purposes of the pole calculations
        #but aren't of further use and are deleted
        del dataframe['colatitude']
        del dataframe['beta']


def sb_vgp_calc(dataframe,site_correction = 'yes', dec_tc = 'dec_tc', inc_tc = 'inc_tc'):
    """
    This function calculates the angular dispersion of VGPs and corrects
    for within site dispersion (unless site_correction = 'no') to return
    a value S_b. The input data needs to be within a pandas Dataframe.

    Parameters
    -----------
    dataframe : the name of the pandas.DataFrame containing the data

    the data frame needs to contain these columns:
    dataframe['site_lat'] : latitude of the site
    dataframe['site_lon'] : longitude of the site
    dataframe['k'] : fisher precision parameter for directions
    dataframe['vgp_lat'] : VGP latitude
    dataframe['vgp_lon'] : VGP longitude
    ----- the following default parameters can be changes by keyword argument -----
    dataframe['inc_tc'] : tilt-corrected inclination
    dataframe['dec_tc'] : tilt-corrected declination

    plot : default is 'no', will make a plot of poles if 'yes'
    """

    # calculate the mean from the directional data
    dataframe_dirs=[]
    for n in range(0,len(dataframe)):
        dataframe_dirs.append([dataframe[dec_tc][n],
                               dataframe[inc_tc][n],1.])
    dataframe_dir_mean=pmag.fisher_mean(dataframe_dirs)

    # calculate the mean from the vgp data
    dataframe_poles=[]
    dataframe_pole_lats=[]
    dataframe_pole_lons=[]
    for n in range(0,len(dataframe)):
        dataframe_poles.append([dataframe['vgp_lon'][n],
                                dataframe['vgp_lat'][n],1.])
        dataframe_pole_lats.append(dataframe['vgp_lat'][n])
        dataframe_pole_lons.append(dataframe['vgp_lon'][n])
    dataframe_pole_mean=pmag.fisher_mean(dataframe_poles)

    # calculate mean paleolatitude from the directional data
    dataframe['paleolatitude']=lat_from_inc(dataframe_dir_mean['inc'])

    angle_list=[]
    for n in range(0,len(dataframe)):
        angle=pmag.angle([dataframe['vgp_lon'][n],dataframe['vgp_lat'][n]],
                         [dataframe_pole_mean['dec'],dataframe_pole_mean['inc']])
        angle_list.append(angle[0])
    dataframe['delta_mean_pole']=angle_list

    if site_correction == 'yes':
        # use eq. 2 of Cox (1970) to translate the directional precision parameter
        # into pole coordinates using the assumption of a Fisherian distribution in
        # directional coordinates and the paleolatitude as calculated from mean
        # inclination using the dipole equation
        dataframe['K']=dataframe['k']/(0.125*(5+18*np.sin(np.deg2rad(dataframe['paleolatitude']))**2
                                              +9*np.sin(np.deg2rad(dataframe['paleolatitude']))**4))
        dataframe['Sw']=81/(dataframe['K']**0.5)

        summation=0
        N=0
        for n in range(0,len(dataframe)):
            quantity=dataframe['delta_mean_pole'][n]**2-dataframe['Sw'][n]**2/dataframe['n'][n]
            summation+=quantity
            N+=1

        Sb=((1.0/(N-1.0))*summation)**0.5

    if site_correction == 'no':

        summation=0
        N=0
        for n in range(0,len(dataframe)):
            quantity=dataframe['delta_mean_pole'][n]**2
            summation+=quantity
            N+=1

        Sb=((1.0/(N-1.0))*summation)**0.5

    return Sb


def make_di_block(dec,inc):
    """
    Some pmag.py functions require a list of unit vectors [dec,inc,1.] as input. This
    function takes declination and inclination data and make it into such a list
    """
    di_block=[]
    for n in range(0,len(dec)):
        di_block.append([dec[n],inc[n],1.0])
    return di_block


def unpack_di_block(di_block):
    """
    This function unpacks a nested list of [dec,inc,mag_moment] into a list of
    declination values, a list of inclination values and a list of magnetic
    moment values. Mag_moment values are optional, while dec and inc values are
    required.
    """
    dec_list = []
    inc_list = []
    moment_list = []

    for n in range(0,len(di_block)):
        dec = di_block[n][0]
        inc = di_block[n][1]
        dec_list.append(dec)
        inc_list.append(inc)
        if len(di_block[n])>2:
            moment = di_block[n][2]
            moment_list.append(moment)

    return dec_list, inc_list, moment_list


def make_diddd_array(dec,inc,dip_direction,dip):
    """
    Some pmag.py functions such as the bootstrap fold test require a numpy array
     of dec, inc, dip direction, dip [dec,inc,dd,dip] as input. This function
     makes such a list.

    Parameters
    -----------
    dec : paleomagnetic declination in degrees
    inc : paleomagnetic inclination in degrees
    dip_direction : the dip direction of bedding (in degrees between 0 and 360)
    dip: dip of bedding (in degrees)
    """
    diddd_block=[]
    for n in range(0,len(dec)):
        diddd_block.append([dec[n],inc[n],dip_direction[n],dip[n]])
    diddd_array = np.array(diddd_block)
    return diddd_array


def shoot(lon, lat, azimuth, maxdist=None):
    """
    This function enables A95 error ellipses to be drawn in basemap around paleomagnetic
    poles in conjunction with equi
    (from: http://www.geophysique.be/2011/02/20/matplotlib-basemap-tutorial-09-drawing-circles/)
    """
    glat1 = lat * np.pi / 180.
    glon1 = lon * np.pi / 180.
    s = maxdist / 1.852
    faz = azimuth * np.pi / 180.

    EPS= 0.00000000005
    if ((np.abs(np.cos(glat1))<EPS) and not (np.abs(np.sin(faz))<EPS)):
        alert("Only N-S courses are meaningful, starting at a pole!")

    a=6378.13/1.852
    f=1/298.257223563
    r = 1 - f
    tu = r * np.tan(glat1)
    sf = np.sin(faz)
    cf = np.cos(faz)
    if (cf==0):
        b=0.
    else:
        b=2. * np.arctan2 (tu, cf)

    cu = 1. / np.sqrt(1 + tu * tu)
    su = tu * cu
    sa = cu * sf
    c2a = 1 - sa * sa
    x = 1. + np.sqrt(1. + c2a * (1. / (r * r) - 1.))
    x = (x - 2.) / x
    c = 1. - x
    c = (x * x / 4. + 1.) / c
    d = (0.375 * x * x - 1.) * x
    tu = s / (r * a * c)
    y = tu
    c = y + 1
    while (np.abs (y - c) > EPS):

        sy = np.sin(y)
        cy = np.cos(y)
        cz = np.cos(b + y)
        e = 2. * cz * cz - 1.
        c = y
        x = e * cy
        y = e + e - 1.
        y = (((sy * sy * 4. - 3.) * y * cz * d / 6. + x) *
              d / 4. - cz) * sy * d + tu

    b = cu * cy * cf - su * sy
    c = r * np.sqrt(sa * sa + b * b)
    d = su * cy + cu * sy * cf
    glat2 = (np.arctan2(d, c) + np.pi) % (2*np.pi) - np.pi
    c = cu * cy - su * sy * cf
    x = np.arctan2(sy * sf, c)
    c = ((-3. * c2a + 4.) * f + 4.) * c2a * f / 16.
    d = ((e * cy * c + cz) * sy * c + y) * sa
    glon2 = ((glon1 + x - (1. - c) * d * f + np.pi) % (2*np.pi)) - np.pi

    baz = (np.arctan2(sa, b) + np.pi) % (2 * np.pi)

    glon2 *= 180./np.pi
    glat2 *= 180./np.pi
    baz *= 180./np.pi

    return (glon2, glat2, baz)


def equi(m, centerlon, centerlat, radius, color):
    """
    This function enables A95 error ellipses to be drawn in basemap around paleomagnetic poles
    in conjunction with shoot
    (from: http://www.geophysique.be/2011/02/20/matplotlib-basemap-tutorial-09-drawing-circles/).
    """
    glon1 = centerlon
    glat1 = centerlat
    X = []
    Y = []
    for azimuth in range(0, 360):
        glon2, glat2, baz = shoot(glon1, glat1, azimuth, radius)
        X.append(glon2)
        Y.append(glat2)
    X.append(X[0])
    Y.append(Y[0])

    X,Y = m(X,Y)
    plt.plot(X,Y,color)


def equi_colormap(m, centerlon, centerlat, radius, color, alpha='1.0'):
    """
    This function enables A95 error ellipses to be drawn in basemap around paleomagnetic poles
    in conjunction with shoot
    (from: http://www.geophysique.be/2011/02/20/matplotlib-basemap-tutorial-09-drawing-circles/).
    """
    glon1 = centerlon
    glat1 = centerlat
    X = []
    Y = []
    for azimuth in range(0, 360):
        glon2, glat2, baz = shoot(glon1, glat1, azimuth, radius)
        X.append(glon2)
        Y.append(glat2)
    X.append(X[0])
    Y.append(Y[0])

    X,Y = m(X,Y)
    plt.plot(X,Y,color,alpha=alpha)


def combine_magic(filenames, outfile):
    """
    Takes a list of magic-formatted files, concatenates them, and creates a single file.
    Returns true if the operation was successful.

    Parameters
    -----------
    filenames : list of MagIC formatted files
    outfile : name of output file
    """
    datasets = []
    if not filenames:
        print "You must provide at least one file"
        return False
    for infile in filenames:
        if not os.path.isfile(infile):
            print "{} is not a valid file name".format(infile)
            return False
        dataset, file_type = pmag.magic_read(infile)
        print "File ",infile," read in with ",len(dataset), " records"
        for rec in dataset:
            datasets.append(rec)

    Recs, keys = pmag.fillkeys(datasets)
    pmag.magic_write(outfile,Recs,file_type)
    print "All records stored in ",outfile
    return True


def aniso_depthplot(ani_file='rmag_anisotropy.txt', meas_file='magic_measurements.txt', samp_file='er_samples.txt', age_file=None, sum_file=None, fmt='svg', dmin=-1, dmax=-1, depth_scale='sample_composite_depth', dir_path = '.'):

    """
    returns matplotlib figure with anisotropy data plotted against depth
    available depth scales: 'sample_composite_depth', 'sample_core_depth', or 'age' (you must provide an age file to use this option)

    """
    pcol=4
    tint=9
    plots = 0

    # format files to use full path
    ani_file = os.path.join(dir_path, ani_file)
    if not os.path.isfile(ani_file):
        print "Could not find rmag_anisotropy type file: {}.\nPlease provide a valid file path and try again".format(ani_file)
        return False, "Could not find rmag_anisotropy type file: {}.\nPlease provide a valid file path and try again".format(ani_file)

    meas_file = os.path.join(dir_path, meas_file)
    #print 'meas_file', meas_file

    if age_file:
        if not os.path.isfile(age_file):
            print 'Warning: you have provided an invalid age file.  Attempting to use sample file instead'
            age_file = None
            depth_scale = 'sample_core_depth'
            samp_file = os.path.join(dir_path, samp_file)
        else:
            samp_file = os.path.join(dir_path, age_file)
            depth_scale='age'
            print 'Warning: you have provided an er_ages format file, which will take precedence over er_samples'
    else:
        samp_file = os.path.join(dir_path, samp_file)

    label=1

    if sum_file:
        sum_file = os.path.join(dir_path, sum_file)

    dmin, dmax = float(dmin), float(dmax)

    # get data read in
    isbulk=0 # tests if there are bulk susceptibility measurements
    AniData,file_type=pmag.magic_read(ani_file)  # read in tensor elements
    if not age_file:
        Samps,file_type=pmag.magic_read(samp_file)  # read in sample depth info from er_sample.txt format file
    else:
        Samps,file_type=pmag.magic_read(samp_file)  # read in sample age info from er_ages.txt format file
        age_unit=Samps[0]['age_unit']
    for s in Samps:
        s['er_sample_name']=s['er_sample_name'].upper() # change to upper case for every sample name
    Meas,file_type=pmag.magic_read(meas_file)
    #print 'meas_file', meas_file
    #print 'file_type', file_type
    if file_type=='magic_measurements':
        isbulk=1
    Data=[]
    Bulks=[]
    BulkDepths=[]
    for rec in AniData:
        samprecs=pmag.get_dictitem(Samps,'er_sample_name',rec['er_sample_name'].upper(),'T') # look for depth record for this sample
        sampdepths=pmag.get_dictitem(samprecs,depth_scale,'','F') # see if there are non-blank depth data
        if dmax!=-1:
            sampdepths=pmag.get_dictitem(sampdepths,depth_scale,dmax,'max') # fishes out records within depth bounds
            sampdepths=pmag.get_dictitem(sampdepths,depth_scale,dmin,'min')
        if len(sampdepths)>0: # if there are any....
            rec['core_depth'] = sampdepths[0][depth_scale] # set the core depth of this record
            Data.append(rec) # fish out data with core_depth
            if isbulk:  # if there are bulk data
                chis=pmag.get_dictitem(Meas,'er_specimen_name',rec['er_specimen_name'],'T')
                chis=pmag.get_dictitem(chis,'measurement_chi_volume','','F') # get the non-zero values for this specimen
                if len(chis)>0: # if there are any....
                    Bulks.append(1e6*float(chis[0]['measurement_chi_volume'])) # put in microSI
                    BulkDepths.append(float(sampdepths[0][depth_scale]))
    if len(Bulks)>0: # set min and max bulk values
        bmin=min(Bulks)
        bmax=max(Bulks)
    xlab="Depth (m)"
    if len(Data)>0:
        location=Data[0]['er_location_name']
    else:
        return False, 'no data to plot'

    # collect the data for plotting tau  V3_inc and V1_dec
    Depths,Tau1,Tau2,Tau3,V3Incs,P,V1Decs=[],[],[],[],[],[],[]
    F23s=[]
    Axs=[] # collect the plot ids
# START HERE
    if len(Bulks)>0: pcol+=1
    s1=pmag.get_dictkey(Data,'anisotropy_s1','f') # get all the s1 values from Data as floats
    s2=pmag.get_dictkey(Data,'anisotropy_s2','f')
    s3=pmag.get_dictkey(Data,'anisotropy_s3','f')
    s4=pmag.get_dictkey(Data,'anisotropy_s4','f')
    s5=pmag.get_dictkey(Data,'anisotropy_s5','f')
    s6=pmag.get_dictkey(Data,'anisotropy_s6','f')
    nmeas=pmag.get_dictkey(Data,'anisotropy_n','int')
    sigma=pmag.get_dictkey(Data,'anisotropy_sigma','f')
    Depths=pmag.get_dictkey(Data,'core_depth','f')
    #Ss=np.array([s1,s4,s5,s4,s2,s6,s5,s6,s3]).transpose() # make an array
    Ss=np.array([s1,s2,s3,s4,s5,s6]).transpose() # make an array
    #Ts=np.reshape(Ss,(len(Ss),3,-1)) # and re-shape to be n-length array of 3x3 sub-arrays
    for k in range(len(Depths)):
        #tau,Evecs= pmag.tauV(Ts[k]) # get the sorted eigenvalues and eigenvectors
        #v3=pmag.cart2dir(Evecs[2])[1] # convert to inclination of the minimum eigenvector
        fpars=pmag.dohext(nmeas[k]-6,sigma[k],Ss[k])
        V3Incs.append(fpars['v3_inc'])
        V1Decs.append(fpars['v1_dec'])
        Tau1.append(fpars['t1'])
        Tau2.append(fpars['t2'])
        Tau3.append(fpars['t3'])
        P.append(Tau1[-1]/Tau3[-1])
        F23s.append(fpars['F23'])
    if len(Depths)>0:
        if dmax==-1:
            dmax=max(Depths)
            dmin=min(Depths)
        tau_min=1
        for t in Tau3:
            if t>0 and t<tau_min:tau_min=t
        tau_max=max(Tau1)
        #tau_min=min(Tau3)
        P_max=max(P)
        P_min=min(P)
        #dmax=dmax+.05*dmax
        #dmin=dmin-.05*dmax

        main_plot = plt.figure(1,figsize=(10,8)) # make the figure

        version_num=pmag.get_version()
        plt.figtext(.02,.01,version_num) # attach the pmagpy version number
        ax=plt.subplot(1,pcol,1) # make the first column
        Axs.append(ax)
        ax.plot(Tau1,Depths,'rs')
        ax.plot(Tau2,Depths,'b^')
        ax.plot(Tau3,Depths,'ko')
        if sum_file:
            core_depth_key, core_label_key, Cores = read_core_csv_file(sum_file)
            for core in Cores:
                 depth=float(core[core_depth_key])
                 if depth>dmin and depth<dmax:
                    plt.plot([0,90],[depth,depth],'b--')
        ax.axis([tau_min,tau_max,dmax,dmin])
        ax.set_xlabel('Eigenvalues')
        if depth_scale=='sample_core_depth':
            ax.set_ylabel('Depth (mbsf)')
        elif depth_scale=='age':
            ax.set_ylabel('Age ('+age_unit+')')
        else:
            ax.set_ylabel('Depth (mcd)')
        ax2=plt.subplot(1,pcol,2) # make the second column
        ax2.plot(P,Depths,'rs')
        ax2.axis([P_min,P_max,dmax,dmin])
        ax2.set_xlabel('P')
        ax2.set_title(location)
        if sum_file:
            for core in Cores:
                 depth=float(core[core_depth_key])
                 if depth>dmin and depth<dmax:
                    plt.plot([0,90],[depth,depth],'b--')
        Axs.append(ax2)
        ax3=plt.subplot(1,pcol,3)
        Axs.append(ax3)
        ax3.plot(V3Incs,Depths,'ko')
        ax3.axis([0,90,dmax,dmin])
        ax3.set_xlabel('V3 Inclination')
        if sum_file:
            for core in Cores:
                 depth=float(core[core_depth_key])
                 if depth>dmin and depth<dmax:
                    plt.plot([0,90],[depth,depth],'b--')
        ax4=plt.subplot(1,np.abs(pcol),4)
        Axs.append(ax4)
        ax4.plot(V1Decs,Depths,'rs')
        ax4.axis([0,360,dmax,dmin])
        ax4.set_xlabel('V1 Declination')
        if sum_file:
            for core in Cores:
                 depth=float(core[core_depth_key])
                 if depth>=dmin and depth<=dmax:
                    plt.plot([0,360],[depth,depth],'b--')
                    if pcol==4 and label==1:plt.text(360,depth+tint,core[core_label_key])
        #ax5=plt.subplot(1,np.abs(pcol),5)
        #Axs.append(ax5)
        #ax5.plot(F23s,Depths,'rs')
        #bounds=ax5.axis()
        #ax5.axis([bounds[0],bounds[1],dmax,dmin])
        #ax5.set_xlabel('F_23')
        #ax5.semilogx()
        #if sum_file:
        #    for core in Cores:
        #         depth=float(core[core_depth_key])
        #         if depth>=dmin and depth<=dmax:
        #            plt.plot([bounds[0],bounds[1]],[depth,depth],'b--')
        #            if pcol==5 and label==1:plt.text(bounds[1],depth+tint,core[core_label_key])
        #if pcol==6:
        if pcol==5:
            #ax6=plt.subplot(1,pcol,6)
            ax6=plt.subplot(1,pcol,5)
            Axs.append(ax6)
            ax6.plot(Bulks,BulkDepths,'bo')
            ax6.axis([bmin-1,1.1*bmax,dmax,dmin])
            ax6.set_xlabel('Bulk Susc. (uSI)')
            if sum_file:
                for core in Cores:
                     depth=float(core[core_depth_key])
                     if depth>=dmin and depth<=dmax:
                        plt.plot([0,bmax],[depth,depth],'b--')
                        if label==1:plt.text(1.1*bmax,depth+tint,core[core_label_key])
        for x in Axs:
            pmagplotlib.delticks(x) # this makes the x-tick labels more reasonable - they were overcrowded using the defaults
        fig_name = location + '_ani_depthplot.' + fmt
        return main_plot, fig_name
    else:
        return False, "No data to plot"

def core_depthplot(input_dir_path='.', meas_file='magic_measurements.txt', spc_file='',
                   samp_file='', age_file='', sum_file='', wt_file='',
                   depth_scale='sample_core_depth', dmin=-1, dmax=-1, sym='bo',
                   size=5, spc_sym='ro', spc_size=5, meth='', step=0, fmt='svg',
                   pltDec=True, pltInc=True, pltMag=True, pltLine=True, pltSus=True,
                   logit=False, pltTime=False, timescale=None, amin=-1, amax=-1,
                   norm=False):
    """
    depth scale can be 'sample_core_depth' or 'sample_composite_depth'
    if age file is provided, depth_scale will be set to 'age' by default
    """
    #print 'input_dir_path', input_dir_path, 'meas_file', meas_file, 'spc_file', spc_file
    #print 'samp_file', samp_file, 'age_file', age_file, 'depth_scale', depth_scale
    #print 'dmin', dmin, 'dmax', dmax, 'sym', sym, 'size', size, 'spc_sym', spc_sym, 'spc_size', spc_size,
    #print 'meth', meth, 'step', step, 'fmt', fmt, 'pltDec', pltDec, 'pltInc', pltInc, 'pltMag', pltMag,
    #print 'pltLine', pltLine, 'pltSus', pltSus, 'logit', logit, 'timescale', timescale, 'amin', amin, 'amax', amax
    #print 'pltTime', pltTime
    #print 'norm', norm
    intlist=['measurement_magnitude','measurement_magn_moment','measurement_magn_volume','measurement_magn_mass']
    width=10
    Ssym,Ssize='cs',5
    pcol=3
    pel=3
    maxInt=-1000
    minInt=1e10
    maxSuc=-1000
    minSuc=10000
    main_plot = None
    if size:
        size = int(size)
    if spc_size:
        spc_size = int(spc_size)


    # files not supported for the moment
    ngr_file="" # nothing needed, not implemented fully in original script
    suc_file="" # nothing else needed, also was not implemented in original script
    res_file="" # need also res_sym, res_size
    wig_file=""#  if wig_file: pcol+=1; width+=2

    title,location="",""

    if not pltDec:
        pcol-=1
        pel-=1
        width-=2
    if not pltInc:
        pcol-=1
        pel-=1
        width-=2
    if not pltMag:
        pcol-=1
        pel-=1
        width-=2


    if not step or meth=='LT-NO':
        step = 0
        method = 'LT-NO'
    elif meth=="AF":
        step=round(float(step)*1e-3,6)
        method='LT-AF-Z'
    elif meth== 'T':
        step=round(float(step)+273,6)
        method='LT-T-Z'
    elif meth== 'ARM':
        method='LT-AF-I'
        step=round(float(step)*1e-3,6)
    elif meth== 'IRM':
        method='LT-IRM'
        step=round(float(step)*1e-3,6)
    # not supporting susceptibility at the moment LJ
    #elif meth== 'X':
    #    method='LP-X'
    #    pcol+=1
    #    if sys.argv[ind+2]=='mass':
    #        suc_key='measurement_chi_mass'
    #    elif sys.argv[ind+2]=='vol':
    #        suc_key='measurement_chi_volume'
    #    else:
    #        print 'error in susceptibility units'
    #        return False, 'error in susceptibility units'
    else:
       print 'method: {} not supported'.format(meth)
       return False, 'method: "{}" not supported'.format(meth)

    if wt_file:
       norm=True

    if dmin and dmax:
        dmin, dmax = float(dmin), float(dmax)
    else:
        dmin, dmax = -1, -1

    if pltTime:
        amin=float(amin)
        amax=float(amax)
        pcol+=1
        width+=2
        if not (amax and timescale):
            return False, "To plot time, you must provide amin, amax, and timescale"

    #
    #
    # get data read in

    meas_file = os.path.join(input_dir_path, meas_file)
    spc_file = os.path.join(input_dir_path, spc_file)
    if age_file=="":
        samp_file = os.path.join(input_dir_path, samp_file)
        Samps,file_type=pmag.magic_read(samp_file)
    else:
        depth_scale='age'
        age_file = os.path.join(input_dir_path, age_file)
        Samps,file_type=pmag.magic_read(age_file)
        age_unit=""
    if spc_file:
        Specs,file_type=pmag.magic_read(spc_file)
    if res_file:
        Results,file_type=pmag.magic_read(res_file)
    if norm:
        ErSpecs,file_type=pmag.magic_read(wt_file)
        print len(ErSpecs), ' specimens read in from ',wt_file

    if not os.path.isfile(spc_file):
        if not os.path.isfile(meas_file):
            return False, "You must provide either a magic_measurements file or a pmag_specimens file"

    Cores=[]
    core_depth_key="Top depth cored CSF (m)"
    if sum_file:
        sum_file = os.path.join(input_dir_path, sum_file)
        input=open(sum_file,'rU').readlines()
        if "Core Summary" in input[0]:
            headline=1
        else:
            headline=0
        keys=input[headline].replace('\n','').split(',')
        if "Core Top (m)" in keys:
            core_depth_key="Core Top (m)"
        if "Top depth cored CSF (m)" in keys:
            core_dpeth_key="Top depth cored CSF (m)"
        if "Core Label" in keys:
            core_label_key="Core Label"
        if "Core label" in keys:
            core_label_key="Core label"
        for line in input[2:]:
            if 'TOTALS' not in line:
                CoreRec={}
                for k in range(len(keys)):CoreRec[keys[k]]=line.split(',')[k]
                Cores.append(CoreRec)
        if len(Cores)==0:
            print 'no Core depth information available: import core summary file'
            sum_file=""
    Data=[]
    if depth_scale=='sample_core_depth' or depth_scale == 'mbsf':
        ylab="Depth (mbsf)"
        depth_scale='sample_core_depth'
    elif depth_scale=='age':
        ylab="Age"
    elif depth_scale=='sample_composite_depth' or depth_scale=='mcd':
        ylab="Depth (mcd)"
        depth_scale = 'sample_composite_depth'
    else:
        print 'Warning: You have provided unsupported depth scale: {}.\nUsing default (mbsf) instead.'.format(depth_scale)
        depth_scale = 'sample_core_depth'
        ylab="Depth (mbsf)"
    # collect the data for plotting declination
    Depths,Decs,Incs,Ints=[],[],[],[]
    SDepths,SDecs,SIncs,SInts=[],[],[],[]
    SSucs=[]
    samples=[]
    methods,steps,m2=[],[],[]
    if pltSus and os.path.isfile(meas_file): # plot the bulk measurement data
        Meas,file_type=pmag.magic_read(meas_file)
        meas_key='measurement_magn_moment'
        print len(Meas), ' measurements read in from ',meas_file
        for m in intlist: # find the intensity key with data
            meas_data=pmag.get_dictitem(Meas,m,'','F') # get all non-blank data for this specimen
            if len(meas_data)>0:
                meas_key=m
                break
        m1=pmag.get_dictitem(Meas,'magic_method_codes',method,'has') # fish out the desired method code
        if method=='LT-T-Z':
            m2=pmag.get_dictitem(m1,'treatment_temp',str(step),'eval') # fish out the desired step
        elif 'LT-AF' in method:
            m2=pmag.get_dictitem(m1,'treatment_ac_field',str(step),'eval')
        elif 'LT-IRM' in method:
            m2=pmag.get_dictitem(m1,'treatment_dc_field',str(step),'eval')
        elif 'LT-X' in method:
            m2=pmag.get_dictitem(m1,suc_key,'','F')
        if len(m2)>0:
          for rec in m2: # fish out depths and weights
            D=pmag.get_dictitem(Samps,'er_sample_name',rec['er_sample_name'],'T')
            if not D:  # if using an age_file, you may need to sort by site
                D=pmag.get_dictitem(Samps,'er_site_name',rec['er_site_name'],'T')
            depth=pmag.get_dictitem(D,depth_scale,'','F')
            if len(depth)>0:
                if ylab=='Age': ylab=ylab+' ('+depth[0]['age_unit']+')' # get units of ages - assume they are all the same!

                rec['core_depth'] = float(depth[0][depth_scale])
                rec['magic_method_codes'] = rec['magic_method_codes']+':'+depth[0]['magic_method_codes']
                if norm:
                    specrecs=pmag.get_dictitem(ErSpecs,'er_specimen_name',rec['er_specimen_name'],'T')
                    specwts=pmag.get_dictitem(specrecs,'specimen_weight',"",'F')
                    if len(specwts)>0:
                        rec['specimen_weight'] = specwts[0]['specimen_weight']
                        Data.append(rec) # fish out data with core_depth and (if needed) weights
                else:
                    Data.append(rec) # fish out data with core_depth and (if needed) weights
                if title=="":
                   pieces=rec['er_sample_name'].split('-')
                   location=rec['er_location_name']
                   title=location

        SData=pmag.sort_diclist(Data,'core_depth')
        for rec in SData: # fish out bulk measurement data from desired depths
            if dmax==-1 or float(rec['core_depth'])<dmax and float(rec['core_depth'])>dmin:
                Depths.append((rec['core_depth']))
                if method=="LP-X":
                    SSucs.append(float(rec[suc_key]))
                else:
                   if pltDec:
                       Decs.append(float(rec['measurement_dec']))
                   if pltInc:
                       Incs.append(float(rec['measurement_inc']))
                   if not norm and pltMag:
                       Ints.append(float(rec[meas_key]))
                   if norm and pltMag:
                       Ints.append(float(rec[meas_key])/float(rec['specimen_weight']))
            if len(SSucs)>0:
                maxSuc=max(SSucs)
                minSuc=min(SSucs)
            if len(Ints)>1:
                maxInt=max(Ints)
                minInt=min(Ints)
        if len(Depths)==0:
            print 'no bulk measurement data matched your request'
    SpecDepths,SpecDecs,SpecIncs=[],[],[]
    FDepths,FDecs,FIncs=[],[],[]
    if spc_file: # add depths to spec data
        print 'spec file found'
        BFLs=pmag.get_dictitem(Specs,'magic_method_codes','DE-BFL','has')  # get all the discrete data with best fit lines
        for spec in BFLs:
            if location=="":
               location=spec['er_location_name']
            samp=pmag.get_dictitem(Samps,'er_sample_name',spec['er_sample_name'],'T')
            if len(samp)>0 and depth_scale in samp[0].keys() and samp[0][depth_scale]!="":
              if ylab=='Age': ylab=ylab+' ('+samp[0]['age_unit']+')' # get units of ages - assume they are all the same!
              if dmax==-1 or float(samp[0][depth_scale])<dmax and float(samp[0][depth_scale])>dmin: # filter for depth
                SpecDepths.append(float(samp[0][depth_scale])) # fish out data with core_depth
                SpecDecs.append(float(spec['specimen_dec'])) # fish out data with core_depth
                SpecIncs.append(float(spec['specimen_inc'])) # fish out data with core_depth
            else:
                print 'no core_depth found for: ',spec['er_specimen_name']
        FMs=pmag.get_dictitem(Specs,'magic_method_codes','DE-FM','has')  # get all the discrete data with best fit lines
        for spec in FMs:
            if location=="":
               location=spec['er_location_name']
            samp=pmag.get_dictitem(Samps,'er_sample_name',spec['er_sample_name'],'T')
            if len(samp)>0 and depth_scale in samp[0].keys() and samp[0][depth_scale]!="":
              if ylab=='Age': ylab=ylab+' ('+samp[0]['age_unit']+')' # get units of ages - assume they are all the same!
              if dmax==-1 or float(samp[0][depth_scale])<dmax and float(samp[0][depth_scale])>dmin: # filter for depth
                FDepths.append(float(samp[0][depth_scale]))# fish out data with core_depth
                FDecs.append(float(spec['specimen_dec'])) # fish out data with core_depth
                FIncs.append(float(spec['specimen_inc'])) # fish out data with core_depth
            else:
                print 'no core_depth found for: ',spec['er_specimen_name']
    ResDepths,ResDecs,ResIncs=[],[],[]
    if 'age' in depth_scale: # set y-key
        res_scale='average_age'
    else:
        res_scale='average_height'
    if res_file: #creates lists of Result Data
        for res in Results:
            meths=res['magic_method_codes'].split(":")
            if 'DE-FM' in meths:
              if dmax==-1 or float(res[res_scale])<dmax and float(res[res_scale])>dmin: # filter for depth
                ResDepths.append(float(res[res_scale])) # fish out data with core_depth
                ResDecs.append(float(res['average_dec'])) # fish out data with core_depth
                ResIncs.append(float(res['average_inc'])) # fish out data with core_depth
                Susc,Sus_depths=[],[]
    if dmin==-1:
        if len(Depths)>0: dmin,dmax=Depths[0],Depths[-1]
        if len(FDepths)>0: dmin,dmax=FDepths[0],FDepths[-1]
        if pltSus and len(SDepths)>0:
            if SDepths[0]<dmin:dmin=SDepths[0]
            if SDepths[-1]>dmax:dmax=SDepths[-1]
        if len(SpecDepths)>0:
            if min(SpecDepths)<dmin:dmin=min(SpecDepths)
            if max(SpecDepths)>dmax:dmax=max(SpecDepths)
        if len(ResDepths)>0:
            if min(ResDepths)<dmin:dmin=min(ResDepths)
            if max(ResDepths)>dmax:dmax=max(ResDepths)
    if suc_file:
        sucdat=open(suc_file,'rU').readlines()
        keys=sucdat[0].replace('\n','').split(',') # splits on underscores
        for line in sucdat[1:]:
            SucRec={}
            for k in range(len(keys)):SucRec[keys[k]]=line.split(',')[k]
            if float(SucRec['Top Depth (m)'])<dmax and float(SucRec['Top Depth (m)'])>dmin and SucRec['Magnetic Susceptibility (80 mm)']!="":
                Susc.append(float(SucRec['Magnetic Susceptibility (80 mm)']))
                if Susc[-1]>maxSuc:maxSuc=Susc[-1]
                if Susc[-1]<minSuc:minSuc=Susc[-1]
                Sus_depths.append(float(SucRec['Top Depth (m)']))
    WIG,WIG_depths=[],[]
    if wig_file:
        wigdat,file_type=pmag.magic_read(wig_file)
        swigdat=pmag.sort_diclist(wigdat,depth_scale)
        keys=wigdat[0].keys()
        for key in keys:
            if key!=depth_scale:
                plt_key=key
                break
        for wig in swigdat:
            if float(wig[depth_scale])<dmax and float(wig[depth_scale])>dmin:
                WIG.append(float(wig[plt_key]))
                WIG_depths.append(float(wig[depth_scale]))
    tint=4.5
    plot=1
    #print 'Decs', len(Decs), 'Depths', len(Depths), 'SpecDecs', len(SpecDecs), 'SpecDepths', len(SpecDepths), 'ResDecs', len(ResDecs), 'ResDepths', len(ResDepths), 'SDecs', len(SDecs), 'SDepths', len(SDepths), 'SIincs', len(SIncs), 'Incs', len(Incs)
    if (Decs and Depths) or (SpecDecs and SpecDepths) or (ResDecs and ResDepths) or (SDecs and SDepths) or (SInts and SDepths) or (SIncs and SDepths) or (Incs and Depths):
        main_plot = plt.figure(1,figsize=(width,8)) # this works
        #pylab.figure(1,figsize=(width,8))
        version_num=pmag.get_version()
        plt.figtext(.02,.01,version_num)
        if pltDec:
            ax=plt.subplot(1,pcol,plot)
            if pltLine:
                plt.plot(Decs,Depths,'k')
            if len(Decs)>0:
                plt.plot(Decs,Depths,sym,markersize=size)
            if len(Decs)==0 and pltLine and len(SDecs)>0:
                plt.plot(SDecs,SDepths,'k')
            if len(SDecs)>0:
                plt.plot(SDecs,SDepths,Ssym,markersize=Ssize)
            if spc_file:
                plt.plot(SpecDecs,SpecDepths,spc_sym,markersize=spc_size)
            if spc_file and len(FDepths)>0:
                plt.scatter(FDecs,FDepths,marker=spc_sym[-1],edgecolor=spc_sym[0],facecolor='white',s=spc_size**2)
            if res_file:
                plt.plot(ResDecs,ResDepths,res_sym,markersize=res_size)
            if sum_file:
                for core in Cores:
                    depth=float(core[core_depth_key])
                    if depth>dmin and depth<dmax:
                        plt.plot([0,360.],[depth,depth],'b--')
                        if pel==plt:
                            plt.text(360,depth+tint,core[core_label_key])
            if pel==plot:
                plt.axis([0,400,dmax,dmin])
            else:
                plt.axis([0,360.,dmax,dmin])
            plt.xlabel('Declination')
            plt.ylabel(ylab)
            plot+=1
            pmagplotlib.delticks(ax) # dec xticks are too crowded otherwise
    else:
        return False, 'No data found to plot\nTry again with different parameters'
    if pltInc:
            plt.subplot(1,pcol,plot)
            if pltLine:
                plt.plot(Incs,Depths,'k')
            if len(Incs)>0:
                plt.plot(Incs,Depths,sym,markersize=size)
            if len(Incs)==0 and pltLine and len(SIncs)>0:
                plt.plot(SIncs,SDepths,'k')
            if len(SIncs)>0:plt.plot(SIncs,SDepths,Ssym,markersize=Ssize)
            if spc_file and len(SpecDepths)>0:
                plt.plot(SpecIncs,SpecDepths,spc_sym,markersize=spc_size)
            if spc_file and len(FDepths)>0:
                plt.scatter(FIncs,FDepths,marker=spc_sym[-1],edgecolor=spc_sym[0],facecolor='white',s=spc_size**2)
            if res_file:
                plt.plot(ResIncs,ResDepths,res_sym,markersize=res_size)
            if sum_file:
                for core in Cores:
                     depth=float(core[core_depth_key])
                     if depth>dmin and depth<dmax:
                         if pel==plot:
                             plt.text(90,depth+tint,core[core_label_key])
                         plt.plot([-90,90],[depth,depth],'b--')
            plt.plot([0,0],[dmax,dmin],'k-')
            if pel==plot:
                plt.axis([-90,110,dmax,dmin])
            else:
                plt.axis([-90,90,dmax,dmin])
            plt.xlabel('Inclination')
            plt.ylabel('')
            plot+=1
    if pltMag and len(Ints)>0 or len(SInts)>0:
            plt.subplot(1,pcol,plot)
            for pow in range(-10,10):
                if maxInt*10**pow>1:break
            if not logit:
                for k in range(len(Ints)):
                    Ints[k]=Ints[k]*10**pow
                for k in range(len(SInts)):
                    SInts[k]=SInts[k]*10**pow
                if pltLine and len(Ints)>0:
                    plt.plot(Ints,Depths,'k')
                if len(Ints)>0:
                    plt.plot(Ints,Depths,sym,markersize=size)
                if len(Ints)==0 and pltLine and len(SInts)>0:
                    plt.plot(SInts,SDepths,'k-')
                if len(SInts)>0:
                    plt.plot(SInts,SDepths,Ssym,markersize=Ssize)
                if sum_file:
                    for core in Cores:
                         depth=float(core[core_depth_key])
                         plt.plot([0,maxInt*10**pow+.1],[depth,depth],'b--')
                         if depth>dmin and depth<dmax:
                             plt.text(maxInt*10**pow-.2*maxInt*10**pow,depth+tint,core[core_label_key])
                plt.axis([0,maxInt*10**pow+.1,dmax,dmin])
                if not norm:
                    plt.xlabel('%s %i %s'%('Intensity (10^-',pow,' Am^2)'))
                else:
                    plt.xlabel('%s %i %s'%('Intensity (10^-',pow,' Am^2/kg)'))
            else:
                if pltLine:
                    plt.semilogx(Ints,Depths,'k')
                if len(Ints)>0:
                    plt.semilogx(Ints,Depths,sym,markersize=size)
                if len(Ints)==0 and pltLine and len(SInts)>0:
                    plt.semilogx(SInts,SDepths,'k')
                if len(Ints)==0 and pltLine==1 and len(SInts)>0:
                    plt.semilogx(SInts,SDepths,'k')
                if len(SInts)>0:
                    plt.semilogx(SInts,SDepths,Ssym,markersize=Ssize)
                if sum_file:
                    for core in Cores:
                         depth=float(core[core_depth_key])
                         plt.semilogx([minInt,maxInt],[depth,depth],'b--')
                         if depth>dmin and depth<dmax:
                             plt.text(maxInt-.2*maxInt,depth+tint,core[core_label_key])
                plt.axis([0,maxInt,dmax,dmin])
                if not norm:
                    plt.xlabel('Intensity (Am^2)')
                else:
                    plt.xlabel('Intensity (Am^2/kg)')
            plot+=1
    if suc_file or len(SSucs)>0:
            plt.subplot(1,pcol,plot)
            if len(Susc)>0:
                if pltLine:
                    plt.plot(Susc,Sus_depths,'k')
                if not logit:
                    plt.plot(Susc,Sus_depths,sym,markersize=size)
                if logit:
                    plt.semilogx(Susc,Sus_depths,sym,markersize=size)
            if len(SSucs)>0:
                if not logit:
                    plt.plot(SSucs,SDepths,sym,markersize=size)
                if logit:
                    plt.semilogx(SSucs,SDepths,sym,markersize=size)
            if sum_file:
                for core in Cores:
                     depth=float(core[core_depth_key])
                     if not logit:
                         plt.plot([minSuc,maxSuc],[depth,depth],'b--')
                     if logit:
                         plt.semilogx([minSuc,maxSuc],[depth,depth],'b--')
            plt.axis([minSuc,maxSuc,dmax,dmin])
            plt.xlabel('Susceptibility')
            plot+=1
    if wig_file:
            plt.subplot(1,pcol,plot)
            plt.plot(WIG,WIG_depths,'k')
            if sum_file:
                for core in Cores:
                     depth=float(core[core_depth_key])
                     plt.plot([WIG[0],WIG[-1]],[depth,depth],'b--')
            plt.axis([min(WIG),max(WIG),dmax,dmin])
            plt.xlabel(plt_key)
            plot+=1
    if pltTime:
            ax1=plt.subplot(1,pcol,plot)
            ax1.axis([-.25,1.5,amax,amin])
            plot+=1
            TS,Chrons=pmag.get_TS(timescale)
            X,Y,Y2=[0,1],[],[]
            cnt=0
            if amin<TS[1]: # in the Brunhes
                Y=[amin,amin] # minimum age
                Y1=[TS[1],TS[1]] # age of the B/M boundary
                ax1.fill_between(X,Y,Y1,facecolor='black') # color in Brunhes, black
            for d in TS[1:]:
                pol=cnt%2
                cnt+=1
                if d<=amax and d>=amin:
                   ind=TS.index(d)
                   Y=[TS[ind],TS[ind]]
                   Y1=[TS[ind+1],TS[ind+1]]
                   if pol: ax1.fill_between(X,Y,Y1,facecolor='black') # fill in every other time
            ax1.plot([0,1,1,0,0],[amin,amin,amax,amax,amin],'k-')
            ax2=ax1.twinx()
            plt.ylabel("Age (Ma): "+timescale)
            for k in range(len(Chrons)-1):
                c=Chrons[k]
                cnext=Chrons[k+1]
                d=cnext[1]-(cnext[1]-c[1])/3.
                if d>=amin and d<amax:
                    ax2.plot([1,1.5],[c[1],c[1]],'k-') # make the Chron boundary tick
                    ax2.text(1.05,d,c[0]) #
            ax2.axis([-.25,1.5,amax,amin])
    figname=location+'_m:_'+method+'_core-depthplot.'+fmt
    plt.title(location)
    return main_plot, figname


def download_magic(infile, dir_path='.', input_dir_path='.',
                   overwrite=False, print_progress=True,
                   data_model=2.5):
    """
    takes the name of a text file downloaded from the MagIC database and
    unpacks it into magic-formatted files. by default, download_magic assumes
    that you are doing everything in your current directory. if not, you may
    provide optional arguments dir_path (where you want the results to go) and
    input_dir_path (where the downloaded file is).
    """
    if data_model == 2.5:
        method_col = "magic_method_codes"
    else:
        method_col = "method_codes"
    f=open(os.path.join(input_dir_path, infile),'rU')
    infile=f.readlines()
    File=[] # will contain all non-blank lines from downloaded file
    for line in infile:
        line=line.replace('\n','')
        if line[0:4]=='>>>>' or len(line.strip()) > 0:  # skip blank lines
            File.append(line)
    LN=0 # tracks our progress iterating through File
    type_list=[]
    filenum=0
    while LN < len(File) - 1:
        line=File[LN]
        file_type=line.split('\t')[1]
        file_type=file_type.lower()
        if file_type[-1]=="\n":
            file_type=file_type[:-1]
        if print_progress==True:
            print 'working on: ', repr(file_type)
        if file_type not in type_list:
            type_list.append(file_type)
        else:
            filenum+=1
        LN+=1
        line=File[LN]
        keys=line.replace('\n','').split('\t')
        if keys[0][0]=='.':
            keys=line.replace('\n','').replace('.','').split('\t')
            keys.append('RecNo') # cludge for new MagIC download format
        LN+=1
        Recs=[]
        while LN<len(File):
            line=File[LN]
            # finish up one file type and then break
            if ">>>>" in line and len(Recs)>0:
                if filenum==0:
                    outfile=dir_path+"/"+file_type.strip()+'.txt'
                else:
                    outfile=dir_path+"/"+file_type.strip()+'_'+str(filenum)+'.txt'
                NewRecs=[]
                for rec in Recs:
                    if method_col in rec.keys():
                        meths=rec[method_col].split(":")
                        if len(meths)>0:
                            methods=""
                            for meth in meths:
                                methods=methods+meth.strip()+":" # get rid of nasty spaces!!!!!!
                            rec[method_col]=methods[:-1]
                    NewRecs.append(rec)
                pmag.magic_write(outfile,Recs,file_type)
                if print_progress==True:
                    print file_type," data put in ",outfile
                Recs=[]
                LN+=1
                break
            # keep adding records of the same file type
            else:
                rec=line.split('\t')
                Rec={}
                if len(rec)==len(keys):
                    for k in range(len(rec)):
                       Rec[keys[k]]=rec[k]
                    Recs.append(Rec)
                # in case of magic_search_results.txt, which has an extra column:
                elif len(rec) - len(keys) == 1:
                    for k in range(len(rec))[:-1]:
                        Rec[keys[k]]=rec[k]
                        Recs.append(Rec)
                else:
                    print 'WARNING:  problem in file with line: '
                    print line
                    print 'skipping....'
                LN+=1
    if len(Recs)>0:
        if filenum==0:
            outfile=dir_path+"/"+file_type.strip()+'.txt'
        else:
            outfile=dir_path+"/"+file_type.strip()+'_'+str(filenum)+'.txt'
        NewRecs=[]
        for rec in Recs:
            if method_col in rec.keys():
                meths=rec[method_col].split(":")
                if len(meths)>0:
                    methods=""
                    for meth in meths:
                        methods=methods+meth.strip()+":" # get rid of nasty spaces!!!!!!
                    rec[method_col]=methods[:-1]
            NewRecs.append(rec)
        pmag.magic_write(outfile,Recs,file_type)
        if print_progress==True:
            print file_type," data put in ",outfile
    # look through locations table and create separate directories for each location
    locs,locnum=[],1
    if 'locations' in type_list:
        locs,file_type=pmag.magic_read(os.path.join(dir_path, 'locations.txt'))
    if len(locs)>0: # at least one location
        for loc in locs:
            loc_name = loc['location']
            if print_progress==True:
                print 'location_'+str(locnum)+": ", loc_name
            lpath=dir_path+'/Location_'+str(locnum)
            locnum+=1
            try:
                os.mkdir(lpath)
            except:
                print 'directory ',lpath,' already exists - overwriting everything: {}'.format(overwrite)
                if not overwrite:
                    print "-W- download_magic encountered a duplicate subdirectory ({}) and could not finish.\nRerun with overwrite=True, or unpack this file in a different directory.".format(lpath)
                    return False
            for f in type_list:
                if print_progress==True:
                    print 'unpacking: ',dir_path+'/'+f+'.txt'
                recs,file_type=pmag.magic_read(dir_path+'/'+f+'.txt')
                if print_progress==True:
                    print len(recs),' read in'
                lrecs=pmag.get_dictitem(recs, 'location', loc_name, 'T')
                if len(lrecs)>0:
                    pmag.magic_write(lpath+'/'+f+'.txt',lrecs,file_type)
                    if print_progress==True:
                        print len(lrecs),' stored in ',lpath+'/'+f+'.txt'
    return True


def upload_magic(concat=0, dir_path='.', data_model=None):
    """
    Finds all magic files in a given directory, and compiles them into an upload.txt file which can be uploaded into the MagIC database.
    returns a tuple of either: (False, error_message, errors) if there was a problem creating/validating the upload file
    or: (filename, '', None) if the upload was fully successful
    """
    SpecDone=[]
    locations = []
    concat = int(concat)
    files_list = ["er_expeditions.txt", "er_locations.txt", "er_samples.txt", "er_specimens.txt", "er_sites.txt", "er_ages.txt", "er_citations.txt", "er_mailinglist.txt", "magic_measurements.txt", "rmag_hysteresis.txt", "rmag_anisotropy.txt", "rmag_remanence.txt", "rmag_results.txt", "pmag_specimens.txt", "pmag_samples.txt", "pmag_sites.txt", "pmag_results.txt", "pmag_criteria.txt", "magic_instruments.txt"]
    file_names = [os.path.join(dir_path, f) for f in files_list]

    # begin the upload process
    up = os.path.join(dir_path, "upload.txt")
    if os.path.exists(up):
        os.remove(up)
    RmKeys = ['citation_label', 'compilation', 'calculation_type', 'average_n_lines', 'average_n_planes',
              'specimen_grade', 'site_vgp_lat', 'site_vgp_lon', 'direction_type', 'specimen_Z',
              'magic_instrument_codes', 'cooling_rate_corr', 'cooling_rate_mcd', 'anisotropy_atrm_alt',
              'anisotropy_apar_perc', 'anisotropy_F', 'anisotropy_F_crit', 'specimen_scat',
              'specimen_gmax','specimen_frac', 'site_vadm', 'site_lon', 'site_vdm', 'site_lat',
              'measurement_chi', 'specimen_k_prime','specimen_k_prime_sse','external_database_names',
              'external_database_ids', 'Further Notes', 'Typology', 'Notes (Year/Area/Locus/Level)',
              'Site', 'Object Number']
    print "-I- Removing: ", RmKeys
    CheckDec = ['_dec', '_lon', '_azimuth', 'dip_direction']
    CheckSign = ['specimen_b_beta']
    last = file_names[-1]
    methods, first_file = [], 1
    for File in file_names:
    # read in the data
        Data,file_type=pmag.magic_read(File)
        if file_type!="bad_file":
            print "-I- file", File, " successfully read in"
            if len(RmKeys)>0:
                for rec in Data:
                    # remove unwanted keys
                    for key in RmKeys:
                        if key=='specimen_Z' and key in rec.keys():
                            rec[key]='specimen_z' # change  # change this to lower case
                        if key in rec.keys():
                            del rec[key] # get rid of unwanted keys
                    # make sure b_beta is positive
                    if 'specimen_b_beta' in rec.keys() and rec['specimen_b_beta']!="": # ignore blanks
                        if float(rec['specimen_b_beta'])< 0:
                            rec['specimen_b_beta']=str(-float(rec['specimen_b_beta']))  # make sure value is positive
                            print '-I- adjusted to positive: ','specimen_b_beta',rec['specimen_b_beta']
                    # make all declinations/azimuths/longitudes in range 0=>360.
                    rec = pmag.adjust_all_to_360(rec)
            if file_type=='er_locations':
                for rec in Data:
                    locations.append(rec['er_location_name'])
            if file_type in ['pmag_samples', 'pmag_sites', 'pmag_specimens']:
                # if there is NO pmag data for specimens (samples/sites),
                # do not try to write it to file
                # (this causes validation errors, elsewise)
                ignore = True
                for rec in Data:
                    if ignore == False:
                        break
                    keys = rec.keys()
                    exclude_keys = ['er_citation_names', 'er_site_name', 'er_sample_name',
                                    'er_location_name', 'er_specimen_names', 'er_sample_names']
                    for key in exclude_keys:
                        if key in keys:
                            keys.remove(key)
                    for key in keys:
                        if rec[key]:
                            ignore = False
                            break
                if ignore:
                    continue

            if file_type=='er_samples': # check to only upload top priority orientation record!
                NewSamps,Done=[],[]
                for rec in Data:
                    if rec['er_sample_name'] not in Done:
                        orient,az_type=pmag.get_orient(Data,rec['er_sample_name'])
                        NewSamps.append(orient)
                        Done.append(rec['er_sample_name'])
                Data=NewSamps
                print 'only highest priority orientation record from er_samples.txt read in '
            if file_type=='er_specimens': #  only specimens that have sample names
                NewData,SpecDone=[],[]
                for rec in Data:
                    if rec['er_sample_name'] in Done:
                        NewData.append(rec)
                        SpecDone.append(rec['er_specimen_name'])
                    else:
                        print 'no valid sample record found for: '
                        print rec
                Data=NewData
                #print 'only measurements that have specimen/sample info'
            if file_type=='magic_measurements': #  only measurements that have specimen names
                no_specs = []
                NewData=[]
                for rec in Data:
                    if rec['er_specimen_name'] in SpecDone:
                        NewData.append(rec)
                    else:
                        print 'no valid specimen record found for: '
                        print rec
                        no_specs.append(rec)
                #print set([record['er_specimen_name'] for record in no_specs])
                Data = NewData
    # write out the data
            if len(Data) > 0:
                if first_file == 1:
                    keystring = pmag.first_rec(up,Data[0],file_type)
                    first_file = 0
                else:
                    keystring = pmag.first_up(up,Data[0],file_type)
                for rec in Data:
    # collect the method codes
                    if "magic_method_codes" in rec.keys():
                        meths = rec["magic_method_codes"].split(':')
                        for meth in meths:
                            if meth.strip() not in methods:
                                if meth.strip() != "LP-DIR-":
                                    methods.append(meth.strip())
                    try:
                        pmag.putout(up,keystring,rec)
                    except IOError:
                        print '-W- File input error: slowing down'
                        time.sleep(1)
                        pmag.putout(up, keystring, rec)

    # write out the file separator
            f=open(up,'a')
            f.write('>>>>>>>>>>\n')
            f.close()
            print file_type, 'written to ',up
        else:
            print 'File:', File
            print file_type, 'is bad or non-existent - skipping '

    # write out the methods table
    first_rec,MethRec=1,{}
    for meth in methods:
        MethRec["magic_method_code"]=meth
        if first_rec==1:meth_keys=pmag.first_up(up,MethRec,"magic_methods")
        first_rec=0
        try:
            pmag.putout(up,meth_keys,MethRec)
        except IOError:
            print '-W- File input error: slowing down'
            time.sleep(1)
            pmag.putout(up,meth_keys,MethRec)
    if concat==1:
        f=open(up,'a')
        f.write('>>>>>>>>>>\n')
        f.close()


    if os.path.isfile(up):
        import validate_upload2 as validate_upload
        validated = False
        validated, errors = validate_upload.read_upload(up, data_model)

    else:
        print "no data found, upload file not created"
        return False, "no data found, upload file not created", None

    #rename upload.txt according to location + timestamp
    format_string = "%d.%b.%Y"
    if locations:
        location = locations[0].replace(' ', '_')
        new_up = location + '_' + time.strftime(format_string) + '.txt'
    else:
        new_up = 'unknown_location_' + time.strftime(format_string) + '.txt'

    new_up = os.path.join(dir_path, new_up)
    if os.path.isfile(new_up):
        fname, extension = os.path.splitext(new_up)
        for i in range(1, 100):
            if os.path.isfile(fname + "_" + str(i) + extension):
                continue
            else:
                new_up = fname + "_" + str(i) + extension
                break
    os.rename(up, new_up)
    print "Finished preparing upload file: {} ".format(new_up)
    if not validated:
        print "-W- validation of upload file has failed.\nPlease fix above errors and try again.\nYou may run into problems if you try to upload this file to the MagIC database"
        return False, "file validation has failed.  You may run into problems if you try to upload this file.", errors
    return new_up, '', None

def upload_magic3(concat=0, dir_path='.', dmodel=None, vocab=""):
    """
    Finds all magic files in a given directory,
    and compiles them into an upload.txt file
    which can be uploaded into the MagIC database.
    returns a tuple of either: (False, error_message, errors)
    if there was a problem creating/validating the upload file
    or: (filename, '', None) if the file creation was fully successful.
    """
    locations = []
    concat = int(concat)
    dtypes = ["locations", "samples", "specimens", "sites", "ages", "measurements",
                  "criteria", "contribution", "images"]
    file_names = [os.path.join(dir_path, dtype + ".txt") for dtype in dtypes]
    con = Contribution(dir_path, vocabulary=vocab)
    # begin the upload process
    up = os.path.join(dir_path, "upload.txt")
    if os.path.exists(up):
        os.remove(up)
    RmKeys = ['citation_label', 'compilation', 'calculation_type', 'average_n_lines', 'average_n_planes',
              'specimen_grade', 'site_vgp_lat', 'site_vgp_lon', 'direction_type', 'specimen_Z',
              'magic_instrument_codes', 'cooling_rate_corr', 'cooling_rate_mcd', 'anisotropy_atrm_alt',
              'anisotropy_apar_perc', 'anisotropy_F', 'anisotropy_F_crit', 'specimen_scat',
              'specimen_gmax','specimen_frac', 'site_vadm', 'site_lon', 'site_vdm', 'site_lat',
              'measurement_chi', 'specimen_k_prime','specimen_k_prime_sse','external_database_names',
              'external_database_ids', 'Further Notes', 'Typology', 'Notes (Year/Area/Locus/Level)',
              'Site', 'Object Number']
    print "-I- Removing: ", RmKeys
    last = file_names[-1]
    first_file = 1
    failing = []
    all_failing_items = {}
    if not dmodel:
        dmodel = data_model.DataModel()
    for file_type in dtypes:
        print "-"
    # read in the data
        #Data, file_type = pmag.magic_read(File)
        if file_type not in con.tables.keys():
            print "-I- No {} file found, continuing".format(file_type)
            continue
        container = con.tables[file_type]
        df = container.df
        if len(df):
            print "-I- {} file successfully read in".format(file_type)
    # make some adjustments to clean up data
            # drop non MagIC keys
            DropKeys = set(RmKeys).intersection(df.columns)
            df.drop(DropKeys, axis=1, inplace=True)
            # make sure int_b_beta is positive
            if 'int_b_beta' in df.columns:
                df['int_b_beta'] = df['int_b_beta'].astype(float).apply(abs)
            # make all declinations/azimuths/longitudes in range 0=>360.
            relevant_cols = val_up3.get_degree_cols(df)
            for col in relevant_cols:
                df[col] = df[col].apply(pmag.adjust_val_to_360)
            # get list of location names
            if file_type == 'locations':
                locations = sorted(df['location'].unique())
            # LJ: need to deal with this
            # use only highest priority orientation -- not sure how this works
            elif file_type == 'samples':
                #orient,az_type=pmag.get_orient(Data,rec['sample'])
                pass
            # include only specimen records with samples
            elif file_type == 'specimens':
                df = df[df['sample'].notnull()]
                if 'samples' in con.tables:
                    samp_df = con.tables['samples'].df
                    df = df[df['sample'].isin(samp_df.index.unique())]
            # include only measurements with specmiens
            elif file_type == 'measurements':
                df = df[df['specimen'].notnull()]
                if 'specimens' in con.tables:
                    spec_df = con.tables['specimens'].df
                    df = df[df['specimen'].isin(spec_df.index.unique())]
    # run validations
            res = val_up3.validate_table(con, file_type)#, verbose=True)
            if res:
                dtype, bad_rows, bad_cols, missing_cols, missing_groups, failing_items = res
                if dtype not in all_failing_items:
                    all_failing_items[dtype] = {}
                all_failing_items[dtype]["rows"] = failing_items
                all_failing_items[dtype]["missing_columns"] = missing_cols
                all_failing_items[dtype]["missing_groups"] = missing_groups
                failing.append(dtype)
    # write out the data
            if len(df):
                container.write_magic_file(up, append=True)
    # write out the file separator
            f = open(up, 'a')
            f.write('>>>>>>>>>>\n')
            f.close()
            print "-I-", file_type, 'written to ',up
        else:
            #print 'File:', File
            print file_type, 'is bad or non-existent - skipping '
    ## add to existing file
    if concat == 1:
        f = open(up, 'a')
        f.write('>>>>>>>>>>\n')
        f.close()

    if not os.path.isfile(up):
        print "no data found, upload file not created"
        return False, "no data found, upload file not created", None

    #rename upload.txt according to location + timestamp
    format_string = "%d.%b.%Y"
    if locations:
        locs = set(locations)
        locs = sorted(locs)[:3]
        #location = locations[0].replace(' ', '_')
        locs = [loc.replace(' ', '-') for loc in locs]
        location = "_".join(locs)
        new_up = location + '_' + time.strftime(format_string) + '.txt'
    else:
        new_up = 'unknown_location_' + time.strftime(format_string) + '.txt'

    new_up = os.path.join(dir_path, new_up)
    if os.path.isfile(new_up):
        fname, extension = os.path.splitext(new_up)
        for i in range(1, 100):
            if os.path.isfile(fname + "_" + str(i) + extension):
                continue
            else:
                new_up = fname + "_" + str(i) + extension
                break
    if not up:
        print "-W- Could not create an upload file"
        return False, "Could not create an upload file", None, None
    os.rename(up, new_up)
    print "Finished preparing upload file: {} ".format(new_up)
    if failing:
        print "-W- validation of upload file has failed."
        print "These tables have errors: {}".format(", ".join(failing))
        print "Please fix above errors and try again."
        print "You may run into problems if you try to upload this file to the MagIC database."
        return False, "file validation has failed.  You may run into problems if you try to upload this file.", failing, all_failing_items
    else:
        print "-I- Your file has passed validation.  You should be able to upload it to the MagIC database without trouble!"
    return new_up, '', None, None


def specimens_results_magic(infile='pmag_specimens.txt', measfile='magic_measurements.txt', sampfile='er_samples.txt', sitefile='er_sites.txt', agefile='er_ages.txt', specout='er_specimens.txt', sampout='pmag_samples.txt', siteout='pmag_sites.txt', resout='pmag_results.txt', critout='pmag_criteria.txt', instout='magic_instruments.txt', plotsites = False, fmt='svg', dir_path='.', cors=[], priorities=['DA-AC-ARM','DA-AC-TRM'], coord='g', user='', vgps_level='site', do_site_intensity=True, DefaultAge=["none"], avg_directions_by_sample=False, avg_intensities_by_sample=False, avg_all_components=False, avg_by_polarity=False, skip_directions=False, skip_intensities=False, use_sample_latitude=False, use_paleolatitude=False, use_criteria='default'):
    """
    Writes magic_intruments, er_specimens, pmag_samples, pmag_sites, pmag_criteria, and pmag_results. The data used to write this is obtained by reading a pmag_speciemns, a magic_measurements, a er_samples, a er_sites, a er_ages.
    @param -> infile: path from the WD to the pmag speciemns table
    @param -> measfile: path from the WD to the magic measurement file
    @param -> sampfile: path from the WD to the er sample file
    @param -> sitefile: path from the WD to the er sites data file
    @param -> agefile: path from the WD to the er ages data file
    @param -> specout: path from the WD to the place to write the er specimens data file
    @param -> sampout: path from the WD to the place to write the pmag samples data file
    @param -> siteout: path from the WD to the place to write the pmag sites data file
    @param -> resout: path from the WD to the place to write the pmag results data file
    @param -> critout: path from the WD to the place to write the pmag criteria file
    @param -> instout: path from th WD to the place to write the magic instruments file
    @param -> documentation incomplete if you know more about the purpose of the parameters in this function and it's side effects please extend and complete this string
    """
    # initialize some variables
    plotsites=False # cannot use drawFIGS from within ipmag
    Comps=[] # list of components
    version_num=pmag.get_version()
    args=sys.argv
    model_lat_file=""
    Dcrit,Icrit,nocrit=0,0,0
    corrections=[]
    nocorrection=['DA-NL','DA-AC','DA-CR']

    # do some data adjustments
    for cor in cors:
        nocorrection.remove('DA-'+cor)
        corrections.append('DA-'+cor)

    for p in priorities:
        if not p.startswith('DA-AC-'):
            p='DA-AC-'+p

    # translate coord into coords
    if coord=='s':coords=['-1']
    if coord=='g':coords=['0']
    if coord=='t':coords=['100']
    if coord=='b':coords=['0','100']

    if vgps_level == 'sample':
        vgps=1 # save sample level VGPS/VADMs
    else:
        vgps = 0 # site level

    if do_site_intensity:
        nositeints=0
    else:
        nositeints=1

    # chagne these all to True/False instead of 1/0

    if not skip_intensities:
        # set model lat and
        if use_sample_latitude and use_paleolatitude:
            print "you should set a paleolatitude file OR use present day lat - not both"
            return False
        elif use_sample_latitude:
            get_model_lat = 1
        elif use_paleolatitude:
            get_model_lat = 2
            try:
                model_lat_file=dir_path+'/'+args[ind+1]
                get_model_lat=2
                mlat=open(model_lat_file,'rU')
                ModelLats=[]
                for line in mlat.readlines():
                    ModelLat={}
                    tmp=line.split()
                    ModelLat["er_site_name"]=tmp[0]
                    ModelLat["site_model_lat"]=tmp[1]
                    ModelLat["er_sample_name"]=tmp[0]
                    ModelLat["sample_lat"]=tmp[1]
                    ModelLats.append(ModelLat)
            except:
                print "use_paleolatitude option requires a valid paleolatitude file"
        else:
            get_model_lat = 0 # skips VADM calculation entirely


    if plotsites and not skip_directions: # plot by site - set up plot window
        import pmagplotlib
        EQ={}
        EQ['eqarea']=1
        pmagplotlib.plot_init(EQ['eqarea'],5,5) # define figure 1 as equal area projection
        pmagplotlib.plotNET(EQ['eqarea']) # I don't know why this has to be here, but otherwise the first plot never plots...
        pmagplotlib.drawFIGS(EQ)

    infile = os.path.join(dir_path, infile)
    measfile = os.path.join(dir_path, measfile)
    instout = os.path.join(dir_path, instout)
    sampfile = os.path.join(dir_path, sampfile)
    sitefile = os.path.join(dir_path, sitefile)
    agefile = os.path.join(dir_path, agefile)
    specout = os.path.join(dir_path, specout)
    sampout = os.path.join(dir_path, sampout)
    siteout = os.path.join(dir_path, siteout)
    resout = os.path.join(dir_path, resout)
    critout = os.path.join(dir_path, critout)



    if use_criteria == 'none':
        Dcrit,Icrit,nocrit=1,1,1 # no selection criteria
        crit_data=pmag.default_criteria(nocrit)
    elif use_criteria == 'default':
        crit_data=pmag.default_criteria(nocrit) # use default criteria
    elif use_criteria == 'existing':
        crit_data,file_type=pmag.magic_read(critout) # use pmag_criteria file
        print "Acceptance criteria read in from ", critout
    accept={}
    for critrec in crit_data:
        for key in critrec.keys():
# need to migrate specimen_dang to specimen_int_dang for intensity data using old format
            if 'IE-SPEC' in critrec.keys() and 'specimen_dang' in critrec.keys() and 'specimen_int_dang' not in critrec.keys():
                critrec['specimen_int_dang']=critrec['specimen_dang']
                del critrec['specimen_dang']
# need to get rid of ron shaars sample_int_sigma_uT
            if 'sample_int_sigma_uT' in critrec.keys():
                critrec['sample_int_sigma']='%10.3e'%(eval(critrec['sample_int_sigma_uT'])*1e-6)
            if key not in accept.keys() and critrec[key]!='':
                accept[key]=critrec[key]

    if use_criteria == 'default':
        pmag.magic_write(critout,[accept],'pmag_criteria')
        print "\n Pmag Criteria stored in ",critout,'\n'

# now we're done slow dancing

    SiteNFO,file_type=pmag.magic_read(sitefile) # read in site data - has the lats and lons
    SampNFO,file_type=pmag.magic_read(sampfile) # read in site data - has the lats and lons
    height_nfo=pmag.get_dictitem(SiteNFO,'site_height','','F') # find all the sites with height info.
    if agefile:
        AgeNFO,file_type=pmag.magic_read(agefile) # read in the age information
    Data,file_type=pmag.magic_read(infile) # read in specimen interpretations
    IntData=pmag.get_dictitem(Data,'specimen_int','','F') # retrieve specimens with intensity data
    comment,orient="",[]
    samples,sites=[],[]
    for rec in Data: # run through the data filling in missing keys and finding all components, coordinates available
# fill in missing fields, collect unique sample and site names
        if 'er_sample_name' not in rec.keys():
            rec['er_sample_name']=""
        elif rec['er_sample_name'] not in samples:
            samples.append(rec['er_sample_name'])
        if 'er_site_name' not in rec.keys():
            rec['er_site_name']=""
        elif rec['er_site_name'] not in sites:
            sites.append(rec['er_site_name'])
        if 'specimen_int' not in rec.keys():rec['specimen_int']=''
        if 'specimen_comp_name' not in rec.keys() or rec['specimen_comp_name']=="":rec['specimen_comp_name']='A'
        if rec['specimen_comp_name'] not in Comps:Comps.append(rec['specimen_comp_name'])
        rec['specimen_tilt_correction']=rec['specimen_tilt_correction'].strip('\n')
        if "specimen_tilt_correction" not in rec.keys(): rec["specimen_tilt_correction"]="-1" # assume sample coordinates
        if rec["specimen_tilt_correction"] not in orient: orient.append(rec["specimen_tilt_correction"])  # collect available coordinate systems
        if "specimen_direction_type" not in rec.keys(): rec["specimen_direction_type"]='l'  # assume direction is line - not plane
        if "specimen_dec" not in rec.keys(): rec["specimen_direction_type"]=''  # if no declination, set direction type to blank
        if "specimen_n" not in rec.keys(): rec["specimen_n"]=''  # put in n
        if "specimen_alpha95" not in rec.keys(): rec["specimen_alpha95"]=''  # put in alpha95
        if "magic_method_codes" not in rec.keys(): rec["magic_method_codes"]=''
     # start parsing data into SpecDirs, SpecPlanes, SpecInts
    SpecInts,SpecDirs,SpecPlanes=[],[],[]
    samples.sort() # get sorted list of samples and sites
    sites.sort()
    if not skip_intensities: # don't skip intensities
        IntData=pmag.get_dictitem(Data,'specimen_int','','F') # retrieve specimens with intensity data
        if nocrit==0: # use selection criteria
            for rec in IntData: # do selection criteria
                kill=pmag.grade(rec,accept,'specimen_int')
                if len(kill)==0: SpecInts.append(rec) # intensity record to be included in sample, site calculations
        else:
            SpecInts=IntData[:] # take everything - no selection criteria
# check for required data adjustments
        if len(corrections)>0 and len(SpecInts)>0:
            for cor in corrections:
                SpecInts=pmag.get_dictitem(SpecInts,'magic_method_codes',cor,'has') # only take specimens with the required corrections
        if len(nocorrection)>0 and len(SpecInts)>0:
            for cor in nocorrection:
                SpecInts=pmag.get_dictitem(SpecInts,'magic_method_codes',cor,'not') # exclude the corrections not specified for inclusion
# take top priority specimen of its name in remaining specimens (only one per customer)
        PrioritySpecInts=[]
        specimens=pmag.get_specs(SpecInts) # get list of uniq specimen names
        for spec in specimens:
            ThisSpecRecs=pmag.get_dictitem(SpecInts,'er_specimen_name',spec,'T') # all the records for this specimen
            if len(ThisSpecRecs)==1:
                PrioritySpecInts.append(ThisSpecRecs[0])
            elif len(ThisSpecRecs)>1: # more than one
                prec=[]
                for p in priorities:
                    ThisSpecRecs=pmag.get_dictitem(SpecInts,'magic_method_codes',p,'has') # all the records for this specimen
                    if len(ThisSpecRecs)>0:prec.append(ThisSpecRecs[0])
                PrioritySpecInts.append(prec[0]) # take the best one
        SpecInts=PrioritySpecInts # this has the first specimen record
    if not skip_directions: # don't skip directions
        AllDirs=pmag.get_dictitem(Data,'specimen_direction_type','','F') # retrieve specimens with directed lines and planes
        Ns=pmag.get_dictitem(AllDirs,'specimen_n','','F')  # get all specimens with specimen_n information
        if nocrit!=1: # use selection criteria
            for rec in Ns: # look through everything with specimen_n for "good" data
                    kill=pmag.grade(rec,accept,'specimen_dir')
                    if len(kill)==0: # nothing killed it
                        SpecDirs.append(rec)
        else: # no criteria
            SpecDirs=AllDirs[:] # take them all
# SpecDirs is now the list of all specimen directions (lines and planes) that pass muster
    PmagSamps,SampDirs=[],[] # list of all sample data and list of those that pass the DE-SAMP criteria
    PmagSites,PmagResults=[],[] # list of all site data and selected results
    SampInts=[]
    for samp in samples: # run through the sample names
        if avg_directions_by_sample: #  average by sample if desired
           SampDir=pmag.get_dictitem(SpecDirs,'er_sample_name',samp,'T') # get all the directional data for this sample
           if len(SampDir)>0: # there are some directions
               for coord in coords: # step through desired coordinate systems
                   CoordDir=pmag.get_dictitem(SampDir,'specimen_tilt_correction',coord,'T') # get all the directions for this sample
                   if len(CoordDir)>0: # there are some with this coordinate system
                       if not avg_all_components: # look component by component
                           for comp in Comps:
                               CompDir=pmag.get_dictitem(CoordDir,'specimen_comp_name',comp,'T') # get all directions from this component
                               if len(CompDir)>0: # there are some
                                   PmagSampRec=pmag.lnpbykey(CompDir,'sample','specimen') # get a sample average from all specimens
                                   PmagSampRec["er_location_name"]=CompDir[0]['er_location_name'] # decorate the sample record
                                   PmagSampRec["er_site_name"]=CompDir[0]['er_site_name']
                                   PmagSampRec["er_sample_name"]=samp
                                   PmagSampRec["er_citation_names"]="This study"
                                   PmagSampRec["er_analyst_mail_names"]=user
                                   PmagSampRec['magic_software_packages']=version_num
                                   if CompDir[0]['specimen_flag']=='g':
                                        PmagSampRec['sample_flag']='g'
                                   else: PmagSampRec['sample_flag']='b'
                                   if nocrit!=1:PmagSampRec['pmag_criteria_codes']="ACCEPT"
                                   if agefile != "": PmagSampRec= pmag.get_age(PmagSampRec,"er_site_name","sample_inferred_",AgeNFO,DefaultAge)
                                   site_height=pmag.get_dictitem(height_nfo,'er_site_name',PmagSampRec['er_site_name'],'T')
                                   if len(site_height)>0:PmagSampRec["sample_height"]=site_height[0]['site_height'] # add in height if available
                                   PmagSampRec['sample_comp_name']=comp
                                   PmagSampRec['sample_tilt_correction']=coord
                                   PmagSampRec['er_specimen_names']= pmag.get_list(CompDir,'er_specimen_name') # get a list of the specimen names used
                                   PmagSampRec['magic_method_codes']= pmag.get_list(CompDir,'magic_method_codes') # get a list of the methods used
                                   if nocrit!=1: # apply selection criteria
                                       kill=pmag.grade(PmagSampRec,accept,'sample_dir')
                                   else:
                                       kill=[]
                                   if len(kill)==0:
                                        SampDirs.append(PmagSampRec)
                                        if vgps==1: # if sample level VGP info desired, do that now
                                            PmagResRec=pmag.getsampVGP(PmagSampRec,SiteNFO)
                                            if PmagResRec!="":
                                                PmagResults.append(PmagResRec)
#                                   print(PmagSampRec)
                                   PmagSamps.append(PmagSampRec)
                       if avg_all_components: # average all components together  basically same as above
                           PmagSampRec=pmag.lnpbykey(CoordDir,'sample','specimen')
                           PmagSampRec["er_location_name"]=CoordDir[0]['er_location_name']
                           PmagSampRec["er_site_name"]=CoordDir[0]['er_site_name']
                           PmagSampRec["er_sample_name"]=samp
                           PmagSampRec["er_citation_names"]="This study"
                           PmagSampRec["er_analyst_mail_names"]=user
                           PmagSampRec['magic_software_packages']=version_num
                           if all(i['specimen_flag']=='g' for i in CoordDir):
                                PmagSampRec['sample_flag']='g'
                           else: PmagSampRec['sample_flag']='b'
                           if nocrit!=1:PmagSampRec['pmag_criteria_codes']=""
                           if agefile != "": PmagSampRec= pmag.get_age(PmagSampRec,"er_site_name","sample_inferred_",AgeNFO,DefaultAge)
                           site_height=pmag.get_dictitem(height_nfo,'er_site_name',site,'T')
                           if len(site_height)>0:PmagSampRec["sample_height"]=site_height[0]['site_height'] # add in height if available
                           PmagSampRec['sample_tilt_correction']=coord
                           PmagSampRec['sample_comp_name']= pmag.get_list(CoordDir,'specimen_comp_name') # get components used
                           PmagSampRec['er_specimen_names']= pmag.get_list(CoordDir,'er_specimen_name') # get specimne names averaged
                           PmagSampRec['magic_method_codes']= pmag.get_list(CoordDir,'magic_method_codes') # assemble method codes
                           if nocrit!=1: # apply selection criteria
                               kill=pmag.grade(PmagSampRec,accept,'sample_dir')
                               if len(kill)==0: # passes the mustard
                                   SampDirs.append(PmagSampRec)
                                   if vgps==1:
                                       PmagResRec=pmag.getsampVGP(PmagSampRec,SiteNFO)
                                       if PmagResRec!="":
                                           PmagResults.append(PmagResRec)
                           else: # take everything
                               SampDirs.append(PmagSampRec)
                               if vgps==1:
                                   PmagResRec=pmag.getsampVGP(PmagSampRec,SiteNFO)
                                   if PmagResRec!="":
                                       PmagResults.append(PmagResRec)
                           PmagSamps.append(PmagSampRec)
        if avg_intensities_by_sample: #  average by sample if desired
           SampI=pmag.get_dictitem(SpecInts,'er_sample_name',samp,'T') # get all the intensity data for this sample
           if len(SampI)>0: # there are some
               PmagSampRec=pmag.average_int(SampI,'specimen','sample') # get average intensity stuff
               PmagSampRec["sample_description"]="sample intensity" # decorate sample record
               PmagSampRec["sample_direction_type"]=""
               PmagSampRec['er_site_name']=SampI[0]["er_site_name"]
               PmagSampRec['er_sample_name']=samp
               PmagSampRec['er_location_name']=SampI[0]["er_location_name"]
               PmagSampRec["er_citation_names"]="This study"
               PmagSampRec["er_analyst_mail_names"]=user
               if agefile != "":   PmagSampRec=pmag.get_age(PmagSampRec,"er_site_name","sample_inferred_", AgeNFO,DefaultAge)
               site_height=pmag.get_dictitem(height_nfo,'er_site_name',PmagSampRec['er_site_name'],'T')
               if len(site_height)>0:PmagSampRec["sample_height"]=site_height[0]['site_height'] # add in height if available
               PmagSampRec['er_specimen_names']= pmag.get_list(SampI,'er_specimen_name')
               PmagSampRec['magic_method_codes']= pmag.get_list(SampI,'magic_method_codes')
               if nocrit!=1:  # apply criteria!
                   kill=pmag.grade(PmagSampRec,accept,'sample_int')
                   if len(kill)==0:
                       PmagSampRec['pmag_criteria_codes']="ACCEPT"
                       SampInts.append(PmagSampRec)
                       PmagSamps.append(PmagSampRec)
                   else:PmagSampRec={} # sample rejected
               else: # no criteria
                   SampInts.append(PmagSampRec)
                   PmagSamps.append(PmagSampRec)
                   PmagSampRec['pmag_criteria_codes']=""
               if vgps==1 and get_model_lat!=0 and PmagSampRec!={}: #
                  if get_model_lat==1: # use sample latitude
                      PmagResRec=pmag.getsampVDM(PmagSampRec,SampNFO)
                      del(PmagResRec['model_lat']) # get rid of the model lat key
                  elif get_model_lat==2: # use model latitude
                      PmagResRec=pmag.getsampVDM(PmagSampRec,ModelLats)
                      if PmagResRec!={}:PmagResRec['magic_method_codes']=PmagResRec['magic_method_codes']+":IE-MLAT"
                  if PmagResRec!={}:
                      PmagResRec['er_specimen_names']=PmagSampRec['er_specimen_names']
                      PmagResRec['er_sample_names']=PmagSampRec['er_sample_name']
                      PmagResRec['pmag_criteria_codes']='ACCEPT'
                      PmagResRec['average_int_sigma_perc']=PmagSampRec['sample_int_sigma_perc']
                      PmagResRec['average_int_sigma']=PmagSampRec['sample_int_sigma']
                      PmagResRec['average_int_n']=PmagSampRec['sample_int_n']
                      PmagResRec['vadm_n']=PmagSampRec['sample_int_n']
                      PmagResRec['data_type']='i'
                      PmagResults.append(PmagResRec)
    if len(PmagSamps)>0:
        TmpSamps,keylist=pmag.fillkeys(PmagSamps) # fill in missing keys from different types of records
        pmag.magic_write(sampout,TmpSamps,'pmag_samples') # save in sample output file
        print ' sample averages written to ',sampout

#
#create site averages from specimens or samples as specified
#
    for site in sites:
        for coord in coords:
            if not avg_directions_by_sample: key,dirlist='specimen',SpecDirs # if specimen averages at site level desired
            if avg_directions_by_sample: key,dirlist='sample',SampDirs # if sample averages at site level desired
            tmp=pmag.get_dictitem(dirlist,'er_site_name',site,'T') # get all the sites with  directions
            tmp1=pmag.get_dictitem(tmp,key+'_tilt_correction',coord,'T') # use only the last coordinate if avg_all_components==False
            sd=pmag.get_dictitem(SiteNFO,'er_site_name',site,'T') # fish out site information (lat/lon, etc.)
            if len(sd)>0:
                sitedat=sd[0]
                if not avg_all_components: # do component wise averaging
                    for comp in Comps:
                        siteD=pmag.get_dictitem(tmp1,key+'_comp_name',comp,'T') # get all components comp
                        #remove bad data from means
                        siteD=filter(lambda x: x['specimen_flag']=='g' if 'specimen_flag' in x else True , siteD)
                        siteD=filter(lambda x: x['sample_flag']=='g' if 'sample_flag' in x else True , siteD)
                        if len(siteD)>0: # there are some for this site and component name
                            PmagSiteRec=pmag.lnpbykey(siteD,'site',key) # get an average for this site
                            PmagSiteRec['site_comp_name']=comp # decorate the site record
                            PmagSiteRec["er_location_name"]=siteD[0]['er_location_name']
                            PmagSiteRec["er_site_name"]=siteD[0]['er_site_name']
                            PmagSiteRec['site_tilt_correction']=coord
                            PmagSiteRec['site_comp_name']= pmag.get_list(siteD,key+'_comp_name')
                            if avg_directions_by_sample:
                                PmagSiteRec['er_sample_names']= pmag.get_list(siteD,'er_sample_name')
                            else:
                                PmagSiteRec['er_specimen_names']= pmag.get_list(siteD,'er_specimen_name')
    # determine the demagnetization code (DC3,4 or 5) for this site
                            AFnum=len(pmag.get_dictitem(siteD,'magic_method_codes','LP-DIR-AF','has'))
                            Tnum=len(pmag.get_dictitem(siteD,'magic_method_codes','LP-DIR-T','has'))
                            DC=3
                            if AFnum>0:DC+=1
                            if Tnum>0:DC+=1
                            PmagSiteRec['magic_method_codes']= pmag.get_list(siteD,'magic_method_codes')+':'+ 'LP-DC'+str(DC)
                            PmagSiteRec['magic_method_codes'].strip(":")
                            if plotsites:
                                print PmagSiteRec['er_site_name']
                                pmagplotlib.plotSITE(EQ['eqarea'],PmagSiteRec,siteD,key) # plot and list the data
                                pmagplotlib.drawFIGS(EQ)
                            PmagSites.append(PmagSiteRec)
                else: # last component only
                    siteD=tmp1[:] # get the last orientation system specified
                    if len(siteD)>0: # there are some
                        PmagSiteRec=pmag.lnpbykey(siteD,'site',key) # get the average for this site
                        PmagSiteRec["er_location_name"]=siteD[0]['er_location_name'] # decorate the record
                        PmagSiteRec["er_site_name"]=siteD[0]['er_site_name']
                        PmagSiteRec['site_comp_name']=comp
                        PmagSiteRec['site_tilt_correction']=coord
                        PmagSiteRec['site_comp_name']= pmag.get_list(siteD,key+'_comp_name')
                        PmagSiteRec['er_specimen_names']= pmag.get_list(siteD,'er_specimen_name')
                        PmagSiteRec['er_sample_names']= pmag.get_list(siteD,'er_sample_name')
                        AFnum=len(pmag.get_dictitem(siteD,'magic_method_codes','LP-DIR-AF','has'))
                        Tnum=len(pmag.get_dictitem(siteD,'magic_method_codes','LP-DIR-T','has'))
                        DC=3
                        if AFnum>0:DC+=1
                        if Tnum>0:DC+=1
                        PmagSiteRec['magic_method_codes']= pmag.get_list(siteD,'magic_method_codes')+':'+ 'LP-DC'+str(DC)
                        PmagSiteRec['magic_method_codes'].strip(":")
                        if not avg_directions_by_sample:PmagSiteRec['site_comp_name']= pmag.get_list(siteD,key+'_comp_name')
                        if plotsites:
                            pmagplotlib.plotSITE(EQ['eqarea'],PmagSiteRec,siteD,key)
                            pmagplotlib.drawFIGS(EQ)
                        PmagSites.append(PmagSiteRec)
            else:
                print 'site information not found in er_sites for site, ',site,' site will be skipped'
    for PmagSiteRec in PmagSites: # now decorate each dictionary some more, and calculate VGPs etc. for results table
        PmagSiteRec["er_citation_names"]="This study"
        PmagSiteRec["er_analyst_mail_names"]=user
        PmagSiteRec['magic_software_packages']=version_num
        if agefile != "": PmagSiteRec= pmag.get_age(PmagSiteRec,"er_site_name","site_inferred_",AgeNFO,DefaultAge)
        PmagSiteRec['pmag_criteria_codes']='ACCEPT'
        if 'site_n_lines' in PmagSiteRec.keys() and 'site_n_planes' in PmagSiteRec.keys() and PmagSiteRec['site_n_lines']!="" and PmagSiteRec['site_n_planes']!="":
            if int(PmagSiteRec["site_n_planes"])>0:
                PmagSiteRec["magic_method_codes"]=PmagSiteRec['magic_method_codes']+":DE-FM-LP"
            elif int(PmagSiteRec["site_n_lines"])>2:
                PmagSiteRec["magic_method_codes"]=PmagSiteRec['magic_method_codes']+":DE-FM"
            kill=pmag.grade(PmagSiteRec,accept,'site_dir')
            if len(kill)==0:
                PmagResRec={} # set up dictionary for the pmag_results table entry
                PmagResRec['data_type']='i' # decorate it a bit
                PmagResRec['magic_software_packages']=version_num
                PmagSiteRec['site_description']='Site direction included in results table'
                PmagResRec['pmag_criteria_codes']='ACCEPT'
                dec=float(PmagSiteRec["site_dec"])
                inc=float(PmagSiteRec["site_inc"])
                if 'site_alpha95' in PmagSiteRec.keys() and PmagSiteRec['site_alpha95']!="":
                    a95=float(PmagSiteRec["site_alpha95"])
                else:a95=180.
                sitedat=pmag.get_dictitem(SiteNFO,'er_site_name',PmagSiteRec['er_site_name'],'T')[0] # fish out site information (lat/lon, etc.)
                lat=float(sitedat['site_lat'])
                lon=float(sitedat['site_lon'])
                plon,plat,dp,dm=pmag.dia_vgp(dec,inc,a95,lat,lon) # get the VGP for this site
                if PmagSiteRec['site_tilt_correction']=='-1':C=' (spec coord) '
                if PmagSiteRec['site_tilt_correction']=='0':C=' (geog. coord) '
                if PmagSiteRec['site_tilt_correction']=='100':C=' (strat. coord) '
                PmagResRec["pmag_result_name"]="VGP Site: "+PmagSiteRec["er_site_name"] # decorate some more
                PmagResRec["result_description"]="Site VGP, coord system = "+str(coord)+' component: '+comp
                PmagResRec['er_site_names']=PmagSiteRec['er_site_name']
                PmagResRec['pmag_criteria_codes']='ACCEPT'
                PmagResRec['er_citation_names']='This study'
                PmagResRec['er_analyst_mail_names']=user
                PmagResRec["er_location_names"]=PmagSiteRec["er_location_name"]
                if avg_directions_by_sample:
                    PmagResRec["er_sample_names"]=PmagSiteRec["er_sample_names"]
                else:
                    PmagResRec["er_specimen_names"]=PmagSiteRec["er_specimen_names"]
                PmagResRec["tilt_correction"]=PmagSiteRec['site_tilt_correction']
                PmagResRec["pole_comp_name"]=PmagSiteRec['site_comp_name']
                PmagResRec["average_dec"]=PmagSiteRec["site_dec"]
                PmagResRec["average_inc"]=PmagSiteRec["site_inc"]
                PmagResRec["average_alpha95"]=PmagSiteRec["site_alpha95"]
                PmagResRec["average_n"]=PmagSiteRec["site_n"]
                PmagResRec["average_n_lines"]=PmagSiteRec["site_n_lines"]
                PmagResRec["average_n_planes"]=PmagSiteRec["site_n_planes"]
                PmagResRec["vgp_n"]=PmagSiteRec["site_n"]
                PmagResRec["average_k"]=PmagSiteRec["site_k"]
                PmagResRec["average_r"]=PmagSiteRec["site_r"]
                PmagResRec["average_lat"]='%10.4f ' %(lat)
                PmagResRec["average_lon"]='%10.4f ' %(lon)
                if agefile != "": PmagResRec= pmag.get_age(PmagResRec,"er_site_names","average_",AgeNFO,DefaultAge)
                site_height=pmag.get_dictitem(height_nfo,'er_site_name',site,'T')
                if len(site_height)>0:PmagResRec["average_height"]=site_height[0]['site_height']
                PmagResRec["vgp_lat"]='%7.1f ' % (plat)
                PmagResRec["vgp_lon"]='%7.1f ' % (plon)
                PmagResRec["vgp_dp"]='%7.1f ' % (dp)
                PmagResRec["vgp_dm"]='%7.1f ' % (dm)
                PmagResRec["magic_method_codes"]= PmagSiteRec["magic_method_codes"]
                if '0' in PmagSiteRec['site_tilt_correction'] and "DA-DIR-GEO" not in PmagSiteRec['magic_method_codes']: PmagSiteRec['magic_method_codes']=PmagSiteRec['magic_method_codes']+":DA-DIR-GEO"
                if '100' in PmagSiteRec['site_tilt_correction'] and "DA-DIR-TILT" not in PmagSiteRec['magic_method_codes']: PmagSiteRec['magic_method_codes']=PmagSiteRec['magic_method_codes']+":DA-DIR-TILT"
                PmagSiteRec['site_polarity']=""
                if avg_by_polarity: # assign polarity based on angle of pole lat to spin axis - may want to re-think this sometime
                      angle=pmag.angle([0,0],[0,(90-plat)])
                      if angle <= 55.: PmagSiteRec["site_polarity"]='n'
                      if angle > 55. and angle < 125.: PmagSiteRec["site_polarity"]='t'
                      if angle >= 125.: PmagSiteRec["site_polarity"]='r'
                PmagResults.append(PmagResRec)
    if avg_by_polarity:
        crecs=pmag.get_dictitem(PmagSites,'site_tilt_correction','100','T') # find the tilt corrected data
        if len(crecs)<2:crecs=pmag.get_dictitem(PmagSites,'site_tilt_correction','0','T') # if there aren't any, find the geographic corrected data
        if len(crecs)>2: # if there are some,
            comp=pmag.get_list(crecs,'site_comp_name').split(':')[0] # find the first component
            crecs=pmag.get_dictitem(crecs,'site_comp_name',comp,'T') # fish out all of the first component
            precs=[]
            for rec in crecs:
                precs.append({'dec':rec['site_dec'],'inc':rec['site_inc'],'name':rec['er_site_name'],'loc':rec['er_location_name']})
            polpars=pmag.fisher_by_pol(precs) # calculate average by polarity
            for mode in polpars.keys(): # hunt through all the modes (normal=A, reverse=B, all=ALL)
                PolRes={}
                PolRes['er_citation_names']='This study'
                PolRes["pmag_result_name"]="Polarity Average: Polarity "+mode #
                PolRes["data_type"]="a"
                PolRes["average_dec"]='%7.1f'%(polpars[mode]['dec'])
                PolRes["average_inc"]='%7.1f'%(polpars[mode]['inc'])
                PolRes["average_n"]='%i'%(polpars[mode]['n'])
                PolRes["average_r"]='%5.4f'%(polpars[mode]['r'])
                PolRes["average_k"]='%6.0f'%(polpars[mode]['k'])
                PolRes["average_alpha95"]='%7.1f'%(polpars[mode]['alpha95'])
                PolRes['er_site_names']= polpars[mode]['sites']
                PolRes['er_location_names']= polpars[mode]['locs']
                PolRes['magic_software_packages']=version_num
                PmagResults.append(PolRes)

    if not skip_intensities and nositeints!=1:
      for site in sites: # now do intensities for each site
        if plotsites:print site
        if not avg_intensities_by_sample: key,intlist='specimen',SpecInts # if using specimen level data
        if avg_intensities_by_sample: key,intlist='sample',PmagSamps # if using sample level data
        Ints=pmag.get_dictitem(intlist,'er_site_name',site,'T') # get all the intensities  for this site
        if len(Ints)>0: # there are some
            PmagSiteRec=pmag.average_int(Ints,key,'site') # get average intensity stuff for site table
            PmagResRec=pmag.average_int(Ints,key,'average') # get average intensity stuff for results table
            if plotsites: # if site by site examination requested - print this site out to the screen
                for rec in Ints:print rec['er_'+key+'_name'],' %7.1f'%(1e6*float(rec[key+'_int']))
                if len(Ints)>1:
                    print 'Average: ','%7.1f'%(1e6*float(PmagResRec['average_int'])),'N: ',len(Ints)
                    print 'Sigma: ','%7.1f'%(1e6*float(PmagResRec['average_int_sigma'])),'Sigma %: ',PmagResRec['average_int_sigma_perc']
                raw_input('Press any key to continue\n')
            er_location_name=Ints[0]["er_location_name"]
            PmagSiteRec["er_location_name"]=er_location_name # decorate the records
            PmagSiteRec["er_citation_names"]="This study"
            PmagResRec["er_location_names"]=er_location_name
            PmagResRec["er_citation_names"]="This study"
            PmagSiteRec["er_analyst_mail_names"]=user
            PmagResRec["er_analyst_mail_names"]=user
            PmagResRec["data_type"]='i'
            if not avg_intensities_by_sample:
                PmagSiteRec['er_specimen_names']= pmag.get_list(Ints,'er_specimen_name') # list of all specimens used
                PmagResRec['er_specimen_names']= pmag.get_list(Ints,'er_specimen_name')
            PmagSiteRec['er_sample_names']= pmag.get_list(Ints,'er_sample_name') # list of all samples used
            PmagResRec['er_sample_names']= pmag.get_list(Ints,'er_sample_name')
            PmagSiteRec['er_site_name']= site
            PmagResRec['er_site_names']= site
            PmagSiteRec['magic_method_codes']= pmag.get_list(Ints,'magic_method_codes')
            PmagResRec['magic_method_codes']= pmag.get_list(Ints,'magic_method_codes')
            kill=pmag.grade(PmagSiteRec,accept,'site_int')
            if nocrit==1 or len(kill)==0:
                b,sig=float(PmagResRec['average_int']),""
                if(PmagResRec['average_int_sigma'])!="":
                    sig=float(PmagResRec['average_int_sigma'])
                sdir=pmag.get_dictitem(PmagResults,'er_site_names',site,'T') # fish out site direction
                if len(sdir)>0 and  sdir[-1]['average_inc']!="": # get the VDM for this record using last average inclination (hope it is the right one!)
                        inc=float(sdir[0]['average_inc']) #
                        mlat=pmag.magnetic_lat(inc) # get magnetic latitude using dipole formula
                        PmagResRec["vdm"]='%8.3e '% (pmag.b_vdm(b,mlat)) # get VDM with magnetic latitude
                        PmagResRec["vdm_n"]=PmagResRec['average_int_n']
                        if 'average_int_sigma' in PmagResRec.keys() and PmagResRec['average_int_sigma']!="":
                            vdm_sig=pmag.b_vdm(float(PmagResRec['average_int_sigma']),mlat)
                            PmagResRec["vdm_sigma"]='%8.3e '% (vdm_sig)
                        else:
                            PmagResRec["vdm_sigma"]=""
                mlat="" # define a model latitude
                if get_model_lat==1: # use present site latitude
                    mlats=pmag.get_dictitem(SiteNFO,'er_site_name',site,'T')
                    if len(mlats)>0: mlat=mlats[0]['site_lat']
                elif get_model_lat==2: # use a model latitude from some plate reconstruction model (or something)
                    mlats=pmag.get_dictitem(ModelLats,'er_site_name',site,'T')
                    if len(mlats)>0: PmagResRec['model_lat']=mlats[0]['site_model_lat']
                    mlat=PmagResRec['model_lat']
                if mlat!="":
                    PmagResRec["vadm"]='%8.3e '% (pmag.b_vdm(b,float(mlat))) # get the VADM using the desired latitude
                    if sig!="":
                        vdm_sig=pmag.b_vdm(float(PmagResRec['average_int_sigma']),float(mlat))
                        PmagResRec["vadm_sigma"]='%8.3e '% (vdm_sig)
                        PmagResRec["vadm_n"]=PmagResRec['average_int_n']
                    else:
                        PmagResRec["vadm_sigma"]=""
                sitedat=pmag.get_dictitem(SiteNFO,'er_site_name',PmagSiteRec['er_site_name'],'T') # fish out site information (lat/lon, etc.)
                if len(sitedat)>0:
                    sitedat=sitedat[0]
                    PmagResRec['average_lat']=sitedat['site_lat']
                    PmagResRec['average_lon']=sitedat['site_lon']
                else:
                    PmagResRec['average_lon']='UNKNOWN'
                    PmagResRec['average_lon']='UNKNOWN'
                PmagResRec['magic_software_packages']=version_num
                PmagResRec["pmag_result_name"]="V[A]DM: Site "+site
                PmagResRec["result_description"]="V[A]DM of site"
                PmagResRec["pmag_criteria_codes"]="ACCEPT"
                if agefile != "": PmagResRec= pmag.get_age(PmagResRec,"er_site_names","average_",AgeNFO,DefaultAge)
                site_height=pmag.get_dictitem(height_nfo,'er_site_name',site,'T')
                if len(site_height)>0:PmagResRec["average_height"]=site_height[0]['site_height']
                PmagSites.append(PmagSiteRec)
                PmagResults.append(PmagResRec)
    if len(PmagSites)>0:
        Tmp,keylist=pmag.fillkeys(PmagSites)
        pmag.magic_write(siteout,Tmp,'pmag_sites')
        print ' sites written to ',siteout
    else: print "No Site level table"
    if len(PmagResults)>0:
        TmpRes,keylist=pmag.fillkeys(PmagResults)
        pmag.magic_write(resout,TmpRes,'pmag_results')
        print ' results written to ',resout
    else: print "No Results level table"


def orientation_magic(or_con=1, dec_correction_con=1, dec_correction=0, bed_correction=True,
                      samp_con='1', hours_from_gmt=0, method_codes='', average_bedding=False,
                      orient_file='orient.txt', samp_file='er_samples.txt', site_file='er_sites.txt',
                      output_dir_path='.', input_dir_path='.', append=False, data_model=2):
    """
    use this function to convert tab delimited field notebook information to MagIC formatted tables (er_samples and er_sites)

    INPUT FORMAT
        Input files must be tab delimited and have in the first line:
tab  location_name
        Note: The "location_name" will facilitate searching in the MagIC database. Data from different
            "locations" should be put in separate files.  The definition of a "location" is rather loose.
             Also this is the word 'tab' not a tab, which will be indicated by '\t'.
        The second line has the names of the columns (tab delimited), e.g.:
site_name sample_name mag_azimuth field_dip date lat long sample_lithology sample_type sample_class shadow_angle hhmm stratigraphic_height bedding_dip_direction bedding_dip GPS_baseline image_name image_look image_photographer participants method_codes site_description sample_description GPS_Az, sample_igsn, sample_texture, sample_cooling_rate, cooling_rate_corr, cooling_rate_mcd


      Notes:
        1) column order doesn't matter but the NAMES do.
        2) sample_name, sample_lithology, sample_type, sample_class, lat and long are required.  all others are optional.
        3) If subsequent data are the same (e.g., date, bedding orientation, participants, stratigraphic_height),
            you can leave the field blank and the program will fill in the last recorded information. BUT if you really want a blank stratigraphic_height, enter a '-1'.    These will not be inherited and must be specified for each entry: image_name, look, photographer or method_codes
        4) hhmm must be in the format:  hh:mm and the hh must be in 24 hour time.
    date must be mm/dd/yy (years < 50 will be converted to  20yy and >50 will be assumed 19yy)
        5) image_name, image_look and image_photographer are colon delimited lists of file name (e.g., IMG_001.jpg) image look direction and the name of the photographer respectively.  If all images had same look and photographer, just enter info once.  The images will be assigned to the site for which they were taken - not at the sample level.
        6) participants:  Names of who helped take the samples.  These must be a colon delimited list.
        7) method_codes:  Special method codes on a sample level, e.g., SO-GT5 which means the orientation is has an uncertainty of >5 degrees
             for example if it broke off before orienting....
        8) GPS_Az is the place to put directly determined GPS Azimuths, using, e.g., points along the drill direction.
        9) sample_cooling_rate is the cooling rate in K per Ma
        10) int_corr_cooling_rate
        11) cooling_rate_mcd:  data adjustment method code for cooling rate correction;  DA-CR-EG is educated guess; DA-CR-PS is percent estimated from pilot samples; DA-CR-TRM is comparison between 2 TRMs acquired with slow and rapid cooling rates.
is the percent cooling rate factor to apply to specimens from this sample, DA-CR-XX is the method code


    defaults:
    orientation_magic(or_con=1, dec_correction_con=1, dec_correction=0, bed_correction=True, samp_con='1', hours_from_gmt=0, method_codes='', average_bedding=False, orient_file='orient.txt', samp_file='er_samples.txt', site_file='er_sites.txt', output_dir_path='.', input_dir_path='.', append=False):
    orientation conventions:
        [1] Standard Pomeroy convention of azimuth and hade (degrees from vertical down)
             of the drill direction (field arrow).  lab arrow azimuth= sample_azimuth = mag_azimuth;
             lab arrow dip = sample_dip =-field_dip. i.e. the lab arrow dip is minus the hade.
        [2] Field arrow is the strike  of the plane orthogonal to the drill direction,
             Field dip is the hade of the drill direction.  Lab arrow azimuth = mag_azimuth-90
             Lab arrow dip = -field_dip
        [3] Lab arrow is the same as the drill direction;
             hade was measured in the field.
             Lab arrow azimuth = mag_azimuth; Lab arrow dip = 90-field_dip
        [4] lab azimuth and dip are same as mag_azimuth, field_dip : use this for unoriented samples too
        [5] Same as AZDIP convention explained below -
            azimuth and inclination of the drill direction are mag_azimuth and field_dip;
            lab arrow is as in [1] above.
            lab azimuth is same as mag_azimuth,lab arrow dip=field_dip-90
        [6] Lab arrow azimuth = mag_azimuth-90; Lab arrow dip = 90-field_dip
        [7] see http://earthref.org/PmagPy/cookbook/#field_info for more information.  You can customize other format yourself, or email ltauxe@ucsd.edu for help.


    Magnetic declination convention:
        [1] Use the IGRF value at the lat/long and date supplied [default]
        [2] Will supply declination correction
        [3] mag_az is already corrected in file
        [4] Correct mag_az but not bedding_dip_dir

    Sample naming convention:
        [1] XXXXY: where XXXX is an arbitrary length site designation and Y
            is the single character sample designation.  e.g., TG001a is the
            first sample from site TG001.    [default]
        [2] XXXX-YY: YY sample from site XXXX (XXX, YY of arbitary length)
        [3] XXXX.YY: YY sample from site XXXX (XXX, YY of arbitary length)
        [4-Z] XXXX[YYY]:  YYY is sample designation with Z characters from site XXX
        [5] site name = sample name
        [6] site name entered in site_name column in the orient.txt format input file  -- NOT CURRENTLY SUPPORTED
        [7-Z] [XXX]YYY:  XXX is site designation with Z characters from samples  XXXYYY
        NB: all others you will have to either customize your
            self or e-mail ltauxe@ucsd.edu for help.


    """
    # initialize some variables
    # bed_correction used to be BedCorr
    # dec_correction_con used to be corr
    # dec_correction used to be DecCorr
    # meths is now method_codes
    # delta_u is now hours_from_gmt

    or_con, dec_correction_con, dec_correction = int(or_con), int(dec_correction_con), float(dec_correction)
    hours_from_gmt = float(hours_from_gmt)
    stratpos=""
    date,lat,lon="","",""  # date of sampling, latitude (pos North), longitude (pos East)
    bed_dip,bed_dip_dir="",""
    participantlist=""
    Lats,Lons=[],[] # list of latitudes and longitudes
    SampOuts,SiteOuts,ImageOuts=[],[],[]  # lists of Sample records and Site records
    samplelist,sitelist,imagelist=[],[],[]
    Z=1
    newbaseline,newbeddir,newbeddip="","",""
    fpars = []
    sclass,lithology,sample_type="","",""
    newclass,newlith,newtype='','',''
    BPs=[]# bedding pole declinations, bedding pole inclinations
    image_file = "er_images.txt"
    #
    # use 3.0. default filenames when in 3.0.
    # but, still allow for custom names
    data_model = int(data_model)
    if data_model == 3:
        if samp_file == "er_samples.txt":
            samp_file = "samples.txt"
        if site_file == "er_sites.txt":
            site_file = "sites.txt"
        image_file = "images.txt"
    orient_file = os.path.join(input_dir_path,orient_file)
    samp_file = os.path.join(output_dir_path,samp_file)
    site_file = os.path.join(output_dir_path, site_file)
    image_file= os.path.join(output_dir_path, image_file)

    # validate input
    if '4' in samp_con[0]:
        pattern = re.compile('[4][-]\d')
        result = pattern.match(samp_con)
        if not result:
            raise Exception("If using sample naming convention 4, you must provide the number of characters with which to distinguish sample from site. [4-Z] XXXX[YYY]:  YYY is sample designation with Z characters from site XXX)")

    if '7' in samp_con[0]:
        pattern = re.compile('[7][-]\d')
        result = pattern.match(samp_con)
        if not result:
            raise Exception("If using sample naming convention 7, you must provide the number of characters with which to distinguish sample from site.  [7-Z] [XXX]YYY:  XXX is site designation with Z characters from samples  XXXYYY")

    if dec_correction_con == 2 and not dec_correction:
        raise Exception("If using magnetic declination convention 2, you must also provide a declincation correction in degrees")

    SampRecs,SiteRecs,ImageRecs=[],[],[]
    SampRecs_sorted, SiteRecs_sorted = {}, {}

    if append:
        try:
            SampRecs,file_type=pmag.magic_read(samp_file)
            # convert 3.0. sample file to 2.5 format
            if data_model == 3:
                SampRecs3 = SampRecs
                SampRecs = []
                for samp_rec in SampRecs3:
                    rec = map_magic.mapping(samp_rec, map_magic.samp_magic3_2_magic2_map)
                    SampRecs.append(rec)
            SampRecs_sorted=pmag.sort_magic_data(SampRecs,'er_sample_name') # magic_data dictionary sorted by sample_name
            print 'sample data to be appended to: ', samp_file
        except Exception as ex:
            print ex
            print 'problem with existing file: ',samp_file, ' will create new.'
        try:
            SiteRecs,file_type=pmag.magic_read(site_file)
            # convert 3.0. site file to 2.5 format
            if data_model == 3:
                SiteRecs3 = SiteRecs
                SiteRecs = []
                for site_rec in SiteRecs3:
                    SiteRecs.append(map_magic.mapping(site_rec, map_magic.site_magic3_2_magic2_map))
            SiteRecs_sorted=pmag.sort_magic_data(SiteRecs,'er_site_name') # magic_data dictionary sorted by site_name
            print 'site data to be appended to: ',site_file
        except Exception as ex:
            print ex
            print 'problem with existing file: ',site_file,' will create new.'
        try:
            ImageRecs,file_type=pmag.magic_read(image_file)
            # convert from 3.0. --> 2.5
            if data_model == 3:
                ImageRecs3 = ImageRecs
                ImageRecs = []
                for image_rec in ImageRecs3:
                    ImageRecs.append(map_magic.mapping(image_rec, map_magic.image_magic3_2_magic2_map))
            print 'image data to be appended to: ',image_file
        except:
            print 'problem with existing file: ',image_file,' will create new.'
    #
    # read in file to convert
    #
    OrData, location_name=pmag.magic_read(orient_file)
    if location_name == "demag_orient":
        location_name = ""
    #
    # step through the data sample by sample
    #
    # use map_magic in here...

    for OrRec in OrData:
        if 'mag_azimuth' not in OrRec.keys():
            OrRec['mag_azimuth']=""
        if 'field_dip' not in OrRec.keys():
            OrRec['field_dip']=""
        if OrRec['mag_azimuth']==" ":
            OrRec["mag_azimuth"]=""
        if OrRec['field_dip']==" ":
            OrRec["field_dip"]=""
        if 'sample_description' in OrRec.keys():
            sample_description=OrRec['sample_description']
        else:
            sample_description=""
        if 'sample_igsn' in OrRec.keys():
            sample_igsn=OrRec['sample_igsn']
        else:
            sample_igsn=""
        if 'sample_texture' in OrRec.keys():
            sample_texture=OrRec['sample_texture']
        else:
            sample_texture=""
        if 'sample_cooling_rate' in OrRec.keys():
            sample_cooling_rate=OrRec['sample_cooling_rate']
        else:
            sample_cooling_rate=""
        if 'cooling_rate_corr' in OrRec.keys():
            cooling_rate_corr=OrRec['cooling_rate_corr']
            if 'cooling_rate_mcd' in OrRec.keys():
                cooling_rate_mcd=OrRec['cooling_rate_mcd']
            else:
                cooling_rate_mcd='DA-CR'
        else:
            cooling_rate_corr=""
            cooling_rate_mcd=""
        sample_orientation_flag='g'
        if 'sample_orientation_flag' in OrRec.keys():
            if OrRec['sample_orientation_flag']=='b' or OrRec["mag_azimuth"]=="":
                sample_orientation_flag='b'
        methcodes=method_codes  # initialize method codes
        if methcodes:
            if 'method_codes' in OrRec.keys() and OrRec['method_codes'].strip()!="":
                methcodes=methcodes+":"+OrRec['method_codes'] # add notes
        else:
            if 'method_codes' in OrRec.keys() and OrRec['method_codes'].strip()!="":
                methcodes=OrRec['method_codes'] # add notes
        codes=methcodes.replace(" ","").split(":")
        sample_name=OrRec["sample_name"]
        # patch added by rshaar 7/2016
        # if sample_name already exists in er_samples.txt:
        # merge the new data colmuns calculated by orientation_magic with the existing data colmuns
        # this is done to make sure no previous data in er_samples.txt and er_sites.txt is lost.

        if sample_name in SampRecs_sorted.keys():
            Prev_MagRec=SampRecs_sorted[sample_name][-1]
            MagRec=Prev_MagRec
        else:
            Prev_MagRec={}
            MagRec={}
        MagRec["er_citation_names"]="This study"

        # the following keys were calculated or defined in the code above:
        for key in ['sample_igsn','sample_texture','sample_cooling_rate','cooling_rate_corr','cooling_rate_mcd','participantlist']:
            command= "var= %s"%key
            exec command
            if var!="":
                MagRec[key]=var
            elif  key  in  Prev_MagRec.keys():
                MagRec[key]=Prev_MagRec[key]
            else:
                MagRec[key]=""

            if location_name!="":
                MagRec["er_location_name"]=location_name
            elif  "er_location_name"  in  Prev_MagRec.keys():
                MagRec["er_location_name"]=Prev_MagRec["er_location_name"]
            else:
                MagRec["er_location_name"]=""

        # the following keys are taken directly from OrRec dictionary:
        for key in ["sample_height","er_sample_alternatives"]:
            if key  in OrRec.keys() and OrRec[key]!= "":
                MagRec[key]=OrRec[key]
            elif  key  in  Prev_MagRec.keys():
                MagRec[key]=Prev_MagRec[key]
            else:
                MagRec[key]=""

        # the following keys are cab be defined here as "Not Specified" :

        for key in ["sample_class","sample_lithology","sample_type"]:
            if key  in OrRec.keys() and OrRec[key]!= "" and  OrRec[key]!= "Not Specified" :
                MagRec[key]=OrRec[key]
            elif  key  in  Prev_MagRec.keys() and  Prev_MagRec[key]!= "" and  Prev_MagRec[key]!= "Not Specified" :
                MagRec[key]=Prev_MagRec[key]
            else:
                MagRec[key]="Not Specified"


        # (rshaar) From here parse new information and replace previous, if exists:
    #
    # parse information common to all orientation methods
    #
        MagRec["er_sample_name"]=OrRec["sample_name"]
        if "IGSN" in OrRec.keys():
            MagRec["sample_igsn"]=OrRec["IGSN"]
        else:
            MagRec["sample_igsn"]=""
        #MagRec["sample_height"],MagRec["sample_bed_dip_direction"],MagRec["sample_bed_dip"]="","",""
        MagRec["sample_bed_dip_direction"],MagRec["sample_bed_dip"]="",""
        #if "er_sample_alternatives" in OrRec.keys():
        #    MagRec["er_sample_alternatives"]=OrRec["sample_alternatives"]
        sample=OrRec["sample_name"]
        if OrRec['mag_azimuth']=="" and OrRec['field_dip']!="":
            OrRec['mag_azimuth']='999'
        if OrRec["mag_azimuth"]!="":
            labaz,labdip=pmag.orient(float(OrRec["mag_azimuth"]),float(OrRec["field_dip"]),or_con)
            if labaz<0:labaz+=360.
        else:
            labaz,labdip="",""
        if  OrRec['mag_azimuth']=='999':labaz=""
        if "GPS_baseline" in OrRec.keys() and OrRec['GPS_baseline']!="":
            newbaseline=OrRec["GPS_baseline"]
        if newbaseline!="":
            baseline=float(newbaseline)
        if 'participants' in OrRec.keys() and OrRec['participants']!="" and OrRec['participants']!=participantlist:
            participantlist=OrRec['participants']
        MagRec['er_scientist_mail_names']=participantlist
        MagRec.pop("participantlist")
        newlat=OrRec["lat"]
        if newlat!="":
            lat=float(newlat)
        if lat=="":
            print "No latitude specified for ! ",sample, ". Latitude is required for all samples."
            return False, "No latitude specified for ! " + sample + ". Latitude is required for all samples."
        MagRec["sample_lat"]='%11.5f'%(lat)
        newlon=OrRec["long"]
        if newlon!="":
            lon=float(newlon)
        if lon=="":
            print "No longitude specified for ! ",sample, ". Longitude is required for all samples."
            return False, str("No longitude specified for ! " + sample + ". Longitude is required for all samples.")
        MagRec["sample_lon"]='%11.5f'%(lon)
        if 'bedding_dip_direction' in OrRec.keys():
            newbeddir=OrRec["bedding_dip_direction"]
        if newbeddir!="":
            bed_dip_dir=OrRec['bedding_dip_direction']
        if 'bedding_dip' in OrRec.keys():
            newbeddip=OrRec["bedding_dip"]
        if newbeddip!="":
            bed_dip=OrRec['bedding_dip']
        MagRec["sample_bed_dip"]=bed_dip
        MagRec["sample_bed_dip_direction"]=bed_dip_dir
        #MagRec["sample_type"]=sample_type
        if labdip!="":
            MagRec["sample_dip"]='%7.1f'%labdip
        else:
            MagRec["sample_dip"]=""
        if "date" in OrRec.keys() and OrRec["date"]!="":
            newdate=OrRec["date"]
            if newdate!="":
                date=newdate
            mmddyy=date.split('/')
            yy=int(mmddyy[2])
            if yy>50:
                yy=1900+yy
            else:
                yy=2000+yy
            decimal_year=yy+float(mmddyy[0])/12
            sample_date='%i:%s:%s'%(yy,mmddyy[0],mmddyy[1])
            time=OrRec['hhmm']
            if time:
                sample_date += (':' + time)
            MagRec["sample_date"]=sample_date.strip(':')
        if labaz!="":
            MagRec["sample_azimuth"]='%7.1f'%(labaz)
        else:
            MagRec["sample_azimuth"]=""
        if "stratigraphic_height" in OrRec.keys():
            if OrRec["stratigraphic_height"]!="":
                MagRec["sample_height"]=OrRec["stratigraphic_height"]
                stratpos=OrRec["stratigraphic_height"]
            elif OrRec["stratigraphic_height"]=='-1':
                MagRec["sample_height"]=""   # make empty
            elif stratpos != "" :
                MagRec["sample_height"]=stratpos   # keep last record if blank
#
        if dec_correction_con==1 and MagRec['sample_azimuth']!="": # get magnetic declination (corrected with igrf value)
            x,y,z,f=pmag.doigrf(lon,lat,0,decimal_year)
            Dir=pmag.cart2dir( (x,y,z))
            dec_correction=Dir[0]
        if "bedding_dip" in OrRec.keys():
            if OrRec["bedding_dip"]!="":
                MagRec["sample_bed_dip"]=OrRec["bedding_dip"]
                bed_dip=OrRec["bedding_dip"]
            else:
                MagRec["sample_bed_dip"]=bed_dip
        else: MagRec["sample_bed_dip"]='0'
        if "bedding_dip_direction" in OrRec.keys():
            if OrRec["bedding_dip_direction"]!="" and bed_correction==1:
                dd=float(OrRec["bedding_dip_direction"])+dec_correction
                if dd>360.:dd=dd-360.
                MagRec["sample_bed_dip_direction"]='%7.1f'%(dd)
                dip_dir=MagRec["sample_bed_dip_direction"]
            else:
                MagRec["sample_bed_dip_direction"]=OrRec['bedding_dip_direction']
        else:
            MagRec["sample_bed_dip_direction"]='0'
        if average_bedding:
            if str(MagRec["sample_bed_dip_direction"]) and str(MagRec["sample_bed_dip"]):
                BPs.append([float(MagRec["sample_bed_dip_direction"]),float(MagRec["sample_bed_dip"])-90.,1.])
        if MagRec['sample_azimuth']=="" and MagRec['sample_dip']=="":
            MagRec["sample_declination_correction"]=''
            methcodes=methcodes+':SO-NO'
        MagRec["magic_method_codes"]=methcodes
        MagRec['sample_description']=sample_description
    #
    # work on the site stuff too
        if 'site_name' in OrRec.keys() and OrRec['site_name']!="":
            site=OrRec['site_name']
        elif 'site_name' in Prev_MagRec.keys() and  Prev_MagRec['site_name']!="":
            site=Prev_MagRec['site_name']
        else:
            site=pmag.parse_site(OrRec["sample_name"],samp_con,Z) # parse out the site name
        MagRec["er_site_name"]=site
        site_description="" # overwrite any prior description
        if 'site_description' in OrRec.keys() and OrRec['site_description']!="":
            site_description=OrRec['site_description'].replace(",",";")
        if "image_name" in OrRec.keys():
            images=OrRec["image_name"].split(":")
            if "image_look" in OrRec.keys():
                looks=OrRec['image_look'].split(":")
            else:
                looks=[]
            if "image_photographer" in OrRec.keys():
                photographers=OrRec['image_photographer'].split(":")
            else:
                photographers=[]
            for image in images:
                if image !="" and image not in imagelist:
                    imagelist.append(image)
                    ImageRec={}
                    ImageRec['er_image_name']=image
                    ImageRec['image_type']="outcrop"
                    ImageRec['image_date']=sample_date
                    ImageRec['er_citation_names']="This study"
                    ImageRec['er_location_name']=location_name
                    ImageRec['er_site_name']=MagRec['er_site_name']
                    k=images.index(image)
                    if len(looks)>k:
                        ImageRec['er_image_description']="Look direction: "+looks[k]
                    elif len(looks)>=1:
                        ImageRec['er_image_description']="Look direction: "+looks[-1]
                    else:
                        ImageRec['er_image_description']="Look direction: unknown"
                    if len(photographers)>k:
                        ImageRec['er_photographer_mail_names']=photographers[k]
                    elif len(photographers)>=1:
                        ImageRec['er_photographer_mail_names']=photographers[-1]
                    else:
                        ImageRec['er_photographer_mail_names']="unknown"
                    ImageOuts.append(ImageRec)
        if site not in sitelist:
            sitelist.append(site) # collect unique site names
            # patch added by rshaar 7/2016
            # if sample_name already exists in er_samples.txt:
            # merge the new data colmuns calculated by orientation_magic with the existing data colmuns
            # this is done to make sure no previous data in er_samples.txt and er_sites.txt is lost.

            if site in SiteRecs_sorted.keys():
                Prev_MagRec=SiteRecs_sorted[site][-1]
                SiteRec=Prev_MagRec
            else:
                Prev_MagRec={}
                SiteRec={}
            SiteRec["er_citation_names"]="This study"
            SiteRec["er_site_name"]=site
            SiteRec["site_definition"]="s"

            for key in ["er_location_name"]:
                if key in Prev_MagRec.keys() and Prev_MagRec[key]!="":
                    SiteRec[key]=Prev_MagRec[key]
                else:
                    SiteRec[key]=""

            for key in ["lat","lon","height"]:
                if "site_"+key in Prev_MagRec.keys() and Prev_MagRec["site_"+key]!="":
                    SiteRec["site_"+key]=Prev_MagRec["site_"+key]
                else:
                    SiteRec["site_"+key]=MagRec["sample_"+key]


            #SiteRec["site_lat"]=MagRec["sample_lat"]
            #SiteRec["site_lon"]=MagRec["sample_lon"]
            #SiteRec["site_height"]=MagRec["sample_height"]

            for key in ["class","lithology","type"]:
                if "site_"+key in Prev_MagRec.keys() and Prev_MagRec["site_"+key]!="Not Specified":
                    SiteRec["site_"+key]=Prev_MagRec["site_"+key]
                else:
                    SiteRec["site_"+key]=MagRec["sample_"+key]

            #SiteRec["site_class"]=MagRec["sample_class"]
            #SiteRec["site_lithology"]=MagRec["sample_lithology"]
            #SiteRec["site_type"]=MagRec["sample_type"]

            if site_description != "": # overwrite only if site_description has something
                SiteRec["site_description"]=site_description
            SiteOuts.append(SiteRec)
        if sample not in samplelist:
            samplelist.append(sample)
            if MagRec['sample_azimuth']!="": # assume magnetic compass only
                MagRec['magic_method_codes']=MagRec['magic_method_codes']+':SO-MAG'
                MagRec['magic_method_codes']=MagRec['magic_method_codes'].strip(":")
            SampOuts.append(MagRec)
            if MagRec['sample_azimuth']!="" and dec_correction_con!=3:
                az=labaz+dec_correction
                if az>360.:az=az-360.
                CMDRec={}
                for key in MagRec.keys():
                    CMDRec[key]=MagRec[key] # make a copy of MagRec
                CMDRec["sample_azimuth"]='%7.1f'%(az)
                CMDRec["magic_method_codes"]=methcodes+':SO-CMD-NORTH'
                CMDRec["magic_method_codes"]=CMDRec['magic_method_codes'].strip(':')
                CMDRec["sample_declination_correction"]='%7.1f'%(dec_correction)
                if dec_correction_con==1:
                    CMDRec['sample_description']=sample_description+':Declination correction calculated from IGRF'
                else:
                    CMDRec['sample_description']=sample_description+':Declination correction supplied by user'
                CMDRec["sample_description"]=CMDRec['sample_description'].strip(':')
                SampOuts.append(CMDRec)
            if "mag_az_bs" in OrRec.keys() and OrRec["mag_az_bs"] !="" and OrRec["mag_az_bs"]!=" ":
                SRec={}
                for key in MagRec.keys():
                    SRec[key]=MagRec[key] # make a copy of MagRec
                labaz=float(OrRec["mag_az_bs"])
                az=labaz+dec_correction
                if az>360.:az=az-360.
                SRec["sample_azimuth"]='%7.1f'%(az)
                SRec["sample_declination_correction"]='%7.1f'%(dec_correction)
                SRec["magic_method_codes"]=methcodes+':SO-SIGHT-BACK:SO-CMD-NORTH'
                SampOuts.append(SRec)
    #
    # check for suncompass data
    #
            if "shadow_angle" in OrRec.keys() and OrRec["shadow_angle"]!="":  # there are sun compass data
                if hours_from_gmt=="":
                    #hours_from_gmt=raw_input("Enter hours to SUBTRACT from time for  GMT: [0] ")
                    hours_from_gmt=0
                SunRec,sundata={},{}
                shad_az=float(OrRec["shadow_angle"])
                if not OrRec["hhmm"]:
                    print 'If using the column shadow_angle for sun compass data, you must also provide the time for each sample.  Sample ', sample, ' has shadow_angle but is missing the "hh:mm" column.'
                else: # calculate sun declination
                    sundata["date"]='%i:%s:%s:%s'%(yy,mmddyy[0],mmddyy[1],OrRec["hhmm"])
    #                if eval(hours_from_gmt)<0:
    #                        MagRec["sample_time_zone"]='GMT'+hours_from_gmt+' hours'
    #                else:
    #                    MagRec["sample_time_zone"]='GMT+'+hours_from_gmt+' hours'
                    sundata["delta_u"]=hours_from_gmt
                    sundata["lon"]='%7.1f'%(lon)
                    sundata["lat"]='%7.1f'%(lat)
                    sundata["shadow_angle"]=OrRec["shadow_angle"]
                    sundec=pmag.dosundec(sundata)
                    for key in MagRec.keys():
                        SunRec[key]=MagRec[key]  # make a copy of MagRec
                    SunRec["sample_azimuth"]='%7.1f'%(sundec)
                    SunRec["sample_declination_correction"]=''
                    SunRec["magic_method_codes"]=methcodes+':SO-SUN'
                    SunRec["magic_method_codes"]=SunRec['magic_method_codes'].strip(':')
                    SampOuts.append(SunRec)
    #
    # check for differential GPS data
    #
            if "prism_angle" in OrRec.keys() and OrRec["prism_angle"]!="":  # there are diff GPS data
                GPSRec={}
                for key in MagRec.keys():
                    GPSRec[key]=MagRec[key]  # make a copy of MagRec
                prism_angle=float(OrRec["prism_angle"])
                laser_angle=float(OrRec["laser_angle"])
                if OrRec["GPS_baseline"]!="": baseline=float(OrRec["GPS_baseline"]) # new baseline
                gps_dec=baseline+laser_angle+prism_angle-90.
                while gps_dec>360.:
                    gps_dec=gps_dec-360.
                while gps_dec<0:
                    gps_dec=gps_dec+360.
                for key in MagRec.keys():
                    GPSRec[key]=MagRec[key]  # make a copy of MagRec
                GPSRec["sample_azimuth"]='%7.1f'%(gps_dec)
                GPSRec["sample_declination_correction"]=''
                GPSRec["magic_method_codes"]=methcodes+':SO-GPS-DIFF'
                SampOuts.append(GPSRec)
            if "GPS_Az" in OrRec.keys() and OrRec["GPS_Az"]!="":  # there are differential GPS Azimuth data
                GPSRec={}
                for key in MagRec.keys():
                    GPSRec[key]=MagRec[key]  # make a copy of MagRec
                GPSRec["sample_azimuth"]='%7.1f'%(float(OrRec["GPS_Az"]))
                GPSRec["sample_declination_correction"]=''
                GPSRec["magic_method_codes"]=methcodes+':SO-GPS-DIFF'
                SampOuts.append(GPSRec)
        if average_bedding!="0" and fpars:
            fpars=pmag.fisher_mean(BPs)
            print 'over-writing all bedding with average '
    Samps=[]
    for  rec in SampOuts:
        if average_bedding!="0" and fpars:
            rec['sample_bed_dip_direction']='%7.1f'%(fpars['dec'])
            rec['sample_bed_dip']='%7.1f'%(fpars['inc']+90.)
            Samps.append(rec)
        else:
            Samps.append(rec)
    for rec in SampRecs:
        if rec['er_sample_name'] not in samplelist: # overwrite prior for this sample
            Samps.append(rec)
    for rec in SiteRecs:
        if rec['er_site_name'] not in sitelist: # overwrite prior for this sample
            SiteOuts.append(rec)
    for rec in ImageRecs:
        if rec['er_image_name'] not in imagelist: # overwrite prior for this sample
            ImageOuts.append(rec)
    print 'saving data...'
    SampsOut,keys=pmag.fillkeys(Samps)
    Sites,keys=pmag.fillkeys(SiteOuts)
    if data_model == 3:
        SampsOut3 = []
        Sites3 = []
        for samp_rec in SampsOut:
            new_rec = map_magic.mapping(samp_rec, map_magic.samp_magic2_2_magic3_map)
            SampsOut3.append(new_rec)
        for site_rec in Sites:
            new_rec = map_magic.mapping(site_rec, map_magic.site_magic2_2_magic3_map)
            Sites3.append(new_rec)
        wrote_samps = pmag.magic_write(samp_file,SampsOut3,"samples")
        wrote_sites = pmag.magic_write(site_file,Sites3,"sites")
    else:
        wrote_samps = pmag.magic_write(samp_file,SampsOut,"er_samples")
        wrote_sites = pmag.magic_write(site_file,Sites,"er_sites")
    if wrote_samps:
        print "Data saved in ", samp_file,' and ',site_file
    else:
        print "No data found"
    if len(ImageOuts)>0:
        # need to do conversion here 3.0. --> 2.5
        Images,keys=pmag.fillkeys(ImageOuts)
        image_type = "er_images"
        if data_model == 3:
            # convert 2.5 --> 3.0.
            image_type = "images"
            Images2 = Images
            Images = []
            for image_rec in Images2:
                Images.append(map_magic.mapping(image_rec, map_magic.image_magic2_2_magic3_map))
        pmag.magic_write(image_file, Images, image_type)
        print "Image info saved in ", image_file
    return True, None


def azdip_magic(orient_file='orient.txt', samp_file="er_samples.txt", samp_con="1", Z=1, method_codes='FS-FD', location_name='unknown', append=False, output_dir='.', input_dir='.'):
    """
    azdip_magic(orient_file='orient.txt', samp_file="er_samples.txt", samp_con="1", Z=1, method_codes='FS-FD', location_name='unknown', append=False):
    takes space delimited AzDip file and converts to MagIC formatted tables

    specify sampling method codes as a colon delimited string:  [default is: FS-FD]
             FS-FD field sampling done with a drill
             FS-H field sampling done with hand samples
             FS-LOC-GPS  field location done with GPS
             FS-LOC-MAP  field location done with map
             SO-POM   a Pomeroy orientation device was used
             SO-ASC   an ASC orientation device was used
             SO-MAG   orientation with magnetic compass

    INPUT FORMAT
        Input files must be space delimited:
            Samp  Az Dip Strike Dip
        Orientation convention:
             Lab arrow azimuth = mag_azimuth; Lab arrow dip = 90-field_dip
                e.g. field_dip is degrees from horizontal of drill direction

         Magnetic declination convention:
             Az is already corrected in file

       Sample naming convention:
            [1] XXXXY: where XXXX is an arbitrary length site designation and Y
                is the single character sample designation.  e.g., TG001a is the
                first sample from site TG001.    [default]
            [2] XXXX-YY: YY sample from site XXXX (XXX, YY of arbitary length)
            [3] XXXX.YY: YY sample from site XXXX (XXX, YY of arbitary length)
            [4-Z] XXXX[YYY]:  YYY is sample designation with Z characters from site XXX
            [5] site name same as sample
            [6] site name entered in site_name column in the orient.txt format input file  -- NOT CURRENTLY SUPPORTED
            [7-Z] [XXXX]YYY:  XXXX is site designation with Z characters with sample name XXXXYYYY
            NB: all others you will have to customize your self
                 or e-mail ltauxe@ucsd.edu for help.

    """
    #
    # initialize variables
    #
    DEBUG=0
    version_num=pmag.get_version()
    or_con,corr = "3","1"
    date,lat,lon="","",""  # date of sampling, latitude (pos North), longitude (pos East)
    bed_dip,bed_dip_dir="",""
    participantlist=""
    sites=[]   # list of site names
    Lats,Lons=[],[] # list of latitudes and longitudes
    SampRecs,SiteRecs,ImageRecs,imagelist=[],[],[],[]  # lists of Sample records and Site records
    average_bedding="1",1,"0"
    newbaseline,newbeddir,newbeddip="","",""
    delta_u="0"
    sclass,lithology,type="","",""
    newclass,newlith,newtype='','',''
    user=""
    corr=="3"
    DecCorr=0.
    samp_file = os.path.join(output_dir, samp_file)
    orient_file = os.path.join(input_dir, orient_file)
    #
    #
    if append:
        try:
            SampRecs,file_type=pmag.magic_read(samp_file)
            print "sample data to be appended to: ",samp_file
        except:
            print 'problem with existing samp file: ',samp_file,' will create new'
    #
    # read in file to convert
    #
    azfile=open(orient_file,'rU')
    AzDipDat=azfile.readlines()
    if not AzDipDat:
        return False, 'No data in orientation file, please try again'
    azfile.close()
    SampOut,samplist=[],[]
    for line in AzDipDat:
        orec=line.split()
        if len(orec)>2:
            labaz,labdip=pmag.orient(float(orec[1]),float(orec[2]),or_con)
            bed_dip=float(orec[4])
            if bed_dip!=0:
                bed_dip_dir=float(orec[3])-90. # assume dip to right of strike
            else:
                bed_dip_dir=float(orec[3]) # assume dip to right of strike
            MagRec={}
            MagRec["er_location_name"]=location_name
            MagRec["er_citation_names"]="This study"
    #
    # parse information common to all orientation methods
    #
            MagRec["er_sample_name"]=orec[0]
            MagRec["sample_bed_dip"]='%7.1f'%(bed_dip)
            MagRec["sample_bed_dip_direction"]='%7.1f'%(bed_dip_dir)
            MagRec["sample_dip"]='%7.1f'%(labdip)
            MagRec["sample_azimuth"]='%7.1f'%(labaz)
            methods = method_codes.replace(" ","").split(":")
            OR = 0
            for method in methods:
                method_type = method.split("-")
                if "SO" in method_type:
                    OR=1
            if OR==0:
                method_codes = method_codes + ":SO-NO"
            MagRec["magic_method_codes"] = method_codes
            site=pmag.parse_site(orec[0],samp_con,Z) # parse out the site name
            MagRec["er_site_name"]=site
            MagRec['magic_software_packages']=version_num
            SampOut.append(MagRec)
            if MagRec['er_sample_name'] not in samplist:
                samplist.append(MagRec['er_sample_name'])
    for samp in SampRecs:
        if samp not in samplist:
            SampOut.append(samp)
    Samps,keys=pmag.fillkeys(SampOut)
    pmag.magic_write(samp_file,Samps,"er_samples")
    print "Data saved in ", samp_file
    return True, None


def iodp_samples_magic(samp_file, output_samp_file=None, output_dir_path='.', input_dir_path='.'):
    """
    iodp_samples_magic(samp_file, output_samp_file=None, output_dir_path='.', input_dir_path='.')
    Default is to overwrite er_samples.txt in your output working directory.
    To specify an er_samples file to append to, use output_samp_file.
    """
    text_key = None
    comp_depth_key=""
    samp_file = os.path.join(input_dir_path, samp_file)
    Samps=[]
    if output_samp_file:
        samp_out = os.path.join(output_dir_path, output_samp_file)
        Samps,file_type = pmag.magic_read(samp_out)
        print len(Samps), ' read in from: ',samp_out
    else:
        samp_out = os.path.join(output_dir_path, 'er_samples.txt')
    file_input = open(samp_file,"rU").readlines()
    keys = file_input[0].replace('\n','').split(',')
    if "CSF-B Top (m)" in keys:
        comp_depth_key="CSF-B Top (m)"
    elif "Top depth CSF-B (m)" in keys:
        comp_depth_key="Top depth CSF-B (m)"
    if "Top Depth (m)" in keys:  # incorporate changes to LIMS data model, while maintaining backward compatibility
        depth_key="Top Depth (m)"
    elif "CSF-A Top (m)" in keys:
        depth_key="CSF-A Top (m)"
    elif "Top depth CSF-A (m)" in keys:
        depth_key="Top depth CSF-A (m)"
    if "Text Id" in keys:
        text_key="Text Id"
    elif "Text identifier" in keys:
        text_key="Text identifier"
    elif "Text ID" in keys:
        text_key="Text ID"
    if "Sample Date Logged" in keys:
        date_key="Sample Date Logged"
    elif "Sample date logged" in keys:
        date_key="Sample date logged"
    elif "Date sample logged" in keys:
        date_key="Date sample logged"
    elif "Timestamp (UTC)" in keys:
        date_key="Timestamp (UTC)"
    if 'Volume (cc)' in keys:volume_key='Volume (cc)'
    if 'Volume (cm^3)' in keys:volume_key='Volume (cm^3)'
    if 'Volume (cm3)' in keys:volume_key='Volume (cm3)'
    if not text_key:
        return False, "Could not extract the necessary data from your input file.\nPlease make sure you are providing a correctly formated IODP samples csv file."
    ErSamples,samples,file_format=[],[],'old'
    for line in file_input[1:]:
      if line[0]!='0':
        ODPRec,SampRec={},{}
        interval,core="",""
        rec=line.replace('\n','').split(',')
        if len(rec)<2:
            print "Error in csv file, blank columns"
            break
        for k in range(len(keys)):
            ODPRec[keys[k]]=rec[k].strip('"')
        SampRec['er_sample_alternatives']=ODPRec[text_key]
        if "Label Id" in keys: # old format
            label=ODPRec['Label Id'].split()
            if len(label)>1:
                interval=label[1].split('/')[0]
                pieces=label[0].split('-')
                core=pieces[2]
            while len(core)<4:core='0'+core # my way
        else: # new format
            file_format='new'
            pieces=[ODPRec['Exp'],ODPRec['Site']+ODPRec['Hole'],ODPRec['Core']+ODPRec['Type'],ODPRec['Sect'],ODPRec['A/W']]
            interval=ODPRec['Top offset (cm)'].split('.')[0].strip() # only integers allowed!
            core=ODPRec['Core']+ODPRec['Type']
        if core!="" and interval!="":
            SampRec['magic_method_codes']='FS-C-DRILL-IODP:SP-SS-C:SO-V'
            if file_format=='old':
                SampRec['er_sample_name']=pieces[0]+'-'+pieces[1]+'-'+core+'-'+pieces[3]+'-'+pieces[4]+'-'+interval
            else:
                SampRec['er_sample_name']=pieces[0]+'-'+pieces[1]+'-'+core+'-'+pieces[3]+'_'+pieces[4]+'_'+interval # change in sample name convention
            SampRec['er_site_name']=SampRec['er_sample_name']
            #pieces=SampRec['er_sample_name'].split('-')
            SampRec['er_expedition_name']=pieces[0]
            SampRec['er_location_name']=pieces[1]
            SampRec['er_citation_names']="This study"
            SampRec['sample_dip']="0"
            SampRec['sample_azimuth']="0"
            SampRec['sample_core_depth']=ODPRec[depth_key]
            if ODPRec[volume_key]!="":
                SampRec['sample_volume']=str(float(ODPRec[volume_key])*1e-6)
            else:
                SampRec['sample_volume']='1'
            if comp_depth_key!="":
                SampRec['sample_composite_depth']=ODPRec[comp_depth_key]
            dates=ODPRec[date_key].split()
            if '/' in dates[0]: # have a date
                mmddyy=dates[0].split('/')
                yyyy='20'+mmddyy[2]
                mm=mmddyy[0]
                if len(mm)==1:mm='0'+mm
                dd=mmddyy[1]
                if len(dd)==1:dd='0'+dd
                date=yyyy+':'+mm+':'+dd+':'+dates[1]+":00.00"
            else:
                date=""
            SampRec['sample_date']=date
            ErSamples.append(SampRec)
            samples.append(SampRec['er_sample_name'])
    if len(Samps)>0:
        for samp in Samps:
           if samp['er_sample_name'] not in samples:
               ErSamples.append(samp)
    Recs,keys=pmag.fillkeys(ErSamples)
    pmag.magic_write(samp_out,Recs,'er_samples')
    print 'sample information written to: ',samp_out
    return True, samp_out


def kly4s_magic(infile, specnum=0, locname="unknown", inst='SIO-KLY4S',
                samp_con="1", or_con='3' ,user='', measfile='magic_measurements.txt',
                aniso_outfile='rmag_anisotropy.txt', samp_infile='', spec_infile='',
                spec_outfile='er_specimens.txt', azdip_infile='', output_dir_path='.',
                input_dir_path='.'):
    """
    def kly4s_magic(infile, specnum=0, locname="unknown", inst='SIO-KLY4S', samp_con="1", or_con='3' ,user='', measfile='magic_measurements.txt', aniso_outfile='rmag_anisotropy.txt', samp_infile='', spec_infile='', azdip_infile='', output_dir_path='.', input_dir_path='.'):

    NAME
        kly4s_magic.py

    DESCRIPTION
        converts files generated by SIO kly4S labview program to MagIC formated
        files for use with PmagPy plotting software

    SYNTAX
        kly4s_magic.py -h [command line options]

    OPTIONS
        -h: prints the help message and quits
        -i: allows interactive input of input/output filenames
        -f FILE: specify .ams input file name
        -fad AZDIP: specify AZDIP file with orientations, will create er_samples.txt file
        -fsa SFILE: specify existing er_samples.txt file with orientation information
        -fsp SPFILE: specify existing er_specimens.txt file for appending
        -F MFILE: specify magic_measurements output file
        -Fa AFILE: specify rmag_anisotropy output file
        -ocn ORCON:  specify orientation convention: default is #3 below -only with AZDIP file
        -usr USER: specify who made the measurements
        -loc LOC: specify location name for study
        -ins INST: specify instrument used
        -spc SPEC: specify number of characters to specify specimen from sample
        -ncn NCON:  specify naming convention: default is #1 below

    DEFAULTS
        MFILE: magic_measurements.txt
        AFILE: rmag_anisotropy.txt
        SPFILE: create new er_specimens.txt file
        USER: ""
        LOC: "unknown"
        INST: "SIO-KLY4S"
        SPEC: 1  specimen name is same as sample (if SPEC is 1, sample is all but last character)
    NOTES:
        Sample naming convention:
            [1] XXXXY: where XXXX is an arbitrary length site designation and Y
                is the single character sample designation.  e.g., TG001a is the
                first sample from site TG001.    [default]
            [2] XXXX-YY: YY sample from site XXXX (XXX, YY of arbitary length)
            [3] XXXX.YY: YY sample from site XXXX (XXX, YY of arbitary length)
            [4-Z] XXXXYYY:  YYY is sample designation with Z characters from site XXX
            [5] site name same as sample
            [6] site name entered in site_name column in the orient.txt format input file  -- NOT CURRENTLY SUPPORTED
            [7-Z] [XXXX]YYY:  XXXX is site designation with Z characters with sample name XXXXYYYY
            NB: all others you will have to customize your self
                 or e-mail ltauxe@ucsd.edu for help.


       Orientation convention:
            [1] Lab arrow azimuth= azimuth; Lab arrow dip=-dip
                i.e., dip is degrees from vertical down - the hade [default]
            [2] Lab arrow azimuth = azimuth-90; Lab arrow dip = -dip
                i.e., azimuth is strike and dip is hade
            [3] Lab arrow azimuth = azimuth; Lab arrow dip = dip-90
                e.g. dip is degrees from horizontal of drill direction
            [4] Lab arrow azimuth = azimuth; Lab arrow dip = dip
            [5] Lab arrow azimuth = azimuth; Lab arrow dip = 90-dip
            [6] all others you will have to either customize your
                self or e-mail ltauxe@ucsd.edu for help.

    """

    # initialize variables
    #not used: #cont=0

    ask=0
    Z=1
    AniRecs,SpecRecs,SampRecs,MeasRecs=[],[],[],[]
    AppSpec=0

    # format variables
    specnum = int(specnum)
    samp_con = str(samp_con)
    or_con = str(or_con)
    if azdip_infile:
        azdip_infile = os.path.join(input_dir_path, azdip_infile)
        azfile=open(azdip_infile,'rU')
        AzDipDat=azfile.readlines()
    amsfile = os.path.join(input_dir_path, infile)
    if spec_infile:
        spec_infile = os.path.join(output_dir_path, spec_infile)
        AppSpec = 1
    else:
        spec_outfile = os.path.join(output_dir_path, spec_outfile)
        AppSpec = 0
    if samp_infile:
        samp_infile = os.path.join(output_dir_path, samp_infile)
    measfile = os.path.join(output_dir_path, measfile)
    anisfile = os.path.join(output_dir_path, aniso_outfile)

    # validate variables
    if "4" in samp_con[0]:
        if "-" not in samp_con:
            print "option [4] must be in form 4-Z where Z is an integer"
            return False, "option [4] must be in form 4-Z where Z is an integer"
        else:
            Z=samp_con.split("-")[1]
            samp_con="4"
    if "7" in samp_con[0]:
        if "-" not in samp_con:
            print "option [7] must be in form 7-Z where Z is an integer"
            return False, "option [7] must be in form 7-Z where Z is an integer"
        else:
            Z=samp_con.split("-")[1]
            samp_con="7"

    try:
        file_input=open(amsfile,'rU')
    except:
        print 'Error opening file: ', amsfile
        return False, 'Error opening file: {}'.format(amsfile)

    # parse file
    SpecRecs,speclist=[],[]
    if AppSpec==1:
        try:
            SpecRecs,filetype=pmag.magic_read(spec_infile) # append new records to existing
            if len(SpecRecs)>0:
                for spec in SpecRecs:
                    if spec['er_specimen_name'] not in speclist:
                        speclist.append(spec['er_specimen_name'])
        except IOError:
            print 'trouble opening ',spec_infile
    Data=file_input.readlines()
    samps=[]
    if samp_infile:
        samps,file_type=pmag.magic_read(samp_infile)
        SO_methods=[]
        for rec in samps:
           if "magic_method_codes" in rec.keys():
               methlist=rec["magic_method_codes"].replace(" ","").split(":")
               for meth in methlist:
                   if "SO" in meth and "SO-POM" not in meth and "SO-GT5" not in meth and "SO-ASC" not in meth and "SO-BAD" not in meth:
                       if meth not in SO_methods: SO_methods.append(meth)
    #
        SO_priorities=pmag.set_priorities(SO_methods,ask)
    for line in Data:
      rec=line.split()
      if len(rec)>0:
        AniRec,SpecRec,SampRec,SiteRec,MeasRec={},{},{},{},{}
        specname=rec[0]
        if specnum!=0:
            sampname=specname[:-specnum]
        else:
            sampname=specname
        site=pmag.parse_site(sampname,samp_con,Z)
        AniRec['er_location_name']=locname
        AniRec['er_citation_names']="This study"
        AniRec['magic_instrument_codes']=inst
        method_codes=['LP-X','AE-H','LP-AN-MS']
        AniRec['magic_experiment_name']=specname+":"+"LP-AN-MS"
        AniRec['er_analyst_mail_names']=user
        AniRec['er_site_name']=site
        AniRec['er_sample_name']=sampname
        AniRec['er_specimen_name']=specname
        labaz,labdip,bed_dip_direction,bed_dip="","","",""
        if azdip_infile:
            for key in AniRec.keys():
                SampRec[key]=AniRec[key]
            for oline in AzDipDat: # look for exact match first
                orec=oline.replace('\n','').split()
                if orec[0].upper() in specname.upper(): # we have a match
                   labaz,labdip=pmag.orient(float(orec[1]),float(orec[2]),or_con)
                   bed_dip_direction=float(orec[3])-90. # assume dip to right of strike
                   bed_dip=float(orec[4])
                   break
            if labaz=="":  # found no exact match - now look at sample level
                for oline in AzDipDat:
                    orec=oline.split()
                    if orec[0].upper() == sampname.upper(): # we have a match
                       labaz,labdip=pmag.orient(float(orec[1]),float(orec[2]),or_con)
                       bed_dip_direction=float(orec[3])-90. # assume dip to right of strike
                       bed_dip=float(orec[4])
                       break
            if labaz=="":  # found no exact match - now look at sample level
                print 'found no orientation data - will use specimen coordinates'
                #raw_input("<return> to continue")
            else:
                for key in AniRec.keys():
                    SampRec[key]=AniRec[key]
                SampRec['sample_azimuth']='%7.1f'%(labaz)
                SampRec['sample_dip']='%7.1f'%(labdip)
                SampRec['sample_bed_dip_direction']='%7.1f'%(bed_dip_direction)
                SampRec['sample_bed_dip']='%7.1f'%(bed_dip)
                SampRecs.append(SampRec)
        elif samp_infile:
           redo,p=1,0
           orient={}
           if len(SO_methods)==1:
                az_type=SO_methods[0]
                orient=pmag.find_samp_rec(AniRec["er_sample_name"],samps,az_type)
                if orient['sample_azimuth']!="":
                    method_codes.append(az_type)
                else:
                    print "no orientation data for ",AniRec["er_sample_name"],labaz
                    orient["sample_azimuth"]=""
                    orient["sample_dip"]=""
                    orient["sample_bed_dip_direction"]=""
                    orient["sample_bed_dip"]=""
                    noorient=1
                    method_codes.append("SO-NO")
                    redo=0
                redo=0
           while redo==1:
                if p>=len(SO_priorities):
                    print "no orientation data for ",AniRec["er_sample_name"],labaz
                    orient["sample_azimuth"]=""
                    orient["sample_dip"]=""
                    orient["sample_bed_dip_direction"]=""
                    orient["sample_bed_dip"]=""
                    noorient=1
                    method_codes.append("SO-NO")
                    redo=0
                else:
                    az_type=SO_methods[SO_methods.index(SO_priorities[p])]
                    orient=pmag.find_samp_rec(AniRec["er_sample_name"],samps,az_type)
                    if orient["sample_azimuth"]  !="":
                        method_codes.append(az_type)
                        redo=0
                    noorient=0
                p+=1
           if orient['sample_azimuth']!="":
               labaz=float(orient['sample_azimuth'])
           if orient['sample_dip']!="":
               labdip=float(orient['sample_dip'])
           if "sample_bed_dip_direction" in orient.keys() and orient['sample_bed_dip_direction']!="":
               bed_dip_direction=float(orient['sample_bed_dip_direction'])
           if "sample_bed_dip" in orient.keys() and orient['sample_bed_dip']!="":
               sample_bed_dip=float(orient['sample_bed_dip'])
        for key in AniRec.keys():
            SpecRec[key]=AniRec[key]
        for key in AniRec.keys():
            MeasRec[key]=AniRec[key]
        AniRec['anisotropy_type']="AMS"
        AniRec['anisotropy_n']="192"
        AniRec['anisotropy_s1']=rec[1]
        AniRec['anisotropy_s2']=rec[2]
        AniRec['anisotropy_s3']=rec[3]
        AniRec['anisotropy_s4']=rec[4]
        AniRec['anisotropy_s5']=rec[5]
        AniRec['anisotropy_s6']=rec[6]
        AniRec['anisotropy_sigma']=rec[7]
        AniRec['anisotropy_tilt_correction']='-1'
        AniRec['anisotropy_unit']='Normalized by trace'
        SpecRec['specimen_volume']='%8.3e'%(1e-6*float(rec[12])) # volume from cc to m^3
        MeasRec['measurement_flag']='g' # good
        MeasRec['measurement_standard']='u' # unknown
        date=rec[14].split('/')
        if int(date[2])>80:
           date[2]='19'+date[2]
        else:
           date[2]='20'+date[2]
        datetime=date[2]+':'+date[0]+':'+date[1]+":"
        datetime=datetime+rec[15]
        MeasRec['measurement_number']='1'
        MeasRec['measurement_date']=datetime
        MeasRec['measurement_lab_field_ac']='%8.3e'%(4*math.pi*1e-7*float(rec[11])) # convert from A/m to T
        MeasRec['measurement_temp']="300" # assumed room T in kelvin
        MeasRec['measurement_chi_volume']=rec[8]
        MeasRec['measurement_description']='Bulk measurement'
        MeasRec['magic_method_codes']='LP-X'
        if SpecRec['er_specimen_name'] not in speclist: # add to list
            speclist.append(SpecRec['er_specimen_name'])
            SpecRecs.append(SpecRec)
        MeasRecs.append(MeasRec)
        methods=""
        for meth in method_codes:
            methods=methods+meth+":"
        AniRec["magic_method_codes"]=methods[:-1]  # get rid of annoying spaces in Anthony's export files
        AniRecs.append(AniRec)
        if labaz!="": # have orientation info
            AniRecG,AniRecT={},{}
            for key in AniRec.keys():AniRecG[key]=AniRec[key]
            for key in AniRec.keys():AniRecT[key]=AniRec[key]
            sbar=[]
            sbar.append(float(AniRec['anisotropy_s1']))
            sbar.append(float(AniRec['anisotropy_s2']))
            sbar.append(float(AniRec['anisotropy_s3']))
            sbar.append(float(AniRec['anisotropy_s4']))
            sbar.append(float(AniRec['anisotropy_s5']))
            sbar.append(float(AniRec['anisotropy_s6']))
            sbarg=pmag.dosgeo(sbar,labaz,labdip)
            AniRecG["anisotropy_s1"]='%12.10f'%(sbarg[0])
            AniRecG["anisotropy_s2"]='%12.10f'%(sbarg[1])
            AniRecG["anisotropy_s3"]='%12.10f'%(sbarg[2])
            AniRecG["anisotropy_s4"]='%12.10f'%(sbarg[3])
            AniRecG["anisotropy_s5"]='%12.10f'%(sbarg[4])
            AniRecG["anisotropy_s6"]='%12.10f'%(sbarg[5])
            AniRecG["anisotropy_tilt_correction"]='0'
            AniRecs.append(AniRecG)
            if bed_dip!="" and bed_dip!=0: # have tilt correction
                sbart=pmag.dostilt(sbarg,bed_dip_direction,bed_dip)
                AniRecT["anisotropy_s1"]='%12.10f'%(sbart[0])
                AniRecT["anisotropy_s2"]='%12.10f'%(sbart[1])
                AniRecT["anisotropy_s3"]='%12.10f'%(sbart[2])
                AniRecT["anisotropy_s4"]='%12.10f'%(sbart[3])
                AniRecT["anisotropy_s5"]='%12.10f'%(sbart[4])
                AniRecT["anisotropy_s6"]='%12.10f'%(sbart[5])
                AniRecT["anisotropy_tilt_correction"]='100'
                AniRecs.append(AniRecT)
    pmag.magic_write(anisfile,AniRecs,'rmag_anisotropy')
    pmag.magic_write(measfile,MeasRecs,'magic_measurements')
    if AppSpec:
        pmag.magic_write(spec_infile,SpecRecs,'er_specimens')
        print 'specimen information appended to {}'.format(spec_infile)
    else:
        pmag.magic_write(spec_outfile, SpecRecs, 'er_specimens')
        print 'specimen information written to new file: {}'.format(spec_outfile)
    print 'anisotropy data saved in ',anisfile
    print 'measurement data saved in ',measfile
    if azdip_infile:
        sampfile='er_samples.txt'
        pmag.magic_write(sampfile,SampRecs,'er_samples')
        print 'sample data saved in ',sampfile
    return True, measfile


def k15_magic(k15file, specnum=0, sample_naming_con='1', er_location_name="unknown", measfile='magic_measurements.txt', sampfile="er_samples.txt", aniso_outfile='rmag_anisotropy.txt', result_file="rmag_results.txt", input_dir_path='.', output_dir_path='.'):
    """
    def k15_magic(k15file, specnum=0, sample_naming_con='1', er_location_name="unknown", measfile='magic_measurements.txt', sampfile="er_samples.txt", aniso_outfile='rmag_anisotropy.txt', result_file="rmag_results.txt", input_dir_path='.', output_dir_path='.'):

    NAME
        k15_magic.py

    DESCRIPTION
        converts .k15 format data to magic_measurements  format.
        assums Jelinek Kappabridge measurement scheme

    SYNTAX
        k15_magic.py [-h] [command line options]

    OPTIONS
        -h prints help message and quits
        -f KFILE: specify .k15 format input file
        -F MFILE: specify magic_measurements format output file
        -Fsa SFILE, specify er_samples format file for output
        -Fa AFILE, specify rmag_anisotropy format file for output
        -Fr RFILE, specify rmag_results format file for output
        -loc LOC: specify location name for study
    #-ins INST: specify instrument that measurements were made on # not implemented
        -spc NUM: specify number of digits for specimen ID, default is 0
        -ncn NCOM: specify naming convention (default is #1)
       Sample naming convention:
            [1] XXXXY: where XXXX is an arbitrary length site designation and Y
                is the single character sample designation.  e.g., TG001a is the
                first sample from site TG001.    [default]
            [2] XXXX-YY: YY sample from site XXXX (XXX, YY of arbitary length)
            [3] XXXX.YY: YY sample from site XXXX (XXX, YY of arbitary length)
            [4-Z] XXXXYYY:  YYY is sample designation with Z characters from site XXX
            [5] site name same as sample
            [6] site name entered in site_name column in the orient.txt format input file  -- NOT CURRENTLY SUPPORTED
            [7-Z] [XXXX]YYY:  XXXX is site designation with Z characters with sample name XXXXYYYY
            NB: all others you will have to customize your self
                 or e-mail ltauxe@ucsd.edu for help.


    DEFAULTS
        MFILE: k15_measurements.txt
        SFILE: er_samples.txt
        AFILE: rmag_anisotropy.txt
        RFILE: rmag_results.txt
        LOC: unknown
        INST: unknown

    INPUT
      name [az,pl,strike,dip], followed by
      3 rows of 5 measurements for each specimen

    """

    #
    # initialize some variables
    #
    # removed 'inst' variable because it is never used
    version_num=pmag.get_version()
    syn=0
    itilt,igeo,linecnt,key=0,0,0,""
    first_save=1
    k15 = []
    citation='This study'
# pick off stuff from command line
    Z=""
    if "4" in sample_naming_con:
        if "-" not in sample_naming_con:
            print "option [4] must be in form 4-Z where Z is an integer"
            return False, "option [4] must be in form 4-Z where Z is an integer"
        else:
            Z=sample_naming_con.split("-")[1]
            sample_naming_con="4"
    if sample_naming_con=='6':
        Samps,filetype=pmag.magic_read(os.path.join(input_dir_path, 'er_samples.txt'))
    sampfile = os.path.join(output_dir_path, sampfile)
    measfile= os.path.join(output_dir_path, measfile)
    aniso_outfile= os.path.join(output_dir_path, aniso_outfile)
    result_file= os.path.join(output_dir_path, result_file)
    k15file = os.path.join(input_dir_path, k15file)
    if not os.path.exists(k15file):
        print k15file
        return False, "You must provide a valid k15 format file"
    try:
        SampRecs,filetype=pmag.magic_read(sampfile) # append new records to existing
        samplist=[]
        for samp in SampRecs:
            if samp['er_sample_name'] not in samplist:
                samplist.append(samp['er_sample_name'])
    except IOError:
        SampRecs=[]
    # measurement directions for Jelinek 1977 protocol:
    Decs=[315,225,180,135,45,90,270,270,270,90,180,180,0,0,0]
    Incs=[0,0,0,0,0,-45,-45,0,45,45,45,-45,-90,-45,45]
    # some defaults to read in  .k15 file format
    # list of measurements and default number of characters for specimen ID
# some magic default definitions
    #
    # read in data
    input=open(k15file,'rU')
    MeasRecs,SpecRecs,AnisRecs,ResRecs=[],[],[],[]
    # read in data
    MeasRec,SpecRec,SampRec,SiteRec,AnisRec,ResRec={},{},{},{},{},{}
    for line in input.readlines():
            linecnt+=1
            rec=line.split()
            if linecnt==1:
                MeasRec["magic_method_codes"]=""
                SpecRec["magic_method_codes"]=""
                SampRec["magic_method_codes"]=""
                AnisRec["magic_method_codes"]=""
                SiteRec["magic_method_codes"]=""
                ResRec["magic_method_codes"]=""
                MeasRec["magic_software_packages"]=version_num
                SpecRec["magic_software_packages"]=version_num
                SampRec["magic_software_packages"]=version_num
                AnisRec["magic_software_packages"]=version_num
                SiteRec["magic_software_packages"]=version_num
                ResRec["magic_software_packages"]=version_num
                MeasRec["magic_method_codes"]="LP-X"
                MeasRec["measurement_flag"]="g"
                MeasRec["measurement_standard"]="u"
                MeasRec["er_citation_names"]="This study"
                SpecRec["er_citation_names"]="This study"
                SampRec["er_citation_names"]="This study"
                AnisRec["er_citation_names"]="This study"
                ResRec["er_citation_names"]="This study"
                MeasRec["er_specimen_name"]=rec[0]
                MeasRec["magic_experiment_name"]=rec[0]+":LP-AN-MS"
                AnisRec["magic_experiment_names"]=rec[0]+":AMS"
                ResRec["magic_experiment_names"]=rec[0]+":AMS"
                SpecRec["er_specimen_name"]=rec[0]
                AnisRec["er_specimen_name"]=rec[0]
                SampRec["er_specimen_name"]=rec[0]
                ResRec["rmag_result_name"]=rec[0]
                specnum=int(specnum)
                if specnum!=0:
                    MeasRec["er_sample_name"]=rec[0][:-specnum]
                if specnum==0:
                    MeasRec["er_sample_name"]=rec[0]
                SampRec["er_sample_name"]=MeasRec["er_sample_name"]
                SpecRec["er_sample_name"]=MeasRec["er_sample_name"]
                AnisRec["er_sample_name"]=MeasRec["er_sample_name"]
                ResRec["er_sample_names"]=MeasRec["er_sample_name"]
                if sample_naming_con=="6":
                    for samp in Samps:
                        if samp['er_sample_name']==AnisRec["er_sample_name"]:
                            sitename=samp['er_site_name']
                            er_location_name=samp['er_location_name']
                elif sample_naming_con!="":
                    sitename=pmag.parse_site(AnisRec['er_sample_name'],sample_naming_con,Z)
                MeasRec["er_site_name"]=sitename
                MeasRec["er_location_name"]=er_location_name
                SampRec["er_site_name"]=MeasRec["er_site_name"]
                SpecRec["er_site_name"]=MeasRec["er_site_name"]
                AnisRec["er_site_name"]=MeasRec["er_site_name"]
                ResRec["er_site_names"]=MeasRec["er_site_name"]
                SampRec["er_location_name"]=MeasRec["er_location_name"]
                SpecRec["er_location_name"]=MeasRec["er_location_name"]
                AnisRec["er_location_name"]=MeasRec["er_location_name"]
                ResRec["er_location_names"]=MeasRec["er_location_name"]
                if len(rec)>=3:
                    SampRec["sample_azimuth"],SampRec["sample_dip"]=rec[1],rec[2]
                    az,pl,igeo=float(rec[1]),float(rec[2]),1
                if len(rec)==5:
                    SampRec["sample_bed_dip_direction"],SampRec["sample_bed_dip"]= '%7.1f'%(90.+float(rec[3])),(rec[4])
                    bed_az,bed_dip,itilt,igeo=90.+float(rec[3]),float(rec[4]),1,1
            else:
                for i in range(5):
                    k15.append(1e-6*float(rec[i])) # assume measurements in micro SI
                if linecnt==4:
                    sbar,sigma,bulk=pmag.dok15_s(k15)
                    hpars=pmag.dohext(9,sigma,sbar)
                    MeasRec["treatment_temp"]='%8.3e' % (273) # room temp in kelvin
                    MeasRec["measurement_temp"]='%8.3e' % (273) # room temp in kelvin
                    for i in range(15):
                        NewMeas=copy.deepcopy(MeasRec)
                        NewMeas["measurement_orient_phi"]='%7.1f' %(Decs[i])
                        NewMeas["measurement_orient_theta"]='%7.1f'% (Incs[i])
                        NewMeas["measurement_chi_volume"]='%12.10f'% (k15[i])
                        NewMeas["measurement_number"]='%i'% (i+1)
                        NewMeas["magic_experiment_name"]=rec[0]+":LP-AN-MS"
                        MeasRecs.append(NewMeas)
                    if SampRec['er_sample_name'] not in samplist:
                        SampRecs.append(SampRec)
                        samplist.append(SampRec['er_sample_name'])
                    SpecRecs.append(SpecRec)
                    AnisRec["anisotropy_type"]="AMS"
                    ResRec["anisotropy_type"]="AMS"
                    AnisRec["anisotropy_s1"]='%12.10f'%(sbar[0])
                    AnisRec["anisotropy_s2"]='%12.10f'%(sbar[1])
                    AnisRec["anisotropy_s3"]='%12.10f'%(sbar[2])
                    AnisRec["anisotropy_s4"]='%12.10f'%(sbar[3])
                    AnisRec["anisotropy_s5"]='%12.10f'%(sbar[4])
                    AnisRec["anisotropy_s6"]='%12.10f'%(sbar[5])
                    AnisRec["anisotropy_mean"]='%12.10f'%(bulk)
                    AnisRec["anisotropy_sigma"]='%12.10f'%(sigma)
                    AnisRec["anisotropy_unit"]='SI'
                    AnisRec["anisotropy_n"]='15'
                    AnisRec["anisotropy_tilt_correction"]='-1'
                    AnisRec["magic_method_codes"]='LP-X:AE-H:LP-AN-MS'
                    AnisRecs.append(AnisRec)
                    ResRec["magic_method_codes"]='LP-X:AE-H:LP-AN-MS'
                    ResRec["anisotropy_tilt_correction"]='-1'
                    ResRec["anisotropy_t1"]='%12.10f'%(hpars['t1'])
                    ResRec["anisotropy_t2"]='%12.10f'%(hpars['t2'])
                    ResRec["anisotropy_t3"]='%12.10f'%(hpars['t3'])
                    ResRec["anisotropy_fest"]='%12.10f'%(hpars['F'])
                    ResRec["anisotropy_ftest12"]='%12.10f'%(hpars['F12'])
                    ResRec["anisotropy_ftest23"]='%12.10f'%(hpars['F23'])
                    ResRec["anisotropy_v1_dec"]='%7.1f'%(hpars['v1_dec'])
                    ResRec["anisotropy_v2_dec"]='%7.1f'%(hpars['v2_dec'])
                    ResRec["anisotropy_v3_dec"]='%7.1f'%(hpars['v3_dec'])
                    ResRec["anisotropy_v1_inc"]='%7.1f'%(hpars['v1_inc'])
                    ResRec["anisotropy_v2_inc"]='%7.1f'%(hpars['v2_inc'])
                    ResRec["anisotropy_v3_inc"]='%7.1f'%(hpars['v3_inc'])
                    ResRec['anisotropy_v1_eta_dec']=ResRec['anisotropy_v2_dec']
                    ResRec['anisotropy_v1_eta_inc']=ResRec['anisotropy_v2_inc']
                    ResRec['anisotropy_v1_zeta_dec']=ResRec['anisotropy_v3_dec']
                    ResRec['anisotropy_v1_zeta_inc']=ResRec['anisotropy_v3_inc']
                    ResRec['anisotropy_v2_eta_dec']=ResRec['anisotropy_v1_dec']
                    ResRec['anisotropy_v2_eta_inc']=ResRec['anisotropy_v1_inc']
                    ResRec['anisotropy_v2_zeta_dec']=ResRec['anisotropy_v3_dec']
                    ResRec['anisotropy_v2_zeta_inc']=ResRec['anisotropy_v3_inc']
                    ResRec['anisotropy_v3_eta_dec']=ResRec['anisotropy_v1_dec']
                    ResRec['anisotropy_v3_eta_inc']=ResRec['anisotropy_v1_inc']
                    ResRec['anisotropy_v3_zeta_dec']=ResRec['anisotropy_v2_dec']
                    ResRec['anisotropy_v3_zeta_inc']=ResRec['anisotropy_v2_inc']
                    ResRec["anisotropy_v1_eta_semi_angle"]='%7.1f'%(hpars['e12'])
                    ResRec["anisotropy_v1_zeta_semi_angle"]='%7.1f'%(hpars['e13'])
                    ResRec["anisotropy_v2_eta_semi_angle"]='%7.1f'%(hpars['e12'])
                    ResRec["anisotropy_v2_zeta_semi_angle"]='%7.1f'%(hpars['e23'])
                    ResRec["anisotropy_v3_eta_semi_angle"]='%7.1f'%(hpars['e13'])
                    ResRec["anisotropy_v3_zeta_semi_angle"]='%7.1f'%(hpars['e23'])
                    ResRec["result_description"]='Critical F: '+hpars["F_crit"]+';Critical F12/F13: '+hpars["F12_crit"]
                    ResRecs.append(ResRec)
                    if igeo==1:
                        sbarg=pmag.dosgeo(sbar,az,pl)
                        hparsg=pmag.dohext(9,sigma,sbarg)
                        AnisRecG=copy.copy(AnisRec)
                        ResRecG=copy.copy(ResRec)
                        AnisRecG["anisotropy_s1"]='%12.10f'%(sbarg[0])
                        AnisRecG["anisotropy_s2"]='%12.10f'%(sbarg[1])
                        AnisRecG["anisotropy_s3"]='%12.10f'%(sbarg[2])
                        AnisRecG["anisotropy_s4"]='%12.10f'%(sbarg[3])
                        AnisRecG["anisotropy_s5"]='%12.10f'%(sbarg[4])
                        AnisRecG["anisotropy_s6"]='%12.10f'%(sbarg[5])
                        AnisRecG["anisotropy_tilt_correction"]='0'
                        ResRecG["anisotropy_tilt_correction"]='0'
                        ResRecG["anisotropy_v1_dec"]='%7.1f'%(hparsg['v1_dec'])
                        ResRecG["anisotropy_v2_dec"]='%7.1f'%(hparsg['v2_dec'])
                        ResRecG["anisotropy_v3_dec"]='%7.1f'%(hparsg['v3_dec'])
                        ResRecG["anisotropy_v1_inc"]='%7.1f'%(hparsg['v1_inc'])
                        ResRecG["anisotropy_v2_inc"]='%7.1f'%(hparsg['v2_inc'])
                        ResRecG["anisotropy_v3_inc"]='%7.1f'%(hparsg['v3_inc'])
                        ResRecG['anisotropy_v1_eta_dec']=ResRecG['anisotropy_v2_dec']
                        ResRecG['anisotropy_v1_eta_inc']=ResRecG['anisotropy_v2_inc']
                        ResRecG['anisotropy_v1_zeta_dec']=ResRecG['anisotropy_v3_dec']
                        ResRecG['anisotropy_v1_zeta_inc']=ResRecG['anisotropy_v3_inc']
                        ResRecG['anisotropy_v2_eta_dec']=ResRecG['anisotropy_v1_dec']
                        ResRecG['anisotropy_v2_eta_inc']=ResRecG['anisotropy_v1_inc']
                        ResRecG['anisotropy_v2_zeta_dec']=ResRecG['anisotropy_v3_dec']
                        ResRecG['anisotropy_v2_zeta_inc']=ResRecG['anisotropy_v3_inc']
                        ResRecG['anisotropy_v3_eta_dec']=ResRecG['anisotropy_v1_dec']
                        ResRecG['anisotropy_v3_eta_inc']=ResRecG['anisotropy_v1_inc']
                        ResRecG['anisotropy_v3_zeta_dec']=ResRecG['anisotropy_v2_dec']
                        ResRecG['anisotropy_v3_zeta_inc']=ResRecG['anisotropy_v2_inc']
                        ResRecG["result_description"]='Critical F: '+hpars["F_crit"]+';Critical F12/F13: '+hpars["F12_crit"]
                        ResRecs.append(ResRecG)
                        AnisRecs.append(AnisRecG)
                    if itilt==1:
                        sbart=pmag.dostilt(sbarg,bed_az,bed_dip)
                        hparst=pmag.dohext(9,sigma,sbart)
                        AnisRecT=copy.copy(AnisRec)
                        ResRecT=copy.copy(ResRec)
                        AnisRecT["anisotropy_s1"]='%12.10f'%(sbart[0])
                        AnisRecT["anisotropy_s2"]='%12.10f'%(sbart[1])
                        AnisRecT["anisotropy_s3"]='%12.10f'%(sbart[2])
                        AnisRecT["anisotropy_s4"]='%12.10f'%(sbart[3])
                        AnisRecT["anisotropy_s5"]='%12.10f'%(sbart[4])
                        AnisRecT["anisotropy_s6"]='%12.10f'%(sbart[5])
                        AnisRecT["anisotropy_tilt_correction"]='100'
                        ResRecT["anisotropy_v1_dec"]='%7.1f'%(hparst['v1_dec'])
                        ResRecT["anisotropy_v2_dec"]='%7.1f'%(hparst['v2_dec'])
                        ResRecT["anisotropy_v3_dec"]='%7.1f'%(hparst['v3_dec'])
                        ResRecT["anisotropy_v1_inc"]='%7.1f'%(hparst['v1_inc'])
                        ResRecT["anisotropy_v2_inc"]='%7.1f'%(hparst['v2_inc'])
                        ResRecT["anisotropy_v3_inc"]='%7.1f'%(hparst['v3_inc'])
                        ResRecT['anisotropy_v1_eta_dec']=ResRecT['anisotropy_v2_dec']
                        ResRecT['anisotropy_v1_eta_inc']=ResRecT['anisotropy_v2_inc']
                        ResRecT['anisotropy_v1_zeta_dec']=ResRecT['anisotropy_v3_dec']
                        ResRecT['anisotropy_v1_zeta_inc']=ResRecT['anisotropy_v3_inc']
                        ResRecT['anisotropy_v2_eta_dec']=ResRecT['anisotropy_v1_dec']
                        ResRecT['anisotropy_v2_eta_inc']=ResRecT['anisotropy_v1_inc']
                        ResRecT['anisotropy_v2_zeta_dec']=ResRecT['anisotropy_v3_dec']
                        ResRecT['anisotropy_v2_zeta_inc']=ResRecT['anisotropy_v3_inc']
                        ResRecT['anisotropy_v3_eta_dec']=ResRecT['anisotropy_v1_dec']
                        ResRecT['anisotropy_v3_eta_inc']=ResRecT['anisotropy_v1_inc']
                        ResRecT['anisotropy_v3_zeta_dec']=ResRecT['anisotropy_v2_dec']
                        ResRecT['anisotropy_v3_zeta_inc']=ResRecT['anisotropy_v2_inc']
                        ResRecT["anisotropy_tilt_correction"]='100'
                        ResRecT["result_description"]='Critical F: '+hpars["F_crit"]+';Critical F12/F13: '+hpars["F12_crit"]
                        ResRecs.append(ResRecT)
                        AnisRecs.append(AnisRecT)
                    k15,linecnt=[],0
                    MeasRec,SpecRec,SampRec,SiteRec,AnisRec={},{},{},{},{}
    pmag.magic_write(sampfile,SampRecs,'er_samples')
    pmag.magic_write(aniso_outfile,AnisRecs,'rmag_anisotropy')
    pmag.magic_write(result_file,ResRecs,'rmag_results')
    pmag.magic_write(measfile,MeasRecs,'magic_measurements')
    print "Data saved to: ",sampfile,aniso_outfile,result_file,measfile
    return True, measfile


def SUFAR4_magic(ascfile, meas_output='magic_measurements.txt', aniso_output='rmag_anisotropy.txt', spec_infile=None, spec_outfile='er_specimens.txt', samp_outfile='er_samples.txt', site_outfile='er_sites.txt', specnum=0, sample_naming_con='1', user="", locname="unknown", instrument='', static_15_position_mode=False, output_dir_path='.', input_dir_path='.'):
    """
    NAME
        sufar4-asc_magic.py

    DESCRIPTION
        converts ascii files generated by SUFAR ver.4.0 to MagIC formated
        files for use with PmagPy plotting software

    SYNTAX
        sufar4-asc_magic.py -h [command line options]

    OPTIONS
        -h: prints the help message and quits
        -f FILE: specify .asc input file name
        -fsi SINFILE: specify er_specimens input file with location, sample, site, etc. information
        -F MFILE: specify magic_measurements output file
        -Fa AFILE: specify rmag_anisotropy output file
        -Fr RFILE: specify rmag_results output file
        -Fsi SFILE: specify er_specimens output file
        -usr USER: specify who made the measurements
        -loc LOC: specify location name for study
        -ins INST: specify instrument used
        -spc SPEC: specify number of characters to specify specimen from sample
        -ncn NCON:  specify naming convention: default is #2 below
        -k15 : specify static 15 position mode - default is spinning
        -new : replace all existing magic files

    DEFAULTS
        AFILE: rmag_anisotropy.txt
        RFILE: rmag_results.txt
        SFILE: default is to create new er_specimen.txt file
        USER: ""
        LOC: "unknown"
        INST: ""
        SPEC: 0  sample name is same as site (if SPEC is 1, sample is all but last character)
        appends to  'er_specimens.txt, er_samples.txt, er_sites.txt' files
       Sample naming convention:
            [1] XXXXY: where XXXX is an arbitrary length site designation and Y
                is the single character sample designation.  e.g., TG001a is the
                first sample from site TG001.    [default]
            [2] XXXX-YY: YY sample from site XXXX (XXX, YY of arbitary length)
            [3] XXXX.YY: YY sample from site XXXX (XXX, YY of arbitary length)
            [4-Z] XXXX[YYY]:  YYY is sample designation with Z characters from site XXX
            [5] site name same as sample
            [6] site name entered in site_name column in the orient.txt format input file  -- NOT CURRENTLY SUPPORTED
            [7-Z] [XXXX]YYY:  XXXX is site designation with Z characters with sample name XXXXYYYY
            NB: all others you will have to customize your self
                 or e-mail ltauxe@ucsd.edu for help.
            [8] This is a synthetic
            [9] ODP naming convention

    """

    citation='This study'
    cont=0
    Z=1
    AniRecSs,AniRecs,SpecRecs,SampRecs,SiteRecs,MeasRecs=[],[],[],[],[],[]
    isspec='0'
    spin=0

    ascfile = os.path.join(input_dir_path, ascfile)
    aniso_output = os.path.join(output_dir_path, aniso_output)
    #rmag_output = os.path.join(output_dir_path, 'rmag_results.txt') -- initialized but not used
    meas_output = os.path.join(output_dir_path, meas_output)

    spec_outfile = os.path.join(output_dir_path, spec_outfile)
    samp_outfile = os.path.join(output_dir_path, samp_outfile)
    site_outfile = os.path.join(output_dir_path, site_outfile)

    if "4" in sample_naming_con:
        if "-" not in sample_naming_con:
            print "option [4] must be in form 4-Z where Z is an integer"
            return False, "option [4] must be in form 4-Z where Z is an integer"
        else:
            Z=sample_naming_con.split("-")[1]
            sample_naming_con="4"
    if "7" in sample_naming_con:
        if "-" not in sample_naming_con:
            print "option [7] must be in form 7-Z where Z is an integer"
            return False, "option [7] must be in form 7-Z where Z is an integer"
        else:
            Z=sample_naming_con.split("-")[1]
            sample_naming_con="7"

    if static_15_position_mode:
        spin=0

    if spec_infile:
        if os.path.isfile(os.path.join(input_dir_path, str(spec_infile))):
            isspec='1' # means an er_specimens.txt file has been provided with sample, site, location (etc.) info

    specnum=int(specnum)

    if isspec=="1":
        specs,file_type=pmag.magic_read(spec_infile)

    specnames,sampnames,sitenames=[],[],[]
    #if '-new' not in sys.argv: # see if there are already specimen,sample, site files lying around
    #    try:
    #        SpecRecs,file_type=pmag.magic_read(input_dir_path+'/er_specimens.txt')
    #        for spec in SpecRecs:
    #            if spec['er_specimen_name'] not in specnames:
    #                specnames.append(samp['er_specimen_name'])
    #    except:
    #        SpecRecs,specs=[],[]
    #    try:
    #        SampRecs,file_type=pmag.magic_read(input_dir_path+'/er_samples.txt')
    #        for samp in SampRecs:
    #            if samp['er_sample_name'] not in sampnames:sampnames.append(samp['er_sample_name'])
    #    except:
    #        sampnames,SampRecs=[],[]
    #    try:
    #        SiteRecs,file_type=pmag.magic_read(input_dir_path+'/er_sites.txt')
    #        for site in SiteRecs:
    #            if site['er_site_names'] not in sitenames:sitenames.append(site['er_site_name'])
    #    except:
    #        sitenames,SiteRecs=[],[]

    try:
        file_input=open(ascfile,'rU')
    except:
        print 'Error opening file: ', ascfile
        return False, 'Error opening file: {}'.format(ascfile)
    Data=file_input.readlines()
    k=0
    while k<len(Data):
        line = Data[k]
        words=line.split()
        if "ANISOTROPY" in words: # first line of data for the spec
            MeasRec,AniRec,SpecRec,SampRec,SiteRec={},{},{},{},{}
            specname=words[0]
            AniRec['er_specimen_name']=specname
            if isspec=="1":
                for spec in specs:
                    if spec['er_specimen_name']==specname:
                        AniRec['er_sample_name']=spec['er_sample_name']
                        AniRec['er_site_name']=spec['er_site_name']
                        AniRec['er_location_name']=spec['er_location_name']
                        break
            elif isspec=="0":
                if specnum!=0:
                    sampname=specname[:-specnum]
                else:
                    sampname=specname
                AniRec['er_sample_name']=sampname
                SpecRec['er_specimen_name']=specname
                SpecRec['er_sample_name']=sampname
                SampRec['er_sample_name']=sampname
                SiteRec['er_sample_name']=sampname
                SiteRec['site_description']='s'
                if sample_naming_con!="9":
                    AniRec['er_site_name']=pmag.parse_site(AniRec['er_sample_name'],sample_naming_con,Z)
                    SpecRec['er_site_name']=pmag.parse_site(AniRec['er_sample_name'],sample_naming_con,Z)
                    SampRec['er_site_name']=pmag.parse_site(AniRec['er_sample_name'],sample_naming_con,Z)
                    SiteRec['er_site_name']=pmag.parse_site(AniRec['er_sample_name'],sample_naming_con,Z)
                else:
                    AniRec['er_site_name']=specname
                    SpecRec['er_site_name']=specname
                    SampRec['er_site_name']=specname
                    SiteRec['er_site_name']=specname
                    pieces=specname.split('-')
                    AniRec['er_expedition_name']=pieces[0]
                    SpecRec['er_expedition_name']=pieces[0]
                    SampRec['er_expedition_name']=pieces[0]
                    SiteRec['er_expedition_name']=pieces[0]
                    location=pieces[1]
                AniRec['er_location_name']=locname
                SpecRec['er_location_name']=locname
                SampRec['er_location_name']=locname
                SiteRec['er_location_name']=locname
                AniRec['er_citation_names']="This study"
                SpecRec['er_citation_names']="This study"
                SampRec['er_citation_names']="This study"
                SiteRec['er_citation_names']="This study"
            AniRec['er_citation_names']="This study"
            AniRec['magic_instrument_codes']=instrument
            AniRec['magic_method_codes']="LP-X:AE-H:LP-AN-MS"
            AniRec['magic_experiment_names']=specname+":"+"LP-AN-MS"
            AniRec['er_analyst_mail_names']=user
            for key in AniRec.keys():MeasRec[key]=AniRec[key]
            MeasRec['measurement_flag']='g'
            AniRec['anisotropy_flag']='g'
            MeasRec['measurement_standard']='u'
            MeasRec['measurement_description']='Bulk sucsecptibility measurement'
            AniRec['anisotropy_type']="AMS"
            AniRec['anisotropy_unit']="Normalized by trace"
            if spin==1:
                AniRec['anisotropy_n']="192"
            else:
                AniRec['anisotropy_n']="15"
        if 'Azi' in words and isspec=='0':
            SampRec['sample_azimuth']=words[1]
            labaz=float(words[1])
        if 'Dip' in words:
            SampRec['sample_dip']='%7.1f'%(-float(words[1]))
            SpecRec['specimen_vol']='%8.3e'%(float(words[10])*1e-6) # convert actual volume to m^3 from cm^3
            labdip=float(words[1])
        if 'T1' in words and 'F1' in words:
            k+=2 # read in fourth line down
            line=Data[k]
            rec=line.split()
            dd=rec[1].split('/')
            dip_direction=int(dd[0])+90
            SampRec['sample_bed_dip_direction']='%i'%(dip_direction)
            SampRec['sample_bed_dip']=dd[1]
            bed_dip=float(dd[1])
        if "Mean" in words:
            k+=4 # read in fourth line down
            line=Data[k]
            rec=line.split()
            MeasRec['measurement_chi_volume']=rec[1]
            sigma=.01*float(rec[2])/3.
            AniRec['anisotropy_sigma']='%7.4f'%(sigma)
            AniRec['anisotropy_unit']='SI'
        if "factors" in words:
            k+=4 # read in second line down
            line=Data[k]
            rec=line.split()
        if "Specimen" in words:  # first part of specimen data
            AniRec['anisotropy_s1']='%7.4f'%(float(words[5])/3.) # eigenvalues sum to unity - not 3
            AniRec['anisotropy_s2']='%7.4f'%(float(words[6])/3.)
            AniRec['anisotropy_s3']='%7.4f'%(float(words[7])/3.)
            k+=1
            line=Data[k]
            rec=line.split()
            AniRec['anisotropy_s4']='%7.4f'%(float(rec[5])/3.) # eigenvalues sum to unity - not 3
            AniRec['anisotropy_s5']='%7.4f'%(float(rec[6])/3.)
            AniRec['anisotropy_s6']='%7.4f'%(float(rec[7])/3.)
            AniRec['anisotropy_tilt_correction']='-1'
            AniRecs.append(AniRec)
            AniRecG,AniRecT={},{}
            for key in AniRec.keys():AniRecG[key]=AniRec[key]
            for key in AniRec.keys():AniRecT[key]=AniRec[key]
            sbar=[]
            sbar.append(float(AniRec['anisotropy_s1']))
            sbar.append(float(AniRec['anisotropy_s2']))
            sbar.append(float(AniRec['anisotropy_s3']))
            sbar.append(float(AniRec['anisotropy_s4']))
            sbar.append(float(AniRec['anisotropy_s5']))
            sbar.append(float(AniRec['anisotropy_s6']))
            sbarg=pmag.dosgeo(sbar,labaz,labdip)
            AniRecG["anisotropy_s1"]='%12.10f'%(sbarg[0])
            AniRecG["anisotropy_s2"]='%12.10f'%(sbarg[1])
            AniRecG["anisotropy_s3"]='%12.10f'%(sbarg[2])
            AniRecG["anisotropy_s4"]='%12.10f'%(sbarg[3])
            AniRecG["anisotropy_s5"]='%12.10f'%(sbarg[4])
            AniRecG["anisotropy_s6"]='%12.10f'%(sbarg[5])
            AniRecG["anisotropy_tilt_correction"]='0'
            AniRecs.append(AniRecG)
            if bed_dip!="" and bed_dip!=0: # have tilt correction
                sbart=pmag.dostilt(sbarg,dip_direction,bed_dip)
                AniRecT["anisotropy_s1"]='%12.10f'%(sbart[0])
                AniRecT["anisotropy_s2"]='%12.10f'%(sbart[1])
                AniRecT["anisotropy_s3"]='%12.10f'%(sbart[2])
                AniRecT["anisotropy_s4"]='%12.10f'%(sbart[3])
                AniRecT["anisotropy_s5"]='%12.10f'%(sbart[4])
                AniRecT["anisotropy_s6"]='%12.10f'%(sbart[5])
                AniRecT["anisotropy_tilt_correction"]='100'
                AniRecs.append(AniRecT)
            MeasRecs.append(MeasRec)
            if SpecRec['er_specimen_name'] not in specnames:
                SpecRecs.append(SpecRec)
                specnames.append(SpecRec['er_specimen_name'])
            if SampRec['er_sample_name'] not in sampnames:
                SampRecs.append(SampRec)
                sampnames.append(SampRec['er_sample_name'])
            if SiteRec['er_site_name'] not in sitenames:
                SiteRecs.append(SiteRec)
                sitenames.append(SiteRec['er_site_name'])
        k+=1 # skip to next specimen
    pmag.magic_write(aniso_output,AniRecs,'rmag_anisotropy')
    print "anisotropy tensors put in ",aniso_output
    pmag.magic_write(meas_output,MeasRecs,'magic_measurements')
    print "bulk measurements put in ",meas_output
    #if isspec=="0":
    SpecOut,keys=pmag.fillkeys(SpecRecs)
    #output = output_dir_path+"/er_specimens.txt"
    pmag.magic_write(spec_outfile,SpecOut,'er_specimens')
    print "specimen info put in ", spec_outfile
    #output = output_dir_path+"/er_samples.txt"
    SampOut,keys=pmag.fillkeys(SampRecs)
    pmag.magic_write(samp_outfile,SampOut,'er_samples')
    print "sample info put in ", samp_outfile
    #output = output_dir_path+"/er_sites.txt"
    SiteOut,keys=pmag.fillkeys(SiteRecs)
    pmag.magic_write(site_outfile,SiteOut,'er_sites')
    print "site info put in ", site_outfile
    return True, meas_output


def agm_magic(agm_file, samp_infile=None, outfile='agm_measurements.txt', spec_outfile='er_specimens.txt', user="", input_dir_path='.', output_dir_path='.', backfield_curve=False, specnum=0, samp_con='1', er_location_name='unknown', units='cgs', er_specimen_name='', fmt='old', inst='', synthetic=False):
    """
    NAME
        agm_magic.py

    DESCRIPTION
        converts Micromag agm files to magic format

    SYNTAX
        agm_magic.py [-h] [command line options]

    OPTIONS
        -usr USER:   identify user, default is "" - put in quotation marks!
        -bak:  this is a IRM backfield curve
        -f FILE, specify input file, required
        -fsa SAMPFILE, specify er_samples.txt file relating samples, site and locations names,default is none
        -F MFILE, specify magic measurements formatted output file, default is agm_measurements.txt
        -spn SPEC, specimen name, default is base of input file name, e.g. SPECNAME.agm
        -spc NUM, specify number of characters to designate a  specimen, default = 0
        -Fsp SPECFILE : name of er_specimens.txt file for appending data to
             [default: er_specimens.txt]
        -ncn NCON,: specify naming convention: default is #1 below
        -syn SYN,  synthetic specimen name
        -loc LOCNAME : specify location/study name,
             should have either LOCNAME or SAMPFILE (unless synthetic)
        -ins INST : specify which instrument was used (e.g, SIO-Maud), default is ""
        -u units:  [cgs,SI], default is cgs
       Sample naming convention:
            [1] XXXXY: where XXXX is an arbitrary length site designation and Y
                is the single character sample designation.  e.g., TG001a is the
                first sample from site TG001.    [default]
            [2] XXXX-YY: YY sample from site XXXX (XXX, YY of arbitary length)
            [3] XXXX.YY: YY sample from site XXXX (XXX, YY of arbitary length)
            [4-Z] XXXX[YYY]:  YYY is sample designation with Z characters from site XXX
            [5] site name same as sample
            [6] site name entered in site_name column in the orient.txt format input file  -- NOT CURRENTLY SUPPORTED
            [7-Z] [XXXX]YYY:  XXXX is site designation with Z characters with sample name XXXXYYYY
            [8] specimen is a synthetic - it has no sample, site, location information
            NB: all others you will have to customize your self
                 or e-mail ltauxe@ucsd.edu for help.

    OUTPUT
        MagIC format files: magic_measurements, er_specimens, er_sample, er_site
    """
    #return False, 'fake error message'
    citation='This study'
    MeasRecs=[]
    meth="LP-HYS"
    version_num=pmag.get_version()
    er_sample_name, er_site_name = "", ""
    Z = 1
    if backfield_curve:
        meth="LP-IRM-DCD"
        #outfile = "irm_measurements.txt"
    output = os.path.join(output_dir_path, outfile)
    specfile = os.path.join(output_dir_path, spec_outfile)

    # if specimen name is not provided, use the name of the file minus the file extension
    if not er_specimen_name:
        er_specimen_name = agm_file.split('.')[0]
    agm_file= os.path.join(input_dir_path, agm_file)
    if not os.path.isfile(agm_file):
        return False,  'You must provide a valid agm file'

    if synthetic:
        er_synthetic_name = synthetic
        er_specimen_name = ""
    else:
        er_synthetic_name = ''

    if samp_infile:
        samp_infile = os.path.join(input_dir_path, samp_infile)
        Samps,file_type=pmag.magic_read(samp_infile)
        print 'sample_file successfully read in'


    # validate some things
    if "4" in samp_con:
        if "-" not in samp_con:
            print "option [4] must be in form 4-Z where Z is an integer"
            return False, "option [4] must be in form 4-Z where Z is an integer"
        else:
            Z=samp_con.split("-")[1]
            samp_con="4"
    if "7" in samp_con:
        if "-" not in samp_con:
            print "option [7] must be in form 7-Z where Z is an integer"
            return False, "option [7] must be in form 7-Z where Z is an integer"
        else:
            Z=samp_con.split("-")[1]
            samp_con="7"

    # read in the data
    ErSpecRecs,filetype=pmag.magic_read(specfile)
    ErSpecRec,MeasRec={},{}
    ErSpecRec['er_citation_names']="This study"
    ErSpecRec['er_specimen_name']=er_specimen_name
    ErSpecRec['er_synthetic_name']=er_synthetic_name
    if specnum!=0:
        ErSpecRec["er_sample_name"]=er_specimen_name[:-specnum]
    else:
        ErSpecRec["er_sample_name"]=er_specimen_name
    if samp_infile and er_synthetic_name=="":
        for samp in Samps:
            if samp["er_sample_name"] == ErSpecRec["er_sample_name"]:
                ErSpecRec["er_location_name"]=samp["er_location_name"]
                ErSpecRec["er_site_name"]=samp["er_site_name"]
                break
    elif int(samp_con)!=6 and int(samp_con)!=8:
        site=pmag.parse_site(ErSpecRec['er_sample_name'],samp_con,Z)
        ErSpecRec["er_site_name"]=site
        ErSpecRec["er_location_name"]=er_location_name
    ErSpecRec['er_scientist_mail_names']=user.strip()
    insert=1
    for rec in ErSpecRecs:
        if rec['er_specimen_name']==er_specimen_name:
            insert=0
            break
    if insert==1:
        ErSpecRecs.append(ErSpecRec)
        ErSpecRecs,keylist=pmag.fillkeys(ErSpecRecs)
        pmag.magic_write(specfile,ErSpecRecs,'er_specimens')
        print "specimen name put in ",specfile
    f=open(agm_file,'rU')
    Data=f.readlines()
    if "ASCII" not in Data[0]:
        fmt='new'
    measnum,start,end=1,"",1
    if fmt=='new': # new Micromag formatted file
        end=2
        for skip in range(len(Data)):
            line=Data[skip]
            rec=line.split()
            if 'Units' in line:
                units=rec[-1]
            if "Raw" in rec:
                start=skip+2
            if "Field" in rec and "Moment" in rec and start=="":
                start=skip+2
                break
            if "Field" in rec and "Remanence" in rec and start=="":
                start=skip+2
                break
    else:
        start = 2
        end=1
    for i in range(start,len(Data)-end): # skip header stuff
        MeasRec={}
        for key in ErSpecRec.keys():
            MeasRec[key]=ErSpecRec[key]
        MeasRec['magic_instrument_codes']=inst
        MeasRec['magic_method_codes']=meth
        if 'er_synthetic_name' in MeasRec.keys() and MeasRec['er_synthetic_name']!="":
            MeasRec['magic_experiment_name']=er_synthetic_name+':'+meth
        else:
            MeasRec['magic_experiment_name']=er_specimen_name+':'+meth
        line=Data[i]
        rec=line.split(',') # data comma delimited
        if rec[0]!='\n':
            if units=='cgs':
                field =float(rec[0])*1e-4 # convert from oe to tesla
            else:
                field =float(rec[0]) # field in tesla
            if meth=="LP-HYS":
                MeasRec['measurement_lab_field_dc']='%10.3e'%(field)
                MeasRec['treatment_dc_field']=''
            else:
                MeasRec['measurement_lab_field_dc']=''
                MeasRec['treatment_dc_field']='%10.3e'%(field)
            if units=='cgs':
                MeasRec['measurement_magn_moment']='%10.3e'%(float(rec[1])*1e-3) # convert from emu to Am^2
            else:
                MeasRec['measurement_magn_moment']='%10.3e'%(float(rec[1])) # Am^2
            MeasRec['treatment_temp']='273' # temp in kelvin
            MeasRec['measurement_temp']='273' # temp in kelvin
            MeasRec['measurement_flag']='g'
            MeasRec['measurement_standard']='u'
            MeasRec['measurement_number']='%i'%(measnum)
            measnum+=1
            MeasRec['magic_software_packages']=version_num
            MeasRecs.append(MeasRec)
# now we have to relabel LP-HYS method codes.  initial loop is LP-IMT, minor loops are LP-M  - do this in measurements_methods function
    if meth=='LP-HYS':
        recnum=0
        while float(MeasRecs[recnum]['measurement_lab_field_dc'])<float(MeasRecs[recnum+1]['measurement_lab_field_dc']) and recnum+1<len(MeasRecs): # this is LP-IMAG
            MeasRecs[recnum]['magic_method_codes']='LP-IMAG'
            MeasRecs[recnum]['magic_experiment_name']=MeasRecs[recnum]['er_specimen_name']+":"+'LP-IMAG'
            recnum+=1
#
    pmag.magic_write(output,MeasRecs,'magic_measurements')
    print "results put in ",output
    return True, output


def read_core_csv_file(sum_file):
    Cores=[]
    core_depth_key="Top depth cored CSF (m)"
    if os.path.isfile(sum_file):
        input=open(sum_file,'rU').readlines()
        if "Core Summary" in input[0]:
            headline=1
        else:
            headline=0
        keys=input[headline].replace('\n','').split(',')
        if "Core Top (m)" in keys:
            core_depth_key="Core Top (m)"
        if "Top depth cored CSF (m)" in keys:
            core_dpeth_key="Top depth cored CSF (m)"
        if "Core Label" in keys:
            core_label_key="Core Label"
        if "Core label" in keys:
            core_label_key="Core label"
        for line in input[2:]:
            if 'TOTALS' not in line:
                CoreRec={}
                for k in range(len(keys)):CoreRec[keys[k]]=line.split(',')[k]
                Cores.append(CoreRec)
        if len(Cores)==0:
            print 'no Core depth information available: import core summary file'
            return False, False, []
        else:
            return core_depth_key, core_label_key, Cores
    else:
        return False, False, []


class Site(object):

    ''' This Site class is for use within Jupyter/IPython notebooks. It reads in
    MagIC-formatted data (text files) and compiles fits, separates them by type,
    and plots equal-area projections inline. If means were not taken and output
    within the Demag GUI, it should automatically compute the Fisher mean for each
    fit type. Code is still a work in progress, but it is currently useful for
    succinctly computing/displaying data in notebook format.
    '''

    def __init__(self, site_name, data_path, data_format="MagIC"):
        '''
        site_name: the name of the site
        data_path: put all MagIC data (text files) in a single directory and
        provide its path
        data_format: MagIC-formatted data is necessary in this code, but future
        compatability with other formats possible (built-in CIT_magic conversion?)
        *other keyword arguments not necessary*
        '''
        # import necessary functions to be used in the notebook
        import os
        from matplotlib import pyplot as plt
        import pandas as pd
        global pd
        global plt
        global os
        import re
        dir_name = os.path.relpath(data_path)
        self.all_file_names = os.listdir(dir_name)
        os.path.join
        self.file_names = []
        for file_name in self.all_file_names:
            if re.match('.*txt',file_name) != None:
                self.file_names.append(file_name)
        for i in self.file_names:
            path_to_open = os.path.join(dir_name,i)
            text_file = open(path_to_open,'r')
            first_line = text_file.readlines()[0]
            text_file.close()
            if 'er_sites' in first_line:
                self.er_sites_path = path_to_open
            elif 'pmag_sites' in first_line:
                self.mean_path = path_to_open
            elif 'pmag_specimens' in first_line:
                self.data_path = path_to_open
        self.name = site_name
        #self.data_path = data_path # default name of 'pmag_specimens'
        self.data_format = data_format # default name of 'pmag_sites'
        #self.mean_path = mean_path # default name of 'er_sites'
        #self.er_sites_path = er_sites_path
        if self.data_format == "MagIC":
            self.fits = pd.read_csv(self.data_path, sep = "\t", skiprows = 1)
            if self.mean_path != None:
                self.means = pd.read_csv(self.mean_path, sep = "\t", skiprows = 1)
            if self.er_sites_path != None:
                self.location = pd.read_csv(self.er_sites_path, sep = "\t", skiprows = 1)
        else:
            raise Exception("Please convert data to MagIC format")
        self.parse_all_fits()
        self.lat = float(self.location.site_lat)
        self.lon = float(self.location.site_lon)
        # the following exception won't be necessary if parse_all_fits is working properly
        if self.mean_path == None:
            raise Exception('Make fisher means within the demag GUI - functionality for handling this is in progress')


    def parse_fits(self, fit_name):
        '''USE PARSE_ALL_FITS unless otherwise necessary
        Isolate fits by the name of the fit; we also set 'specimen_tilt_correction' to zero in order
        to only include data in geographic coordinates - THIS NEEDS TO BE GENERALIZED
        '''
        fits = self.fits.ix[self.fits.specimen_comp_name==fit_name].ix[self.fits.specimen_tilt_correction==0]
        fits.reset_index(inplace=True)
        means = self.means.ix[self.means.site_comp_name==fit_name].ix[self.means.site_tilt_correction==0]
        means.reset_index(inplace=True)
        mean_name = str(fit_name) + "_mean"
        setattr(self,fit_name,fits)
        setattr(self,mean_name,means)


    def parse_all_fits(self):
        # This is run upon initialization of the Site class
        self.fit_types = self.fits.specimen_comp_name.unique().tolist()
        for fit_type in self.fit_types:
            self.parse_fits(fit_type)
        print "Data separated by ", self.fit_types, "fits and can be accessed by <site_name>.<fit_name>"


    def get_fit_names(self):
        return self.fit_types


    def get_fisher_mean(self, fit_name):
        mean_name = str(fit_name) + "_mean"
        if self.mean_path != None:
            self.fisher_dict = {'dec':float(getattr(self,mean_name).site_dec),
                                'inc':float(getattr(self,mean_name).site_inc),
                                'alpha95':float(getattr(self,mean_name).site_alpha95),
                                'k':float(getattr(self,mean_name).site_k),
                                'r':float(getattr(self,mean_name).site_r),
                                'n':float(getattr(self,mean_name).site_n)}
            return self.fisher_dict

        else:
            self.directions = []
            for fit_num in range(0,len(getattr(self,fit_name))):
                self.directions.append([list(getattr(self,fit_name).specimen_dec)[fit_num],
                                        list(getattr(self,fit_name).specimen_inc)[fit_num],1.])
            #fish_mean = pmag.fisher_mean(directions)
            self.fisher_dict = pmag.fisher_mean(self.directions)
            #setattr(self,fisher_dict,fish_mean)
            #self.fisher_dict = getattr(self,mean_name)
            return self.fisher_dict

    def get_lat(self):
        return self.lat

    def get_lon(self):
        return self.lon

    def get_site_coor(self):
        return [self.lat,self.lon]

    def get_name(self):
        return self

    def eq_plot_everything(self, title=None, clrs = None, size = (5,5), **kwargs):
        fignum = 0
        plt.figure(num=fignum,figsize=size,dpi=200)
        plot_net(fignum)
        clr_idx = 0
        for fits in self.fit_types:
            mean_code = str(fits)+"_mean"
            print mean_code
            if clrs is not None:
                plot_di(getattr(self,fits).specimen_dec,
                getattr(self,fits).specimen_inc,color=clrs[clr_idx], label=fits+' directions')
                print float(getattr(self,mean_code).site_dec),float(getattr(self,mean_code).site_inc)
                plot_di_mean(float(getattr(self,mean_code).site_dec),
                                   float(getattr(self,mean_code).site_inc),
                                   float(getattr(self,mean_code).site_alpha95),
                                   color=clrs[clr_idx],marker='s',label=fits+' mean')
                clr_idx += 1

            else:
                self.random_color = np.random.rand(3)
                plot_di(getattr(self,fits).specimen_dec,
                getattr(self,fits).specimen_inc,color=self.random_color, label=fits+' directions')
                print float(getattr(self,mean_code).site_dec),float(getattr(self,mean_code).site_inc)
                plot_di_mean(float(getattr(self,mean_code).site_dec),
                                   float(getattr(self,mean_code).site_inc),
                                   float(getattr(self,mean_code).site_alpha95),
                                   color=self.random_color,marker='s',label=fits+' mean')
        plt.legend(**kwargs)
        if title != None:
            plt.title(title)
        plt.show()

    def eq_plot(self,fit_name,title=None, clr = None, size = (5,5), **kwargs):
        fignum = 0
        plt.figure(num=fignum,figsize=size,dpi=200)
        plot_net(fignum)
        mean_code = str(fit_name)+"_mean"
        if clr is not None:
            self.random_color = clr
        else:
            self.random_color = np.random.rand(3)
        plot_di(getattr(self,fit_name).specimen_dec,
                      getattr(self,fit_name).specimen_inc,
                      color=self.random_color,label=fit_name+' directions')
        plot_di_mean(float(getattr(self,mean_code).site_dec),
                           float(getattr(self,mean_code).site_inc),
                           float(getattr(self,mean_code).site_alpha95), marker='s', label=fit_name+' mean')
        plt.legend(**kwargs)
        if title != None:
            plt.title(title)
        plt.show()

    # def eq_plot_sidebyside(self, fit_name):
    #     fig,ax = plt.subplots(1,2)
    #     ax[0].plot(self.eq_plot_everything())
    #     ax[1].plot(self.eq_plot(fit_name))
    #     plt.show()

    def get_site_data(self, description, fit_name,demag_type = 'Thermal',cong_test_result = None):
        self.site_data = pd.Series({'site_type':str(description),
                                   'site_lat':self.get_lat(),
                                   'site_lon':self.get_lon(),
                                   'demag_type':demag_type,
                                   'dec':float(self.get_fisher_mean(fit_name)['dec']),
                                   'inc':float(self.get_fisher_mean(fit_name)['inc']),
                                   'a_95':float(self.get_fisher_mean(fit_name)['alpha95']),
                                   'n':int(self.get_fisher_mean(fit_name)['n']),
                                   'kappa':float(self.get_fisher_mean(fit_name)['k']),
                                   'R':float(self.get_fisher_mean(fit_name)['r']),
                                    'cong_test_result':cong_test_result},
                                   name=str(self.name))
        return self.site_data


def dayplot(path_to_file = '.',hyst_file="rmag_hysteresis.txt",
            rem_file="rmag_remanence.txt", save = False, save_folder='.', fmt = 'pdf'):
    """
    Makes 'day plots' (Day et al. 1977) and squareness/coercivity plots
    (Neel, 1955; plots after Tauxe et al., 2002); plots 'linear mixing'
    curve from Dunlop and Carter-Stiglitz (2006).

    Optional Parameters (defaults are used if not specified)
    ----------
    path_to_file : path to directory that contains files (default is current directory, '.')
    hyst_file : hysteresis file (default is 'rmag_hysteresis.txt')
    rem_file : remanence file (default is 'rmag_remanence.txt')
    save : boolean argument to save plots (default is False)
    save_folder : relative directory where plots will be saved (default is current directory, '.')
    fmt : format of saved figures (default is 'pdf')
    """
    args=sys.argv
    hyst_path = os.path.join(path_to_file,hyst_file)
    rem_path = os.path.join(path_to_file,rem_file)
    #hyst_file,rem_file="rmag_hysteresis.txt","rmag_remanence.txt"
    dir_path = path_to_file
    verbose=pmagplotlib.verbose
    # initialize some variables
    # define figure numbers for Day,S-Bc,S-Bcr
    DSC={}
    DSC['day'],DSC['S-Bc'],DSC['S-Bcr'],DSC['bcr1-bcr2']=1,2,3,4
    plt.figure(num=DSC['day'],figsize=(5,5));
    plt.figure(num=DSC['S-Bc'],figsize=(5,5));
    plt.figure(num=DSC['S-Bcr'],figsize=(5,5));
    plt.figure(num=DSC['bcr1-bcr2'],figsize=(5,5));
    hyst_data,file_type=pmag.magic_read(hyst_path)
    rem_data,file_type=pmag.magic_read(rem_path)
    S,BcrBc,Bcr2,Bc,hsids,Bcr=[],[],[],[],[],[]
    Ms,Bcr1,Bcr1Bc,S1=[],[],[],[]
    locations=''
    for rec in  hyst_data:
        if 'er_location_name' in rec.keys() and rec['er_location_name'] not in locations: locations=locations+rec['er_location_name']+'_'
        if rec['hysteresis_bcr'] !="" and rec['hysteresis_mr_moment']!="":
            S.append(float(rec['hysteresis_mr_moment'])/float(rec['hysteresis_ms_moment']))
            Bcr.append(float(rec['hysteresis_bcr']))
            Bc.append(float(rec['hysteresis_bc']))
            BcrBc.append(Bcr[-1]/Bc[-1])
            if 'er_synthetic_name' in rec.keys() and rec['er_synthetic_name']!="":
                rec['er_specimen_name']=rec['er_synthetic_name']
            hsids.append(rec['er_specimen_name'])
    if len(rem_data)>0:
        for rec in  rem_data:
            if rec['remanence_bcr'] !="" and float(rec['remanence_bcr'])>0:
                try:
                    ind=hsids.index(rec['er_specimen_name'])
                    Bcr1.append(float(rec['remanence_bcr']))
                    Bcr1Bc.append(Bcr1[-1]/Bc[ind])
                    S1.append(S[ind])
                    Bcr2.append(Bcr[ind])
                except ValueError:
                    if verbose:print 'hysteresis data for ',rec['er_specimen_name'],' not found'
    #
    # now plot the day and S-Bc, S-Bcr plots
    #
    leglist=[]
    if len(Bcr1)>0:
        pmagplotlib.plotDay(DSC['day'],Bcr1Bc,S1,'ro')
        pmagplotlib.plotSBcr(DSC['S-Bcr'],Bcr1,S1,'ro')
        pmagplotlib.plot_init(DSC['bcr1-bcr2'],5,5)
        pmagplotlib.plotBcr(DSC['bcr1-bcr2'],Bcr1,Bcr2)
        plt.show()
    else:
        del DSC['bcr1-bcr2']
    if save==True:
        pmagplotlib.plotDay(DSC['day'],BcrBc,S,'bs')
        plt.savefig(os.path.join(save_folder,'Day.' + fmt))
        pmagplotlib.plotSBcr(DSC['S-Bcr'],Bcr,S,'bs')
        plt.savefig(os.path.join(save_folder,'S-Bcr.' + fmt))
        pmagplotlib.plotSBc(DSC['S-Bc'],Bc,S,'bs')
        plt.savefig(os.path.join(save_folder,'S-Bc.' + fmt))
    else:
        pmagplotlib.plotDay(DSC['day'],BcrBc,S,'bs')
        pmagplotlib.plotSBcr(DSC['S-Bcr'],Bcr,S,'bs')
        pmagplotlib.plotSBc(DSC['S-Bc'],Bc,S,'bs')
        plt.show()


def smooth(x,window_len,window='bartlett'):
    """
    Smooth the data using a sliding window with requested size - meant to be
    used with the ipmag function curie().
    This method is based on the convolution of a scaled window with the signal.
    The signal is prepared by padding the beginning and the end of the signal
    with average of the first (last) ten values of the signal, to evoid jumps
    at the beggining/end. Output is an array of the smoothed signal.

    Required Parameters
    ----------
    x : the input signal, equaly spaced!
    window_len : the dimension of the smoothing window

    Optional Parameters (defaults are used if not specified)
    ----------
    window : type of window from numpy library ['flat','hanning','hamming','bartlett','blackman']
        (default is Bartlett)
        -flat window will produce a moving average smoothing.
        -Bartlett window is very similar to triangular window,
            but always ends with zeros at points 1 and n.
        -hanning,hamming,blackman are used for smoothing the Fourier transfrom
    """

    if x.ndim != 1:
        raise ValueError, "smooth only accepts 1 dimension arrays."

    if x.size < window_len:
        raise ValueError, "Input vector needs to be bigger than window size."

    if window_len<3:
        return x

    # numpy available windows
    if not window in ['flat', 'hanning', 'hamming', 'bartlett', 'blackman']:
        raise ValueError, "Window is on of 'flat', 'hanning', 'hamming', 'bartlett', 'blackman'"

    # padding the beggining and the end of the signal with an average value to evoid edge effect
    start=[np.average(x[0:10])]*window_len
    end=[np.average(x[-10:])]*window_len
    s=start+list(x)+end


    #s=numpy.r_[2*x[0]-x[window_len:1:-1],x,2*x[-1]-x[-1:-window_len:-1]]
    if window == 'flat': #moving average
        w=ones(window_len,'d')
    else:
        w=eval('np.'+window+'(window_len)')
    y=np.convolve(w/w.sum(),s,mode='same')
    return np.array(y[window_len:-window_len])



def deriv1(x,y,i,n):
    """
    Alternative way to smooth the derivative of a noisy signal
    using least square fit. In this method the slope in position
    'i' is calculated by least square fit of 'n' points before
    and after position.

    Required Parameters
    ----------
    x : array of x axis
    y : array of y axis
    n : smoothing factor
    i : position
    """
    m_,x_,y_,xy_,x_2=0.,0.,0.,0.,0.
    for ix in range(i,i+n,1):
        x_=x_+x[ix]
        y_=y_+y[ix]
        xy_=xy_+x[ix]*y[ix]
        x_2=x_2+x[ix]**2
    m = ((n*xy_) - (x_*y_) ) / ( n*x_2-(x_)**2)
    return(m)

def curie(path_to_file = '.',file_name = 'magic_measurements.txt',
        window_length = 3, save = False, save_folder = '.', fmt = 'svg'):
    """
    Plots and interprets curie temperature data.
    ***
    The 1st derivative is calculated from smoothed M-T curve (convolution
    with trianfular window with width= <-w> degrees)
    ***
    The 2nd derivative is calculated from smoothed 1st derivative curve
    (using the same sliding window width)
    ***
    The estimated curie temp. is the maximum of the 2nd derivative.
    Temperature steps should be in multiples of 1.0 degrees.

    Optional Parameters (defaults are used if not specified)
    ----------
    path_to_file : path to directory that contains file (default is current directory, '.')
    file_name : name of file to be opened (default is 'magic_measurements.txt')
    window_length : dimension of smoothing window (input to smooth() function)
    save : boolean argument to save plots (default is False)
    save_folder : relative directory where plots will be saved (default is current directory, '.')
    fmt : format of saved figures
    """

    plot=0
    window_len=window_length
    t_begin=''
    t_end=''

    # read data from file
    complete_path = os.path.join(path_to_file,file_name)
    Data=np.loadtxt(complete_path,dtype=np.float)
    T=Data.transpose()[0]
    M=Data.transpose()[1]
    T=list(T)
    M=list(M)
    # cut the data if -t is one of the flags
    if t_begin:
        while T[0]<t_begin:
            M.pop(0);T.pop(0)
        while T[-1]>t_end:
            M.pop(-1);T.pop(-1)


    # prepare the signal:
    # from M(T) array with unequal deltaT
    # to M(T) array with deltaT=(1 degree).
    # if delataT is larger, then points are added using linear fit between
    # consecutive data points.
    # exit if deltaT is not integer
    i=0
    while i<(len(T)-1):
        if (T[i+1]-T[i])%1>0.001:
            print "delta T should be integer, this program will not work!"
            print "temperature range:",T[i],T[i+1]
            sys.exit()
        if (T[i+1]-T[i])==0.:
            M[i]=np.average([M[i],M[i+1]])
            M.pop(i+1);T.pop(i+1)
        elif (T[i+1]-T[i])<0.:
            M.pop(i+1);T.pop(i+1)
            print "check data in T=%.0f ,M[T] is ignored"%(T[i])
        elif (T[i+1]-T[i])>1.:
            slope,b=np.polyfit([T[i],T[i+1]],[M[i],M[i+1]],1)
            for j in range(int(T[i+1])-int(T[i])-1):
                M.insert(i+1,slope*(T[i]+1.)+b)
                T.insert(i+1,(T[i]+1.))
                i=i+1
        i=i+1

    # calculate the smoothed signal
    M=np.array(M,'f')
    T=np.array(T,'f')
    M_smooth=[]
    M_smooth=smooth(M,window_len)

    #plot the original data and the smooth data
    PLT={'M_T':1,'der1':2,'der2':3,'Curie':4}
    plt.figure(num=PLT['M_T'],figsize=(5,5))
    string='M-T (sliding window=%i)'%int(window_len)
    pmagplotlib.plotXY(PLT['M_T'],T,M_smooth,sym='-')
    pmagplotlib.plotXY(PLT['M_T'],T,M,sym='--',xlab='Temperature C',ylab='Magnetization',title=string)

    #calculate first derivative
    d1,T_d1=[],[]
    for i in range(len(M_smooth)-1):
        Dy=M_smooth[i-1]-M_smooth[i+1]
        Dx=T[i-1]-T[i+1]
        d1.append(Dy/Dx)
    T_d1=T[1:len(T-1)]
    d1=np.array(d1,'f')
    d1_smooth=smooth(d1,window_len)

    #plot the first derivative
    plt.figure(num=PLT['der1'],figsize=(5,5))
    string='1st derivative (sliding window=%i)'%int(window_len)
    pmagplotlib.plotXY(PLT['der1'],T_d1,d1_smooth,sym='-',xlab='Temperature C',title=string)
    pmagplotlib.plotXY(PLT['der1'],T_d1,d1,sym='b--')

    #calculate second derivative
    d2,T_d2=[],[]
    for i in range(len(d1_smooth)-1):
        Dy=d1_smooth[i-1]-d1_smooth[i+1]
        Dx=T[i-1]-T[i+1]
        #print Dy/Dx
        d2.append(Dy/Dx)
    T_d2=T[2:len(T-2)]
    d2=np.array(d2,'f')
    d2_smooth=smooth(d2,window_len)

    #plot the second derivative
    plt.figure(num=PLT['der2'],figsize=(5,5))
    string='2nd derivative (sliding window=%i)'%int(window_len)
    pmagplotlib.plotXY(PLT['der2'],T_d2,d2,sym='-',xlab='Temperature C',title=string)
    d2=list(d2)
    print 'second derivative maximum is at T=%i'%int(T_d2[d2.index(max(d2))])

    # calculate Curie temperature for different width of sliding windows
    curie,curie_1=[],[]
    wn=range(5,50,1)
    for win in wn:
        # calculate the smoothed signal
        M_smooth=[]
        M_smooth=smooth(M,win)
        #calculate first derivative
        d1,T_d1=[],[]
        for i in range(len(M_smooth)-1):
            Dy=M_smooth[i-1]-M_smooth[i+1]
            Dx=T[i-1]-T[i+1]
            d1.append(Dy/Dx)
        T_d1=T[1:len(T-1)]
        d1=np.array(d1,'f')
        d1_smooth=smooth(d1,win)
        #calculate second derivative
        d2,T_d2=[],[]
        for i in range(len(d1_smooth)-1):
            Dy=d1_smooth[i-1]-d1_smooth[i+1]
            Dx=T[i-1]-T[i+1]
            d2.append(Dy/Dx)
        T_d2=T[2:len(T-2)]
        d2=np.array(d2,'f')
        d2_smooth=smooth(d2,win)
        d2=list(d2)
        d2_smooth=list(d2_smooth)
        curie.append(T_d2[d2.index(max(d2))])
        curie_1.append(T_d2[d2_smooth.index(max(d2_smooth))])

    #plot Curie temp for different sliding window length
    plt.figure(num=PLT['Curie'],figsize=(5,5))
    pmagplotlib.plotXY(PLT['Curie'],wn,curie,sym='.',xlab='Sliding Window Width (degrees)',ylab='Curie Temp',title='Curie Statistics')
    files = {}
    for key in PLT.keys(): files[key]=str(key) + '.' + fmt
    if save == True:
        for key in PLT.keys():
            try:
                plt.figure(num=PLT[key])
                plt.savefig(save_folder + '/' + files[key].replace('/','-'))
            except:
                print 'could not save: ',PLT[key],files[key]
                print "output file format not supported "
    plt.show()

def chi_magic(path_to_file = '.', file_name = 'magic_measurements.txt',
            save = False, save_folder = '.', fmt='svg'):
    """
    Generates plots that compare susceptibility to temperature at different
    frequencies.

    Optional Parameters (defaults are used if not specified)
    ----------
    path_to_file : path to directory that contains file (default is current directory, '.')
    file_name : name of file to be opened (default is 'magic_measurements.txt')
    save : boolean argument to save plots (default is False)
    save_folder : relative directory where plots will be saved (default is current directory, '.')
    """
    cont,FTinit,BTinit,k="",0,0,0
    complete_path = os.path.join(path_to_file,file_name)
    Tind,cont=0,""
    EXP=""
    #
    meas_data,file_type=pmag.magic_read(complete_path)
    #
    # get list of unique experiment names
    #
    # initialize some variables (a continuation flag, plot initialization flags and the experiment counter
    experiment_names=[]
    for rec in meas_data:
        if rec['magic_experiment_name'] not in experiment_names:experiment_names.append(rec['magic_experiment_name'])
    #
    # hunt through by experiment name
    if EXP!="":
        try:
            k=experiment_names.index(EXP)
        except:
            print "Bad experiment name"
            sys.exit()
    while k < len(experiment_names):
        e=experiment_names[k]
        if EXP=="":print e, k+1 , 'out of ',len(experiment_names)
    #
    #  initialize lists of data, susceptibility, temperature, frequency and field
        X,T,F,B=[],[],[],[]
        for rec in meas_data:
            methcodes=rec['magic_method_codes']
            meths=methcodes.strip().split(':')
            if rec['magic_experiment_name']==e and "LP-X" in meths: # looking for chi measurement
                if 'measurement_temp' not in rec.keys():rec['measurement_temp']='300' # set defaults
                if 'measurement_freq' not in rec.keys():rec['measurement_freq']='0' # set defaults
                if 'measurement_lab_field_ac' not in rec.keys():rec['measurement_lab_field_ac']='0' # set default
                X.append(float(rec['measurement_x']))
                T.append(float(rec['measurement_temp']))
                F.append(float(rec['measurement_freq']))
                B.append(float(rec['measurement_lab_field_ac']))
    #
    # get unique list of Ts,Fs, and Bs
    #
        Ts,Fs,Bs=[],[],[]
        for k in range(len(X)):   # hunt through all the measurements
            if T[k] not in Ts:Ts.append(T[k])  # append if not in list
            if F[k] not in Fs:Fs.append(F[k])
            if B[k] not in Bs:Bs.append(B[k])
        Ts.sort() # sort list of temperatures, frequencies and fields
        Fs.sort()
        Bs.sort()
        if '-x' in sys.argv:
            k=len(experiment_names)+1 # just plot the one
        else:
            k+=1  # increment experiment number
    #
    # plot chi versus T and F holding B constant
    #
        plotnum=1  # initialize plot number to 1
        if len(X)>2:  # if there are any data to plot, continue
            b=Bs[-1]  # keeping field constant and at maximum
            XTF=[] # initialize list of chi versus Temp and freq
            for f in Fs:   # step through frequencies sequentially
                XT=[]  # initialize list of chi versus temp
                for kk in range(len(X)): # hunt through all the data
                    if F[kk]==f and B[kk]==b:  # select data with given freq and field
                        XT.append([X[kk],T[kk]]) # append to list
                XTF.append(XT) # append list to list of frequencies
            if len(XT)>1: # if there are any temperature dependent data
                plt.figure(num=plotnum,figsize=(5,5)) # initialize plot
                pmagplotlib.plotXTF(plotnum,XTF,Fs,e,b) # call the plotting function
                pmagplotlib.showFIG(plotnum)
                plotnum+=1 # increment plot number
            f=Fs[0] # set frequency to minimum
            XTB=[] # initialize list if chi versus Temp and field
            for b in Bs:  # step through field values
                XT=[] # initial chi versus temp list for this field
                for kk in range(len(X)): # hunt through all the data
                    if F[kk]==f and B[kk]==b: # select data with given freq and field
                        XT.append([X[kk],T[kk]]) # append to list
                XTB.append(XT)
            if len(XT)>1: # if there are any temperature dependent data
                plt.figure(num=plotnum,figsize=(5,5)) # set up plot
                pmagplotlib.plotXTB(plotnum,XTB,Bs,e,f) # call the plotting function
                pmagplotlib.showFIG(plotnum)
                plotnum+=1 # increment plot number
            if save == True:
                files={}
                PLTS={}
                for p in range(1,plotnum):
                    key=str(p)
                    files[key]=e+'_'+key+'.'+fmt
                    PLTS[key]=p
                for key in PLTS.keys():
                    try:
                        plt.figure(num=PLTS[key])
                        plt.savefig(save_folder + '/' + files[key].replace('/','-'))
                    except:
                        print 'could not save: ',PLTS[key],files[key]
                        print "output file format not supported "


def pmag_results_extract(res_file="pmag_results.txt", crit_file="", spec_file="",
                         age_file="", latex=False, grade=False, WD="."):
    """
    Generate tab delimited output file(s) with result data.
    Save output files and return True if successful.
    Possible output files: Directions, Intensities, SiteNfo, Criteria,
                           Specimens

    Optional Parameters (defaults are used if not specified)
    ----------
    res_file : name of pmag_results file (default is "pmag_results.txt")
    crit_file : name of criteria file (default is "pmag_criteria.txt")
    spec_file : name of specimen file (default is "pmag_specimens.txt")
    age_file : name of age file (default is "er_ages.txt")
    latex : boolean argument to output in LaTeX (default is False)
    WD : path to directory that contains input files and takes output (default is current directory, '.')
    """
    # format outfiles
    if latex:
        latex = 1
        file_type = '.tex'
    else:
        latex = 0
        file_type = '.txt'
    dir_path = os.path.realpath(WD)
    outfile = os.path.join(dir_path, 'Directions' + file_type)
    Ioutfile = os.path.join(dir_path, 'Intensities' + file_type)
    Soutfile = os.path.join(dir_path, 'SiteNfo' + file_type)
    Specout = os.path.join(dir_path, 'Specimens' + file_type)
    Critout = os.path.join(dir_path, 'Criteria' + file_type)
    # format infiles
    res_file = os.path.join(dir_path, res_file)
    if crit_file:
        crit_file = os.path.join(dir_path, crit_file)
    if spec_file:
        spec_file = os.path.join(dir_path, spec_file)
    else:
        grade = False
    # open output files
    f = open(outfile, 'w')
    sf = open(Soutfile, 'w')
    fI = open(Ioutfile, 'w')
    if crit_file:
        cr = open(Critout, 'w')
    # set up column headers
    Sites, file_type = pmag.magic_read(res_file)
    if crit_file:
        Crits, file_type = pmag.magic_read(crit_file)
    else:
        Crits = []
    SiteCols = ["Site", "Location", "Lat. (N)", "Long. (E)", "Age ", "Age sigma", "Units"]
    SiteKeys = ["er_site_names", "average_lat", "average_lon", "average_age",
                "average_age_sigma", "average_age_unit"]
    DirCols = ["Site", 'Comp.', "perc TC", "Dec.", "Inc.", "Nl", "Np", "k    ", "R", "a95",
             "PLat", "PLong"]
    DirKeys = ["er_site_names", "pole_comp_name", "tilt_correction", "average_dec", "average_inc",
               "average_n_lines", "average_n_planes", "average_k", "average_r", "average_alpha95",
               "vgp_lat", "vgp_lon"]
    IntCols = ["Site", "N", "B (uT)", "sigma", "sigma perc", "VADM", "VADM sigma"]
    IntKeys = ["er_site_names", "average_int_n", "average_int", "average_int_sigma",
               'average_int_sigma_perc', "vadm", "vadm_sigma"]
    AllowedKeys = ['specimen_frac','specimen_scat','specimen_gap_max','measurement_step_min',
                   'measurement_step_max', 'measurement_step_unit', 'specimen_polarity',
                   'specimen_nrm', 'specimen_direction_type', 'specimen_comp_nmb', 'specimen_mad',
                   'specimen_alpha95', 'specimen_n', 'specimen_int_sigma',
                   'specimen_int_sigma_perc', 'specimen_int_rel_sigma',
                   'specimen_int_rel_sigma_perc', 'specimen_int_mad', 'specimen_int_n',
                   'specimen_w', 'specimen_q', 'specimen_f', 'specimen_fvds', 'specimen_b_sigma',
                   'specimen_b_beta', 'specimen_g', 'specimen_dang', 'specimen_md',
                   'specimen_ptrm', 'specimen_drat', 'specimen_drats', 'specimen_rsc',
                   'specimen_viscosity_index', 'specimen_magn_moment', 'specimen_magn_volume',
                   'specimen_magn_mass', 'specimen_int_ptrm_n', 'specimen_delta', 'specimen_theta',
                   'specimen_gamma', 'sample_polarity', 'sample_nrm', 'sample_direction_type',
                   'sample_comp_nmb', 'sample_sigma', 'sample_alpha95', 'sample_n',
                   'sample_n_lines', 'sample_n_planes', 'sample_k', 'sample_r',
                   'sample_tilt_correction', 'sample_int_sigma', 'sample_int_sigma_perc',
                   'sample_int_rel_sigma', 'sample_int_rel_sigma_perc', 'sample_int_n',
                   'sample_magn_moment', 'sample_magn_volume', 'sample_magn_mass', 'site_polarity',
                   'site_nrm', 'site_direction_type', 'site_comp_nmb', 'site_sigma',
                   'site_alpha95', 'site_n', 'site_n_lines', 'site_n_planes', 'site_k', 'site_r',
                   'site_tilt_correction', 'site_int_sigma', 'site_int_sigma_perc',
                   'site_int_rel_sigma', 'site_int_rel_sigma_perc', 'site_int_n',
                   'site_magn_moment', 'site_magn_volume', 'site_magn_mass', 'average_age_min',
                   'average_age_max', 'average_age_sigma', 'average_age_unit', 'average_sigma',
                   'average_alpha95', 'average_n', 'average_nn', 'average_k', 'average_r',
                   'average_int_sigma', 'average_int_rel_sigma', 'average_int_rel_sigma_perc',
                   'average_int_n', 'average_int_nn', 'vgp_dp', 'vgp_dm', 'vgp_sigma',
                   'vgp_alpha95', 'vgp_n', 'vdm_sigma', 'vdm_n', 'vadm_sigma', 'vadm_n']
    if crit_file:
        crit = Crits[0] # get a list of useful keys
        for key in crit.keys():
            if key not in AllowedKeys:
                del(crit[key])
        for key in crit.keys():
            if (not crit[key]) or (eval(crit[key]) > 1000) or (eval(crit[key])==0):
                del(crit[key]) # get rid of all blank or too big ones or too little ones
        CritKeys = crit.keys()
    if spec_file:
        Specs, file_type =pmag.magic_read(spec_file)
        fsp = open(Specout,'w') # including specimen intensities if desired
        SpecCols = ["Site", "Specimen", "B (uT)", "MAD", "Beta", "N", "Q", "DANG", "f-vds",
                    "DRATS", "T (C)"]
        SpecKeys = ['er_site_name', 'er_specimen_name', 'specimen_int', 'specimen_int_mad',
                    'specimen_b_beta', 'specimen_int_n', 'specimen_q', 'specimen_dang',
                    'specimen_fvds', 'specimen_drats', 'trange']
        Xtra = ['specimen_frac', 'specimen_scat', 'specimen_gmax']
        if grade:
            SpecCols.append('Grade')
            SpecKeys.append('specimen_grade')
        for x in Xtra:  # put in the new intensity keys if present
            if x in Specs[0].keys():
                SpecKeys.append(x)
                newkey = ""
                for k in x.split('_')[1:]:
                    newkey = newkey + k + '_'
                SpecCols.append(newkey.strip('_'))
        SpecCols.append('Corrections')
        SpecKeys.append('corrections')
    Micro = ['specimen_int', 'average_int', 'average_int_sigma'] # these should be multiplied by 1e6
    Zeta = ['vadm', 'vadm_sigma'] # these should be multiplied by 1e21
    # write out the header information for each output file
    if latex: #write out the latex header stuff
        sep=' & '
        end='\\\\'
        f.write('\\documentclass{article}\n')
        f.write('\\usepackage[margin=1in]{geometry}\n')
        f.write('\\usepackage{longtable}\n')
        f.write('\\begin{document}\n')
        sf.write('\\documentclass{article}\n')
        sf.write('\\usepackage[margin=1in]{geometry}\n')
        sf.write('\\usepackage{longtable}\n')
        sf.write('\\begin{document}\n')
        fI.write('\\documentclass{article}\n')
        fI.write('\\usepackage[margin=1in]{geometry}\n')
        fI.write('\\usepackage{longtable}\n')
        fI.write('\\begin{document}\n')
        if crit_file:
            cr.write('\\documentclass{article}\n')
            cr.write('\\usepackage[margin=1in]{geometry}\n')
            cr.write('\\usepackage{longtable}\n')
            cr.write('\\begin{document}\n')
        if spec_file:
            fsp.write('\\documentclass{article}\n')
            fsp.write('\\usepackage[margin=1in]{geometry}\n')
            fsp.write('\\usepackage{longtable}\n')
            fsp.write('\\begin{document}\n')
        tabstring = '\\begin{longtable}{'
        fstring = tabstring
        for k in range(len(SiteCols)):
            fstring = fstring + 'r'
        sf.write(fstring+'}\n')
        sf.write('\hline\n')
        fstring = tabstring
        for k in range(len(DirCols)):
            fstring = fstring + 'r'
        f.write(fstring+'}\n')
        f.write('\hline\n')
        fstring = tabstring
        for k in range(len(IntCols)):
            fstring = fstring + 'r'
        fI.write(fstring+'}\n')
        fI.write('\hline\n')
        fstring = tabstring
        if crit_file:
            for k in range(len(CritKeys)):
                fstring = fstring + 'r'
            cr.write(fstring+'}\n')
            cr.write('\hline\n')
        if spec_file:
            fstring = tabstring
            for k in range(len(SpecCols)):
                fstring = fstring + 'r'
            fsp.write(fstring+'}\n')
            fsp.write('\hline\n')
    else:   # just set the tab and line endings for tab delimited
        sep=' \t '
        end=''
# now write out the actual column headers
    Soutstring, Doutstring, Ioutstring, Spoutstring, Croutstring = "", "", "", "", ""
    for k in range(len(SiteCols)):
        Soutstring = Soutstring + SiteCols[k] + sep
    Soutstring = Soutstring.strip(sep)
    Soutstring =Soutstring + end + '\n'
    sf.write(Soutstring)
    for k in range(len(DirCols)):
        Doutstring = Doutstring + DirCols[k] + sep
    Doutstring = Doutstring.strip(sep)
    Doutstring = Doutstring + end + '\n'
    f.write(Doutstring)
    for k in range(len(IntCols)):
        Ioutstring=Ioutstring+IntCols[k]+sep
    Ioutstring = Ioutstring.strip(sep)
    Ioutstring = Ioutstring + end + '\n'
    fI.write(Ioutstring)
    if crit_file:
        for k in range(len(CritKeys)):
            Croutstring = Croutstring + CritKeys[k] + sep
        Croutstring = Croutstring.strip(sep)
        Croutstring = Croutstring + end + '\n'
        cr.write(Croutstring)
    if spec_file:
        for k in range(len(SpecCols)):
            Spoutstring = Spoutstring + SpecCols[k] + sep
        Spoutstring = Spoutstring.strip(sep)
        Spoutstring = Spoutstring + end + "\n"
        fsp.write(Spoutstring)
    if latex: # put in a horizontal line in latex file
        f.write('\hline\n')
        sf.write('\hline\n')
        fI.write('\hline\n')
        if crit_file:
            cr.write('\hline\n')
        if spec_file:
            fsp.write('\hline\n')
 # do criteria
    if crit_file:
        for crit in Crits: #
            Croutstring=""
            for key in CritKeys:
                Croutstring = Croutstring + crit[key] + sep
            Croutstring = Croutstring.strip(sep) + end
            cr.write(Croutstring + '\n')
 # do directions
    VGPs = pmag.get_dictitem(Sites, 'vgp_lat', '', 'F') # get all results with VGPs
    VGPs = pmag.get_dictitem(VGPs, 'data_type', 'i', 'T') # get site level stuff
    for site in VGPs:
        if len(site['er_site_names'].split(":"))==1:
            if 'er_sample_names' not in site.keys():
                site['er_sample_names']=''
            if 'pole_comp_name' not in site.keys():
                site['pole_comp_name']="A"
            if 'average_nn' not in site.keys() and 'average_n' in site.keys():
                site['average_nn']=site['average_n']
            if 'average_n_lines' not in site.keys():
                site['average_n_lines']=site['average_nn']
            if 'average_n_planes' not in site.keys():
                site['average_n_planes']=""
            Soutstring, Doutstring = "", ""
            for key in SiteKeys:
                if key in site.keys():
                    Soutstring = Soutstring + site[key] + sep
            Soutstring = Soutstring.strip(sep) + end
            sf.write(Soutstring + '\n')
            for key in DirKeys:
                if key in site.keys():
                    Doutstring = Doutstring + site[key] + sep
            Doutstring = Doutstring.strip(sep) + end
            f.write(Doutstring + '\n')
# now do intensities
    VADMs = pmag.get_dictitem(Sites, 'vadm', '', 'F')
    VADMs=pmag.get_dictitem(VADMs, 'data_type', 'i', 'T')
    for site in VADMs: # do results level stuff
        if site not in VGPs:
            Soutstring = ""
            for key in SiteKeys:
                if key in site.keys():
                    Soutstring = Soutstring + site[key] + sep
                else:
                    Soutstring = Soutstring + " " + sep
            Soutstring = Soutstring.strip(sep) + end
            sf.write(Soutstring+'\n')
        if len(site['er_site_names'].split(":"))==1 and site['data_type']=='i':
            if 'average_int_sigma_perc' not in site.keys():
                site['average_int_sigma_perc'] = "0"
            if site["average_int_sigma"] == "":
                site["average_int_sigma"] = "0"
            if site["average_int_sigma_perc"] == "":
                site["average_int_sigma_perc"] = "0"
            if site["vadm"] == "":
                site["vadm"] = "0"
            if site["vadm_sigma"]=="":
                site["vadm_sigma"]="0"
        for key in site.keys(): # reformat vadms, intensities
            if key in Micro:
                site[key]='%7.1f'%(float(site[key])*1e6)
            if key in Zeta:
                site[key]='%7.1f'%(float(site[key])*1e-21)
        outstring=""
        for key in IntKeys:
          if key not in site.keys():
              site[key]=""
          outstring = outstring + site[key] + sep
        outstring = outstring.strip(sep) + end + '\n'
        fI.write(outstring)
#    VDMs=pmag.get_dictitem(Sites,'vdm','','F') # get non-blank VDMs
#    for site in VDMs: # do results level stuff
#      if len(site['er_site_names'].split(":"))==1:
#            if 'average_int_sigma_perc' not in site.keys():site['average_int_sigma_perc']="0"
#            if site["average_int_sigma"]=="":site["average_int_sigma"]="0"
#            if site["average_int_sigma_perc"]=="":site["average_int_sigma_perc"]="0"
#            if site["vadm"]=="":site["vadm"]="0"
#            if site["vadm_sigma"]=="":site["vadm_sigma"]="0"
#      for key in site.keys(): # reformat vadms, intensities
#            if key in Micro: site[key]='%7.1f'%(float(site[key])*1e6)
#            if key in Zeta: site[key]='%7.1f'%(float(site[key])*1e-21)
#      outstring=""
#      for key in IntKeys:
#          outstring=outstring+site[key]+sep
#      fI.write(outstring.strip(sep)+'\n')
    if spec_file:
        SpecsInts = pmag.get_dictitem(Specs, 'specimen_int', '', 'F')
        for spec in SpecsInts:
            spec['trange'] = '%i'%(int(float(spec['measurement_step_min'])-273))+'-'+'%i'%(int(float(spec['measurement_step_max'])-273))
            meths = spec['magic_method_codes'].split(':')
            corrections = ''
            for meth in meths:
                if 'DA' in meth:
                    corrections = corrections + meth[3:] + ':'
            corrections = corrections.strip(':')
            if corrections.strip() == "":
                corrections = "None"
            spec['corrections'] = corrections
            outstring = ""
            for key in SpecKeys:
                if key in Micro:
                    spec[key] = '%7.1f'%(float(spec[key]) * 1e6)
                if key in Zeta:
                    spec[key] = '%7.1f'%(float(spec[key]) * 1e-21)
                outstring = outstring + spec[key] + sep
            fsp.write(outstring.strip(sep) + end + '\n')
    #
    if latex: # write out the tail stuff
        f.write('\hline\n')
        sf.write('\hline\n')
        fI.write('\hline\n')
        f.write('\end{longtable}\n')
        sf.write('\end{longtable}\n')
        fI.write('\end{longtable}\n')
        f.write('\end{document}\n')
        sf.write('\end{document}\n')
        fI.write('\end{document}\n')
        if spec_file:
            fsp.write('\hline\n')
            fsp.write('\end{longtable}\n')
            fsp.write('\end{document}\n')
        if crit_file:
            cr.write('\hline\n')
            cr.write('\end{longtable}\n')
            cr.write('\end{document}\n')
    f.close()
    sf.close()
    fI.close()
    print 'data saved in: ', outfile, Ioutfile, Soutfile
    outfiles = [outfile, Ioutfile, Soutfile]
    if spec_file:
        fsp.close()
        print 'specimen data saved in: ', Specout
        outfiles.append(Specout)
    if crit_file:
        cr.close()
        print 'Selection criteria saved in: ', Critout
        outfiles.append(Critout)
    return True, outfiles


def demag_magic(path_to_file = '.', file_name = 'magic_measurements.txt',
               save = False, save_folder = '.', fmt='svg', plot_by='loc',
               treat=None, XLP = "", individual = None, average_measurements = False,
               single_plot = False):
    '''
    Takes demagnetization data (from magic_measurements file) and outputs
    intensity plots (with optional save).

    Parameters
    -----------
    path_to_file : path to directory that contains files (default is current directory, '.')
    file_name : name of measurements file (default is 'magic_measurements.txt')
    save : boolean argument to save plots (default is False)
    save_folder : relative directory where plots will be saved (default is current directory, '.')
    fmt : format of saved figures (default is 'svg')
    plot_by : specifies what sampling level you wish to plot the data at
        ('loc' -- plots all samples of the same location on the same plot
        'exp' -- plots all samples of the same expedition on the same plot
        'site' -- plots all samples of the same site on the same plot
        'sample' -- plots all measurements of the same sample on the same plot
        'spc' -- plots each specimen individually)
    treat : treatment step
        'T' = thermal demagnetization
        'AF' = alternating field demagnetization
        'M' = microwave radiation demagnetization
        (default is 'AF')
    XLP : filter data by a particular method
    individual : This function outputs all plots by default. If plotting by sample
        or specimen, you may not wish to see (or wait for) every single plot. You can
        therefore specify a particular plot by setting this keyword argument to
        a string of the site/sample/specimen name.
    average_measurements : Option to average demagnetization measurements by
        the grouping specified with the 'plot_by' keyword argument (default is False)
    single_plot : Option to output a single plot with all measurements (default is False)
    '''

    FIG={} # plot dictionary
    FIG['demag']=1 # demag is figure 1
    in_file,plot_key,LT=os.path.join(path_to_file, file_name),'er_location_name',"LT-AF-Z"
    XLP=""
    norm=1
    units,dmag_key='T','treatment_ac_field'
    plot_num=0

    if plot_by=='loc':
        plot_key='er_location_name'
    elif plot_by=='exp':
        plot_key='er_expedition_name'
    elif plot_by=='site':
        plot_key='er_site_name'
    elif plot_by=='sam':
        plot_key='er_sample_name'
    elif plot_by=='spc':
        plot_key='er_specimen_name'

    if treat != None:
        LT='LT-'+treat+'-Z' # get lab treatment for plotting
        if  LT=='LT-T-Z':
            units,dmag_key='K','treatment_temp'
        elif  LT=='LT-AF-Z':
            units,dmag_key='T','treatment_ac_field'
        elif  LT=='LT-M-Z':
            units,dmag_key='J','treatment_mw_energy'
        else:
            units='U'
    else:
        LT='LT-AF-Z'

    plot_dict = {}
    data,file_type=pmag.magic_read(in_file)
    sids=pmag.get_specs(data)
    plt.figure(num=FIG['demag'],figsize=(5,5))
    print len(data),' records read from ',in_file
    #
    #
    # find desired intensity data
    #
    # get plotlist
    #
    plotlist,intlist=[],['measurement_magnitude','measurement_magn_moment',
                         'measurement_magn_volume','measurement_magn_mass']
    IntMeths=[]
    FixData=[]
    for rec in data:
        meths=[]
        methcodes=rec['magic_method_codes'].split(':')
        for meth in methcodes:
            meths.append(meth.strip())
        for key in rec.keys():
            if key in intlist and rec[key]!="":
                if key not in IntMeths:
                    IntMeths.append(key)
                if rec[plot_key] not in plotlist and LT in meths:
                    plotlist.append(rec[plot_key])
                if 'measurement_flag' not in rec.keys():
                    rec['measurement_flag']='g'
                FixData.append(rec)
        plotlist.sort()
    if len(IntMeths)==0:
        print 'No intensity information found'
    data=FixData
    int_key=IntMeths[0] # plot first intensity method found - normalized to initial value anyway - doesn't matter which used
    # print plotlist
    if individual is not None:
        if type(individual) == list or type(individual)==tuple:
            plotlist = list(individual)
        else:
            plotlist = []
            plotlist.append(individual)
    for plot in plotlist:
        print plot,'plotting by: ',plot_key
        PLTblock=pmag.get_dictitem(data,plot_key,plot,'T') # fish out all the data for this type of plot
        PLTblock=pmag.get_dictitem(PLTblock,'magic_method_codes',LT,'has') # fish out all the dmag for this experiment type
        PLTblock=pmag.get_dictitem(PLTblock,int_key,'','F') # get all with this intensity key non-blank
        if XLP!="":
            # reject data with XLP in method_code
            PLTblock=pmag.get_dictitem(PLTblock,'magic_method_codes',XLP,'not')
    # for plot in plotlist:
        if len(PLTblock)>2:
            title=PLTblock[0][plot_key]
            spcs=[]
            for rec in PLTblock:
                if rec['er_specimen_name'] not in spcs:
                    spcs.append(rec['er_specimen_name'])
            if average_measurements is False:
                for spc in spcs:
                    SPCblock=pmag.get_dictitem(PLTblock,'er_specimen_name',spc,'T') # plot specimen by specimen
                    INTblock=[]
                    for rec in SPCblock:
                        INTblock.append([float(rec[dmag_key]),0,0,float(rec[int_key]),1,rec['measurement_flag']])
                    if len(INTblock)>2:
                        pmagplotlib.plotMT(FIG['demag'],INTblock,title,0,units,norm)
            else:
                AVGblock={}
                for spc in spcs:
                    SPCblock=pmag.get_dictitem(PLTblock,'er_specimen_name',spc,'T') # plot specimen by specimen
                    for rec in SPCblock:
                        if rec['measurement_flag'] == 'g':
                            if float(rec[dmag_key]) not in AVGblock.keys():
                                AVGblock[float(rec[dmag_key])] = [float(rec[int_key])]
                            else:
                                AVGblock[float(rec[dmag_key])].append(float(rec[int_key]))
                INTblock = []
                for step in sorted(AVGblock.keys()):
                    INTblock.append([float(step), 0, 0, float(sum(AVGblock[step]))/float(len(AVGblock[step])), 1, 'g'])
                pmagplotlib.plotMT(FIG['demag'],INTblock,title,0,units,norm)
        if save==True:
            plt.savefig(os.path.join(save_folder, title)+ '.' + fmt)
        if single_plot is False:
            plt.show()
    if single_plot is True:
        plt.show()


def iplotHYS(fignum,B,M,s):
    """
    function to plot hysteresis data

    This function has been adapted from pmagplotlib.iplotHYS for specific use
    within a Jupyter notebook.

    Parameters
    -----------
    fignum : reference number for matplotlib figure being created
    B : list of B (flux density) values of hysteresis experiment
    M : list of M (magnetization) values of hysteresis experiment
    s : sample name
    """
    import pmagpy.spline as spline
    from matplotlib.pylab import polyfit
    if fignum!=0:
        plt.figure(num=fignum)
        plt.clf()
    hpars={}
# close up loop
    Npts=len(M)
    B70=0.7*B[0] # 70 percent of maximum field
    for b in B:
        if b<B70:
            break
    Nint=B.index(b)-1
    if Nint>30:Nint=30
    if Nint<10:Nint=10
    Bzero,Mzero,Mfix,Mnorm,Madj,MadjN="","",[],[],[],[]
    Mazero=""
    m_init=0.5*(M[0]+M[1])
    m_fin=0.5*(M[-1]+M[-2])
    diff=m_fin-m_init
    Bmin=0.
    for k in range(Npts):
        frac=float(k)/float(Npts-1)
        Mfix.append((M[k]-diff*frac))
        if Bzero=="" and B[k]<0: Bzero=k
        if B[k]<Bmin:
            Bmin=B[k]
            kmin=k
    Bslop=B[2:Nint+2] # adjust slope with first 30 data points (throwing out first 3)
    Mslop=Mfix[2:Nint+2]
    polyU=polyfit(Bslop,Mslop,1) # best fit line to high field points
    Bslop=B[kmin:kmin+(Nint+1)] # adjust slope with first 30 points of ascending branch
    Mslop=Mfix[kmin:kmin+(Nint+1)]
    polyL=polyfit(Bslop,Mslop,1) # best fit line to high field points
    xhf=0.5*(polyU[0]+polyL[0]) # mean of two slopes
    hpars['hysteresis_xhf']='%8.2e'%(xhf*4*np.pi*1e-7) # convert B to A/m, high field slope in m^3
    meanint=0.5*(polyU[1]+polyL[1]) # mean of two intercepts
    Msat=0.5*(polyU[1]-polyL[1]) # mean of saturation remanence
    Moff=[]
    for k in range(Npts):
        Moff.append((Mfix[k]-xhf*B[k]-meanint))  # take out linear slope and offset (makes symmetric about origin)
        if Mzero=="" and Moff[k]<0:
            Mzero=k
        if Mzero!="" and Mazero=="" and Moff[k]>0:
            Mazero=k
    hpars['hysteresis_ms_moment']='%8.3e'%(Msat) # Ms in Am^2
#
# split into upper and lower loops for splining
    Mupper,Bupper,Mlower,Blower=[],[],[],[]
    deltaM,Bdm=[],[] # diff between upper and lower curves at Bdm
    for k in range(kmin-2,0,-1):
        Mupper.append(Moff[k]/Msat)
        Bupper.append(B[k])
    for k in range(kmin+2,len(B)):
        Mlower.append(Moff[k]/Msat)
        Blower.append(B[k])
    Iupper=spline.Spline(Bupper,Mupper) # get splines for upper up and down
    Ilower=spline.Spline(Blower,Mlower) # get splines for lower
    for b in np.arange(B[0],step=.01):  # get range of field values
        Mpos=((Iupper(b)-Ilower(b))) # evaluate on both sides of B
        Mneg=((Iupper(-b)-Ilower(-b)))
        Bdm.append(b)
        deltaM.append(0.5*(Mpos+Mneg))# take average delta M
    for k in range(Npts):
        MadjN.append(Moff[k]/Msat)
        Mnorm.append(M[k]/Msat)
# find Mr : average of two spline fits evaluted at B=0 (times Msat)
    Mr=Msat*0.5*(Iupper(0.)-Ilower(0.))
    hpars['hysteresis_mr_moment']='%8.3e'%(Mr)
# find Bc (x intercept), interpolate between two bounding points
    Bz=B[Mzero-1:Mzero+1]
    Mz=Moff[Mzero-1:Mzero+1]
    Baz=B[Mazero-1:Mazero+1]
    Maz=Moff[Mazero-1:Mazero+1]
    try:
        poly=polyfit(Bz,Mz,1) # best fit line through two bounding points
        Bc=-poly[1]/poly[0] # x intercept
        poly=polyfit(Baz,Maz,1) # best fit line through two bounding points
        Bac=-poly[1]/poly[0] # x intercept
        hpars['hysteresis_bc']='%8.3e'%(0.5*(abs(Bc)+abs(Bac)))
    except:
        hpars['hysteresis_bc']='0'
    return hpars,deltaM,Bdm, B, Mnorm, MadjN


def hysteresis_magic(path_to_file = '.',hyst_file="rmag_hysteresis.txt",
                     save = False, save_folder = '.',
                     fmt = "svg", plots = True):
    """
    Calculates hysteresis parameters, saves them in rmag_hysteresis format file.
    If selected, this function also plots hysteresis loops, delta M curves,
    d (Delta M)/dB curves, and IRM backfield curves.

    Parameters (defaults are used if not specified)
    ----------
    path_to_file : path to directory that contains files (default is current directory, '.')
    hyst_file : hysteresis file (default is 'rmag_hysteresis.txt')
    save : boolean argument to save plots (default is False)
    save_folder : relative directory where plots will be saved (default is current directory, '.')
    fmt : format of saved figures (default is 'pdf')
    plots: whether or not to display the plots (default is true)
    """
    from matplotlib.pylab import polyfit
    import matplotlib.ticker as mtick
    user,meas_file,rmag_out,rmag_file="","agm_measurements.txt","rmag_hysteresis.txt",""
    pltspec=""
    dir_path=save_folder
    verbose=pmagplotlib.verbose
    version_num=pmag.get_version()
    rmag_out=save_folder+'/'+rmag_out
    meas_file=path_to_file+'/'+hyst_file
    rmag_rem=save_folder+"/rmag_remanence.txt"
    #
    #
    meas_data,file_type=pmag.magic_read(meas_file)
    if file_type!='magic_measurements':
        print hysteresis_magic.__doc__
        print 'bad file'
        return

    # initialize some variables
    # define figure numbers for hyst,deltaM,DdeltaM curves
    HystRecs,RemRecs=[],[]
    HDD = {}
    HDD['hyst'],HDD['deltaM'],HDD['DdeltaM']=1,2,3
    experiment_names,sids=[],[]
    for rec in meas_data:
        meths=rec['magic_method_codes'].split(':')
        methods=[]
        for meth in meths:
            methods.append(meth.strip())
        if 'LP-HYS' in methods:
            if 'er_synthetic_name' in rec.keys() and rec['er_synthetic_name']!="":
                rec['er_specimen_name']=rec['er_synthetic_name']
            if rec['magic_experiment_name'] not in experiment_names:experiment_names.append(rec['magic_experiment_name'])
            if rec['er_specimen_name'] not in sids:sids.append(rec['er_specimen_name'])
    #
    fignum = 1
    sample_num = 0
    # initialize variables to record some bulk info in first loop
    first_dcd_rec,first_rec,first_imag_rec=1,1,1
    while sample_num < len(sids):
        sample = sids[sample_num]
        print sample, sample_num+1 , 'out of ',len(sids)
        B,M,Bdcd,Mdcd=[],[],[],[] #B,M for hysteresis, Bdcd,Mdcd for irm-dcd data
        Bimag,Mimag=[],[] #Bimag,Mimag for initial magnetization curves
        for rec in meas_data:
            methcodes=rec['magic_method_codes'].split(':')
            meths=[]
            for meth in methcodes:
                meths.append(meth.strip())
            if rec['er_specimen_name']==sample and "LP-HYS" in meths:
                B.append(float(rec['measurement_lab_field_dc']))
                M.append(float(rec['measurement_magn_moment']))
                if first_rec==1:
                    e=rec['magic_experiment_name']
                    HystRec={}
                    first_rec=0
                    if "er_location_name" in rec.keys():
                        HystRec["er_location_name"]=rec["er_location_name"]
                        locname=rec['er_location_name'].replace('/','-')
                    if "er_sample_name" in rec.keys():HystRec["er_sample_name"]=rec["er_sample_name"]
                    if "er_site_name" in rec.keys():HystRec["er_site_name"]=rec["er_site_name"]
                    if "er_synthetic_name" in rec.keys() and rec['er_synthetic_name']!="":
                        HystRec["er_synthetic_name"]=rec["er_synthetic_name"]
                    else:
                        HystRec["er_specimen_name"]=rec["er_specimen_name"]
            if rec['er_specimen_name']==sample and "LP-IRM-DCD" in meths:
                Bdcd.append(float(rec['treatment_dc_field']))
                Mdcd.append(float(rec['measurement_magn_moment']))
                if first_dcd_rec==1:
                    RemRec={}
                    irm_exp=rec['magic_experiment_name']
                    first_dcd_rec=0
                    if "er_location_name" in rec.keys():RemRec["er_location_name"]=rec["er_location_name"]
                    if "er_sample_name" in rec.keys():RemRec["er_sample_name"]=rec["er_sample_name"]
                    if "er_site_name" in rec.keys():RemRec["er_site_name"]=rec["er_site_name"]
                    if "er_synthetic_name" in rec.keys() and rec['er_synthetic_name']!="":
                        RemRec["er_synthetic_name"]=rec["er_synthetic_name"]
                    else:
                        RemRec["er_specimen_name"]=rec["er_specimen_name"]
            if rec['er_specimen_name']==sample and "LP-IMAG" in meths:
                if first_imag_rec==1:
                    imag_exp=rec['magic_experiment_name']
                    first_imag_rec=0
                Bimag.append(float(rec['measurement_lab_field_dc']))
                Mimag.append(float(rec['measurement_magn_moment']))
        if len(B)>0:
            hmeths=[]
            for meth in meths:
                hmeths.append(meth)
    #         fignum = 1
            fig = plt.figure(figsize=(8,8))
            hpars,deltaM,Bdm, B, Mnorm, MadjN = iplotHYS(1,B,M,sample)
            ax1 = fig.add_subplot(2,2,1)
            ax1.axhline(0,color='k')
            ax1.axvline(0,color='k')
            ax1.plot(B,Mnorm,'r')
            ax1.plot(B,MadjN,'b')
            ax1.set_xlabel('B (T)')
            ax1.set_ylabel("M/Msat")
    #         ax1.set_title(sample)
            ax1.set_xlim(-1,1)
            ax1.set_ylim(-1,1)
            bounds=ax1.axis()
            n4='Ms: '+'%8.2e'%(float(hpars['hysteresis_ms_moment']))+' Am^2'
            ax1.text(bounds[1]-.9*bounds[1],-.9,n4, fontsize=9)
            n1='Mr: '+'%8.2e'%(float(hpars['hysteresis_mr_moment']))+' Am^2'
            ax1.text(bounds[1]-.9*bounds[1],-.7,n1, fontsize=9)
            n2='Bc: '+'%8.2e'%(float(hpars['hysteresis_bc']))+' T'
            ax1.text(bounds[1]-.9*bounds[1],-.5,n2, fontsize=9)
            if 'hysteresis_xhf' in hpars.keys():
                n3=r'Xhf: '+'%8.2e'%(float(hpars['hysteresis_xhf']))+' m^3'
                ax1.text(bounds[1]-.9*bounds[1],-.3,n3, fontsize=9)
    #         plt.subplot(1,2,2)
    #         plt.subplot(1,3,3)
        DdeltaM=[]
        Mhalf=""
        for k in range(2,len(Bdm)):
            DdeltaM.append(abs(deltaM[k]-deltaM[k-2])/(Bdm[k]-Bdm[k-2])) # differnential
        for k in range(len(deltaM)):
            if deltaM[k]/deltaM[0] < 0.5:
                Mhalf=k
                break
        try:
            Bhf=Bdm[Mhalf-1:Mhalf+1]
            Mhf=deltaM[Mhalf-1:Mhalf+1]
            poly=polyfit(Bhf,Mhf,1) # best fit line through two bounding points
            Bcr=(.5*deltaM[0] - poly[1])/poly[0]
            hpars['hysteresis_bcr']='%8.3e'%(Bcr)
            hpars['magic_method_codes']="LP-BCR-HDM"
            if HDD['deltaM']!=0:
                ax2 = fig.add_subplot(2,2,2)
                ax2.plot(Bdm,deltaM,'b')
                ax2.set_xlabel('B (T)')
                ax2.set_ylabel('Delta M')
                linex=[0,Bcr,Bcr]
                liney=[deltaM[0]/2.,deltaM[0]/2.,0]
                ax2.plot(linex,liney,'r')
    #             ax2.set_title(sample)
                ax3 = fig.add_subplot(2,2,3)
                ax3.plot(Bdm[(len(Bdm)-len(DdeltaM)):],DdeltaM,'b')
                ax3.set_xlabel('B (T)')
                ax3.set_ylabel('d (Delta M)/dB')
    #             ax3.set_title(sample)

                ax4 = fig.add_subplot(2,2,4)
                ax4.plot(Bdcd,Mdcd)
                ax4.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.2e'))
                ax4.axhline(0,color='k')
                ax4.axvline(0,color='k')
                ax4.set_xlabel('B (T)')
                ax4.set_ylabel('M/Mr')
        except:
            print "not doing it"
            hpars['hysteresis_bcr']='0'
            hpars['magic_method_codes']=""
        plt.gcf()
        plt.gca()
        plt.tight_layout()
        if save:
            plt.savefig(save_folder + '/' + sample + '_hysteresis.' + fmt)
        plt.show()
        sample_num += 1


def find_ei(data, nb=1000, save = False, save_folder = '.', fmt='svg',
            site_correction = False, return_new_dirs = False):
    """
    Applies series of assumed flattening factor and "unsquishes" inclinations assuming tangent function.
    Finds flattening factor that gives elongation/inclination pair consistent with TK03;
    or, if correcting by site instead of for study-level secular variation,
    finds flattening factor that minimizes elongation and most resembles a
    Fisherian distribution.
    Finds bootstrap confidence bounds

    Required Parameter
    -----------
    data: a nested list of dec/inc pairs

    Optional Parameters (defaults are used unless specified)
    -----------
    nb: number of bootstrapped pseudo-samples (default is 1000)
    save: Boolean argument to save plots (default is False)
    save_folder: path to folder in which plots should be saved (default is current directory)
    fmt: specify format of saved plots (default is 'svg')
    site_correction: Boolean argument to specify whether to "unsquish" data to
        1) the elongation/inclination pair consistent with TK03 secular variation model
        (site_correction = False)
        or
        2) a Fisherian distribution (site_correction = True). Default is FALSE.
        Note that many directions (~ 100) are needed for this correction to be reliable.
    return_new_dirs: optional return of newly "unflattened" directions (default is False)

    Output
    -----------
    four plots:   1) equal area plot of original directions
                  2) Elongation/inclination pairs as a function of f,  data plus 25 bootstrap samples
                  3) Cumulative distribution of bootstrapped optimal inclinations plus uncertainties.
                     Estimate from original data set plotted as solid line
                  4) Orientation of principle direction through unflattening

    NOTE: If distribution does not have a solution, plot labeled: Pathological.  Some bootstrap samples may have
       valid solutions and those are plotted in the CDFs and E/I plot.
    """
    print "Bootstrapping.... be patient"
    print ""
    sys.stdout.flush()

    upper,lower=int(round(.975*nb)),int(round(.025*nb))
    E,I=[],[]

    plt.figure(num=1,figsize=(4,4))
    plot_net(1)
    plot_di(di_block=data)

    ppars=pmag.doprinc(data)
    Io=ppars['inc']
    n=ppars["N"]
    Es,Is,Fs,V2s=pmag.find_f(data)
    if site_correction == True:
        Inc,Elong=Is[Es.index(min(Es))],Es[Es.index(min(Es))]
        flat_f = Fs[Es.index(min(Es))]
    else:
        Inc,Elong=Is[-1],Es[-1]
        flat_f = Fs[-1]

    plt.figure(num=2,figsize=(4,4))
    plt.plot(Is,Es,'r')
    plt.xlabel("Inclination")
    plt.ylabel("Elongation")
    plt.text(Inc,Elong,' %3.1f'%(flat_f))
    plt.text(Is[0]-2,Es[0],' %s'%('f=1'))

    b=0

    while b < nb:
        bdata = pmag.pseudo(data)
        Esb,Isb,Fsb,V2sb = pmag.find_f(bdata)
        if b<25:
            plt.plot(Isb,Esb,'y')
        if Esb[-1] != 0:
            ppars=pmag.doprinc(bdata)
            if site_correction == True:
                I.append(abs(Isb[Esb.index(min(Esb))]))
                E.append(Esb[Esb.index(min(Esb))])
            else:
                I.append(abs(Isb[-1]))
                E.append(Esb[-1])
            b += 1

    I.sort()
    E.sort()
    Eexp=[]
    for i in I:
        Eexp.append(pmag.EI(i))
    plt.plot(I,Eexp,'g-')
    if Inc==0:
        title= 'Pathological Distribution: '+'[%7.1f, %7.1f]' %(I[lower],I[upper])
    else:
        title= '%7.1f [%7.1f, %7.1f]' %(Inc, I[lower],I[upper])

    cdf_fig_num = 3
    plt.figure(num=cdf_fig_num,figsize=(4,4))
    pmagplotlib.plotCDF(cdf_fig_num,I,'Inclinations','r',title)
    pmagplotlib.plotVs(cdf_fig_num,[I[lower],I[upper]],'b','--')
    pmagplotlib.plotVs(cdf_fig_num,[Inc],'g','-')
    pmagplotlib.plotVs(cdf_fig_num,[Io],'k','-')

    # plot corrected directional data

    di_lists = unpack_di_block(data)
    if len(di_lists) == 3:
        decs, incs, intensity = di_lists
    if len(di_lists) == 2:
        decs, incs = di_lists
    if flat_f:
        unsquished_incs = unsquish(incs, flat_f)
        plt.figure(num=4,figsize=(4,4))
        plot_net(4)
        plot_di(decs,unsquished_incs)
    else:
        plt.figure(num=4,figsize=(4,4))
        plot_net(4)
        plot_di(decs,incs)

    if (Inc, Elong, flat_f) == (0, 0, 0):
        print "PATHOLOGICAL DISTRIBUTION"
    print "The original inclination was: " + str(Io)
    print ""
    print "The corrected inclination is: " + str(Inc)
    print "with bootstrapped confidence bounds of: " +  str(I[lower]) + ' to ' + str(I[upper])
    print "and elongation parameter of: " + str(Elong)
    print "The flattening factor is: " + str(flat_f)
    if return_new_dirs is True:
        return make_di_block(decs, unsquished_incs)

def plate_rate_mc(pole1_plon,pole1_plat,pole1_kappa,pole1_N,pole1_age,pole1_age_error,
                  pole2_plon,pole2_plat,pole2_kappa,pole2_N,pole2_age,pole2_age_error,
                  ref_loc_lon,ref_loc_lat,samplesize=10000, plot=True,
                  savefig=True, save_directory='./', figure_name=''):
    """
    Determine the latitudinal motion implied by a pair of poles and utilize
    the Monte Carlo sampling method of Swanson-Hysell (2014) to determine the
    associated uncertainty.

    These values are required for pole1 and pole2:
    ----------------------------
    plon : longitude of pole
    plat : latitude of pole
    kappa : Fisher precision parameter for VPGs in pole
    N : number of VGPs in pole
    age : age assigned to pole in Ma
    age_error : 1 sigma age uncertainty in million years

    Additional required parameters:
    ----------------------------
    ref_loc_lon : longitude of reference location
    ref_loc_lat : latitude of reference location
    samplesize : number of draws from pole and age distributions (default set to 10000)

    Optional parameters for plotting and saving figures (3 are generated):
    ----------------------------
    plot : whether to make figures (default is True)
    savefig : whether to save figures (default is True)
    save_directory = default is local directory
    figure_name = prefix for file names

    Returns
    ----------------------------
    rate, 2.5 percentile rate, 97.5 percentile rate
    """
    from mpl_toolkits.basemap import Basemap
    from scipy import stats

    ref_loc = [ref_loc_lon,ref_loc_lat]
    pole1 = (pole1_plon, pole1_plat)
    pole1_paleolat = 90-pmag.angle(pole1,ref_loc)
    pole2=(pole2_plon, pole2_plat)
    pole2_paleolat = 90-pmag.angle(pole2,ref_loc)
    print "The paleolatitude for ref_loc resulting from pole 1 is:" + str(pole1_paleolat)
    print "The paleolatitude for ref_loc resulting from pole 2 is:" + str(pole2_paleolat)
    rate=((pole1_paleolat-pole2_paleolat)*111*100000)/((pole1_age-pole2_age)*1000000)
    print "The rate of paleolatitudinal change implied by the poles pairs in cm/yr is:" + str(rate)

    pole1_MCages = np.random.normal(pole1_age,pole1_age_error,samplesize)
    pole2_MCages = np.random.normal(pole2_age,pole2_age_error,samplesize)

    plt.hist(pole1_MCages,100,histtype='stepfilled',color='darkred',label='Pole 1 ages')
    plt.hist(pole2_MCages,100,histtype='stepfilled',color='darkblue',label='Pole 2 ages')
    plt.xlabel('Age (Ma)')
    plt.ylabel('n')
    plt.legend(loc=3)
    if savefig == True:
        plot_extension = '_1.svg'
        plt.savefig(save_directory + figure_name + plot_extension)
    plt.show()

    pole1_MCpoles = []
    pole1_MCpole_lat = []
    pole1_MCpole_long = []
    pole1_MCpaleolat = []
    for n in range(samplesize):
        vgp_samples = []
        for vgp in range(pole1_N):
            #pmag.dev returns a direction from a fisher distribution with specified kappa
            direction_atN = pmag.fshdev(pole1_kappa)
            #this direction is centered at latitude of 90 degrees and needs to be rotated
            #to be centered on the mean pole position
            tilt_direction = pole1_plon
            tilt_amount = 90-pole1_plat
            direction = pmag.dotilt(direction_atN[0],direction_atN[1],tilt_direction,tilt_amount)
            vgp_samples.append([direction[0],direction[1],1.])
        mean = pmag.fisher_mean(vgp_samples)
        mean_pole_position = (mean['dec'],mean['inc'])
        pole1_MCpoles.append([mean['dec'],mean['inc'],1.])
        pole1_MCpole_lat.append(mean['inc'])
        pole1_MCpole_long.append(mean['dec'])
        paleolat = 90-pmag.angle(mean_pole_position,ref_loc)
        pole1_MCpaleolat.append(paleolat[0])

    pole2_MCpoles=[]
    pole2_MCpole_lat=[]
    pole2_MCpole_long=[]
    pole2_MCpaleolat=[]
    for n in range(samplesize):
        vgp_samples=[]
        for vgp in range(pole2_N):
            #pmag.dev returns a direction from a fisher distribution with specified kappa
            direction_atN=pmag.fshdev(pole2_kappa)
            #this direction is centered at latitude of 90 degrees and needs to be rotated
            #to be centered on the mean pole position
            tilt_direction=pole2_plon
            tilt_amount=90-pole2_plat
            direction=pmag.dotilt(direction_atN[0],direction_atN[1],tilt_direction,tilt_amount)
            vgp_samples.append([direction[0],direction[1],1.])
        mean=pmag.fisher_mean(vgp_samples)
        mean_pole_position=(mean['dec'],mean['inc'])
        pole2_MCpoles.append([mean['dec'],mean['inc'],1.])
        pole2_MCpole_lat.append(mean['inc'])
        pole2_MCpole_long.append(mean['dec'])
        paleolat=90-pmag.angle(mean_pole_position,ref_loc)
        pole2_MCpaleolat.append(paleolat[0])

    if plot is True:
        plt.figure(figsize=(5, 5))
        m = Basemap(projection='ortho',lat_0=35,lon_0=200,resolution='c',area_thresh=50000)
        m.drawcoastlines(linewidth=0.25)
        m.fillcontinents(color='bisque',lake_color='white',zorder=1)
        m.drawmapboundary(fill_color='white')
        m.drawmeridians(np.arange(0,360,30))
        m.drawparallels(np.arange(-90,90,30))

        plot_vgp(m,pole1_MCpole_long,pole1_MCpole_lat,color='b')
        plot_vgp(m,pole2_MCpole_long,pole2_MCpole_lat,color='g')
        if savefig == True:
            plot_extension = '_2.svg'
            plt.savefig(save_directory + figure_name + plot_extension)
        plt.show()

    #calculating the change in paleolatitude between the Monte Carlo pairs
    pole1_pole2_Delta_degrees=[]
    pole1_pole2_Delta_kilometers=[]
    pole1_pole2_Delta_myr=[]
    pole1_pole2_degrees_per_myr=[]
    pole1_pole2_cm_per_yr=[]

    for n in range(samplesize):
        Delta_degrees=pole1_MCpaleolat[n]-pole2_MCpaleolat[n]
        Delta_Myr=pole1_MCages[n]-pole2_MCages[n]
        pole1_pole2_Delta_degrees.append(Delta_degrees)
        degrees_per_myr=Delta_degrees/Delta_Myr
        cm_per_yr=((Delta_degrees*111)*100000)/(Delta_Myr*1000000)
        pole1_pole2_degrees_per_myr.append(degrees_per_myr)
        pole1_pole2_cm_per_yr.append(cm_per_yr)

    if plot is True:
        plotnumber=100
        plt.figure(num=None, figsize=(10, 4))
        plt.subplot(1, 2, 1)
        for n in range(plotnumber):
            plt.plot([pole1_MCpaleolat[n],pole2_MCpaleolat[n]],
                     [pole1_MCages[n],pole2_MCages[n]],'k-',linewidth=0.1,alpha=0.3)
        plt.scatter(pole1_MCpaleolat[:plotnumber],pole1_MCages[:plotnumber],color='b',s=3)
        plt.scatter(pole1_paleolat,pole1_age,color='lightblue',s=100, edgecolor='w', zorder=10000)
        plt.scatter(pole2_MCpaleolat[:plotnumber],pole2_MCages[:plotnumber],color='g',s=3)
        plt.scatter(pole2_paleolat,pole2_age,color='lightgreen',s=100, edgecolor='w', zorder=10000)
        plt.plot([pole1_paleolat,pole2_paleolat],[pole1_age,pole2_age],'w-',linewidth=2)
        plt.gca().invert_yaxis()
        plt.xlabel('paleolatitude at Duluth, MN (degrees)',size=14)
        plt.ylabel('time (Ma)',size=14)

        plt.subplot(1, 2, 2)
        plt.hist(pole1_pole2_cm_per_yr,bins=600)
        plt.ylabel('n',size=14)
        plt.xlabel('latitudinal drift rate (cm/yr)',size=14)
        #plt.xlim([0,90])
        if savefig == True:
            plot_extension = '_3.svg'
            plt.savefig(save_directory + figure_name + plot_extension)
        plt.show()

    twopointfive_percentile=stats.scoreatpercentile(pole1_pole2_cm_per_yr,2.5)
    fifty_percentile=stats.scoreatpercentile(pole1_pole2_cm_per_yr,50)
    ninetysevenpointfive_percentile=stats.scoreatpercentile(pole1_pole2_cm_per_yr,97.5)
    print "2.5th percentile is: " + str(twopointfive_percentile)
    print "50th percentile is: " + str(fifty_percentile)
    print "97.5th percentile is: " + str(ninetysevenpointfive_percentile)
    return rate[0], twopointfive_percentile, ninetysevenpointfive_percentile
