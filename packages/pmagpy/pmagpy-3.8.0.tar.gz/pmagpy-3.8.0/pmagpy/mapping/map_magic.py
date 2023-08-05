#!/usr/bin/env python

# map_MagIC.py: -*- Python -*-  DESCRIPTIVE TEXT.
#
#  Copyright (c) 2014 Lori Jonestrask
#  Author: Lori Jonestrask (mintblue87@gmail.com) .


def mapping(dictionary, mapping):
    """
    takes in a dictionary and a mapping which contains new key names,
    and returns a new dictionary with the updated key names, i.e.:
    dictionary = {'a': 1, 'b': 2, 'c': 3}
    mapping = {'a': 'aa', 'c': 'cc'}
    mapped_dictionary = mapping(dictionary, mapping)
    mapped_dictionary = {'aa': 1, b, 2, 'cc': 3}
    """
    mapped_dictionary = {}
    for key, value in dictionary.iteritems():
        if key in mapping.keys():
            new_key = mapping[key]
            mapped_dictionary[new_key] = value
        else:
            mapped_dictionary[key] = value # if this line is left in, it gives everything from the original dictionary
    return mapped_dictionary

#mapped_pars = mapping(Pint_pars.pars, a_map)

# mapping between SPD & Magic 2
spd = ['R_corr2', 'PCA_sigma_int_Free', 'PCA_sigma_max_Free', 'n_tail', 'delta_pal', 'DRAT_tail', 'MD_VDS', 'n_add', 'delta_AC', 'y_Arai_mean', 'MAD_Free', 'n_ptrm', 'DRAT', 'IZZI_MD', 'FRAC', 'CDRAT', 'Dec_Free', 'mean_DEV', 'DRATS', 'Z', 'max_DEV', 'fail_arai_beta_box_scatter', 'GAP-MAX', 'pTRM_MAD_Free', 'ptrms_dec_Free', 'MAD_Anc', 'fail_ptrm_beta_box_scatter', 'ptrms_angle_Free', 'scat_bounding_line_low', 'PCA_sigma_min_Free', 'B_anc', 'SCAT', 'R_det2', 'best_fit_vector_Free', 'specimen_b_beta', 'specimen_YT', 'delta_CK', 'lab_dc_field', 'Inc_Free', 'mean_DRAT', 'theta', 'max_ptrm_check', 'tmin', 'x_Arai_mean', 'fail_tail_beta_box_scatter', 'delta_TR', 'alpha', 'specimen_fvds', 'specimen_b_sigma', 'specimen_b', 'specimen_g', 'specimen_f', 'tmax', 'specimen_int_n', 'specimen_q', 'DANG', 'ptrms_inc_Free', 'SSE', 'gamma', 'scat_bounding_line_high', 'specimen_k', 'specimen_int_crm', 'specimen_dt', 'specimen_k_prime', 'specimen_k_prime_SSE']

magic = ['specimen_coeff_det_sq', 'specimen_PCA_sigma_int', 'specimen_PCA_sigma_max', 'specimen_int_ptrm_tail_n', 'specimen_dpal', 'specimen_tail_drat', 'specimen_md', 'specimen_ac_n', 'specimen_dac', 'specimen_cm_y', 'specimen_int_mad', 'specimen_int_ptrm_n', 'specimen_drat', 'specimen_z_md', 'specimen_frac', 'specimen_cdrat', 'specimen_dec', 'specimen_mdev', 'specimen_drats', 'specimen_z', 'specimen_maxdev', 'fail_arai_beta_box_scatter', 'specimen_gmax', 'specimen_ptrms_mad', 'specimen_ptrms_dec', 'specimen_int_mad_anc', 'fail_ptrm_beta_box_scatter', 'specimen_ptrms_angle', 'specimen_scat_bounding_line_low', 'specimen_PCA_sigma_min', 'specimen_int_uT', 'specimen_scat', 'specimen_r_sq', 'specimen_PCA_v1', 'specimen_b_beta', 'specimen_YT', 'specimen_dck', 'lab_dc_field', 'specimen_inc', 'specimen_mdrat', 'specimen_theta', 'specimen_ptrm', 'measurement_step_min', 'specimen_cm_x', 'fail_tail_beta_box_scatter', 'specimen_dtr', 'specimen_int_alpha', 'specimen_fvds', 'specimen_b_sigma', 'specimen_b', 'specimen_g', 'specimen_f', 'measurement_step_max', 'specimen_int_n', 'specimen_q', 'specimen_int_dang', 'specimen_ptrms_inc', 'specimen_k_sse', 'specimen_gamma', 'specimen_scat_bounding_line_high', 'specimen_k', 'specimen_int_crm', 'specimen_dt', 'specimen_k_prime', 'specimen_k_prime_sse']

magic3 = ['specimens.int_r2_det', 'specimens.int_n_ptrm_tail', 'specimens.int_dpal', 'specimens.int_drat_tail', 'specimens.int_md', 'specimens.int_n_ac', 'specimens.int_dac', 'specimens.int_mad', 'specimens.int_n_ptrm', 'specimens.int_drat', 'specimens.int_z_md', 'specimens.int_frac', 'specimens.int_cdrat', 'specimens.dir_dec', 'specimens.int_mdev', 'specimens.int_drats', 'specimens.int_z', 'specimens.int_maxdev', 'specimens.int_gmax', 'specimens.int_mad_anc', 'specimens.int_scat', 'specimens.int_r2_corr', 'specimens.int_b_beta', 'specimens.int_dck', 'specimens.treat_dc_field', 'specimens.dir_inc', 'specimens.int_mdrat', 'specimens.int_theta', 'specimens.int_ptrm', 'specimens.meas_step_min', 'specimens.int_dtr', 'specimens.int_alpha', 'specimens.int_fvds', 'specimens.int_b_sigma', 'specimens.int_b', 'specimens.int_g', 'specimens.int_f', 'specimens.meas_step_max', 'specimens.int_n_measurements', 'specimens.int_q', 'specimens.int_dang',  'specimens.int_k_sse', 'specimens.int_gamma', 'specimens.int_k', 'specimens.int_crm', 'specimens.int_dt', 'specimens.int_k_prime', 'specimens.int_k_prime_sse','samples.int_n_specimens','samples.int_abs_sigma_perc','samples.int_abs_sigma','sites.int_n_specimens','sites.int_abs_sigma_perc','sites.int_abs_sigma','criterion']
spd2magic_map = dict(zip(spd, magic))
magic2spd_map = dict(zip(magic, spd))


# mapping between magic2 and magic3

#measurement data translation measurements.txt -> magic_measurements.txt
meas_magic3_2_magic2_map = {'treat_dc_field_theta': 'treatment_dc_field_theta', 'sample': 'er_sample_name', 'treat_dc_field': 'treatment_dc_field', 'instrument_codes': 'magic_instrument_codes', 'description': 'measurement_description', 'magn_volume': 'measurement_magn_volume', 'specimen': 'er_specimen_name', 'treat_dc_field_phi': 'treatment_dc_field_phi', 'number': 'measurement_number', 'site': 'er_site_name', 'treat_ac_field': 'treatment_ac_field', 'quality': 'measurement_flag', 'dir_inc': 'measurement_inc', 'location': 'er_location_name', 'dir_dec': 'measurement_dec', 'method_codes': 'magic_method_codes', 'treat_temp': 'treatment_temp', 'magn_moment': 'measurement_magn_moment', 'magn_mass': 'measurement_magn_mass', 'dir_csd': 'measurement_csd','experiment':'magic_experiment_name', 'meas_field_dc': 'measurement_lab_field_dc', 'scientists': 'er_scientist_mail_names', 'citations': 'er_citation_names'}

meas_magic2_2_magic3_map = {v:k for k,v in meas_magic3_2_magic2_map.items()}

#measurement data translation magic_measurements.txt -> measurements.txt
#meas_magic2_2_magic3_map = {'treatment_ac_field': 'treat_ac_field', 'measurement_number': 'number', 'treatment_dc_field_theta': 'treat_dc_field_theta', 'er_site_name': 'site', 'er_sample_name': 'sample', 'treatment_dc_field_phi': 'treat_dc_field_phi', 'measurement_magn_volume': 'magn_volume', 'magic_instrument_codes': 'instrument_codes', 'measurement_description': 'description', 'er_location_name': 'location', 'measurement_dec': 'dir_dec', 'measurement_flag': 'quality', 'measurement_magn_moment': 'magn_moment', 'measurement_inc': 'dir_inc', 'treatment_temp': 'treat_temp', 'er_specimen_name': 'specimen', 'measurement_csd': 'dir_csd', 'treatment_dc_field': 'treat_dc_field', 'measurement_magn_mass': 'magn_mass', 'magic_method_codes': 'method_codes','magic_experiment_name' : 'experiment', 'measurement_temp' : 'meas_temp', 'measurement_standard' : 'standard', 'measurement_positions' : 'meas_n_orient', 'measurement_sd_x' : 'magn_x_sigma', 'measurement_sd_y' : 'magn_y_sigma', 'measurement_sd_z' : 'magn_z_sigma', 'magic_software_packages' : 'software_packages', 'er_citation_names': 'citations', 'meas_field_dc': 'measurement_lab_field_dc'}


#specimen data translation pmag_speciemns,er_specimens -> specimens.txt
spec_magic3_2_magic2_map = {'int_drats': 'specimen_drats', 'site': 'er_site_name', 'int_mad': 'specimen_int_mad', 'sample': 'er_sample_name', 'int_n_measurements': 'specimen_int_n', 'int_corr': 'specimen_correction', 'int_rsc': 'specimen_rsc', 'analyst_names': 'er_analyst_mail_names', 'int_scat': 'specimen_scat', 'int_ptrm_n': 'specimen_int_ptrm_n', 'citations': 'er_citation_names', 'int_gmax': 'specimen_gmax', 'int_dang': 'specimen_int_dang', 'dir_tilt_correction': 'specimen_tilt_correction', 'location': 'er_location_name', 'dir_comp': 'specimen_comp_name', 'specimen_magn_moment': 'magn_moment', 'int_w': 'specimen_w', 'specimen': 'er_specimen_name', 'int_q': 'specimen_q', 'int_fvds': 'specimen_fvds', 'specimen_mad': 'dir_mad_free', 'int_frac': 'specimen_frac', 'meas_step_min': 'measurement_step_min', 'int_f': 'specimen_f', 'software_packages': 'magic_software_packages', 'dir_mad_free': 'specimen_mad', 'magn_moment': 'specimen_magn_moment', 'instrument_codes': 'magic_instrument_codes', 'int_b_beta': 'specimen_b_beta', 'dir_n_comps': 'specimen_comp_n', 'int_md': 'specimen_md', 'dir_n_measurements': 'specimen_n', 'dir_inc': 'specimen_inc', 'specimen_magn_volumn': 'magn_volumn', 'meas_step_max': 'measurement_step_max', 'dir_alpha95': 'specimen_alpha95', 'magn_volumne': 'specimen_magn_volumn', 'measurement_step_min': 'meas_step_min', 'meas_step_unit': 'measurement_step_unit', 'dir_dec': 'specimen_dec', 'method_codes': 'magic_method_codes', 'result_quality': 'specimen_flag', 'dir_dang': 'specimen_dang', 'geologic_classes': 'specimen_class', 'experiments': 'magic_experiment_names', 'int_b': 'specimen_b', 'int_b_sigma': 'specimen_b_sigma', 'int_abs': 'specimen_int', 'int_treat_dc_field': 'specimen_lab_field_dc', 'lithologies': 'specimen_lithology', 'geologic_types': 'specimen_type', 'int_gamma': 'specimen_gamma'}

spec_magic2_2_magic3_map = {v:k for k,v in spec_magic3_2_magic2_map.items()}


#samp_magic2_2_magic3_map = {v:k for k,v in samp_magic3_2_magic2_map.items()}

#site data translation pmag_sites,er_sites -> sites.txt and back
site_magic3_2_magic2_map = {'int_abs_sigma': 'site_int_sigma', 'int_abs_sigma_perc': 'site_int_sigma_perc',
                            'int_n_samples': 'site_int_n', 'dir_alpha95': 'site_alpha95', 'dir_k': 'site_k',
                            'dir_n_samples': 'site_n', 'dir_n_specimens_lines': 'site_n_lines',
                            'dir_n_specimens_planes': 'site_n_planes', 'dir_r': 'site_r',
                            'criteria': 'pmag_criteria_codes', 'method_codes': 'magic_method_codes',
                            'site': 'er_site_name', 'software_packages': 'magic_software_packages',
                            'location': 'er_location_name', 'citations': 'er_citation_names',
                            'geologic_classes': 'site_class', 'height': 'site_height', 'lat': 'site_lat',
                            'lon': 'site_lon', 'geologic_types': 'site_type', 'lithologies': 'site_lithology',
                            'samples': 'er_sample_names', 'specimens': 'er_specimen_names',
                            'analysts': 'er_analyst_mail_names', 'dir_comp_name': 'site_comp_name',
                            'dir_dec': 'site_dec', 'description': 'site_description', 'dir_inc': 'site_inc',
                            'age': 'site_inferred_age', 'age_sigma': 'site_inferred_age_sigma',
                            'age_unit': 'site_inferred_age_unit', 'int_abs': 'site_int',
                            'dir_polarity': 'site_polarity', 'dir_tilt_correction': 'site_tilt_correction'}

site_magic2_2_magic3_map = {v: k for k, v in site_magic3_2_magic2_map.items()}

loc_magic3_2_magic2_map = {'location': 'er_location_name', 'sites': 'er_site_names', 'citations': 'er_citation_names',
                           'lat_s': 'location_begin_lat', 'lon_w': 'location_begin_lon', 'lat_n': 'location_end_lat',
                           'lon_e': 'location_end_lon', 'location_alternatives': 'er_location_alternatives'}

loc_magic2_2_magic3_map = {v: k for k, v in list(loc_magic3_2_magic2_map.items())}

aniso_magic3_2_magic2_map={'specimen':'er_specimen_name', 'aniso_type':'anisotropy_type', 'description':'result_description', 'aniso_ftest':'anisotropy_ftest', 'aniso_ftest12':'anisotropy_ftest12', 'aniso_ftest23':'anisotropy_ftest23', 'aniso_s_mean':'anisotropy_mean', 'aniso_s_n_measurements':'anisotropy_n', 'aniso_s_sigma':'anisotropy_sigma', 'aniso_s_unit':'anisotropy_unit', 'aniso_tilt_correction':'anisotropy_tilt_correction'}

aniso_magic2_2_magic3_map={'anisotropy_ftest23': 'aniso_ftest23', 'anisotropy_ftest': 'aniso_ftest', 'anisotropy_sigma': 'aniso_s_sigma', 'anisotropy_type': 'aniso_type', 'anisotropy_ftest12': 'aniso_ftest12', 'anisotropy_tilt_correction': 'aniso_tilt_correction', 'er_specimen_name': 'specimen', 'anisotropy_unit': 'aniso_s_unit', 'anisotropy_mean': 'aniso_s_mean', 'result_description': 'description', 'anisotropy_n': 'aniso_s_n_measurements','pmag_criteria_codes':'criteria','result_quality':'result_quality'}


# sample data translation pmag_samples.txt => samples.txt
samp_magic2_2_magic3_map = {'sample_n_planes': 'dir_n_specimens_planes', 'sample_n_lines': 'dir_n_specimens_lines',
                            'sample_r': 'dir_r', 'sample_n': 'dir_n_specimens', 'sample_k': 'dir_k',
                            'sample_int_sigma_perc': 'int_abs_sigma_perc', 'sample_int_n': 'int_n_specimens',
                            'sample_alpha95': 'dir_alpha95', 'sample_int_sigma': 'int_abs_sigma',
                            'pmag_criteria_codes': 'criteria', 'magic_method_codes':'method_codes',
                            'magic_software_packages': 'software_packages', # LJ started adding here
                            'sample_class': 'geologic_classes',
                            'sample_lon': 'lon', 'sample_height': 'height', "er_sample_name": "sample",
                            "er_site_name": "site", "sample_description": "description",
                            "sample_bed_dip": "bed_dip", "er_scientist_mail_names": "scientists",
                            "er_citation_names": "citations", "sample_texture": "texture",
                            "sample_declination_correction": "azimuth_dec_correction",
                            "sample_lithology": "lithologies", "sample_lat": "lat", "sample_lon": "lon",
                            "sample_type": "geologic_types", "sample_igsn": "igsn",
                            "er_sample_alternatives": "sample_alternatives", "sample_azimuth": "azimuth",
                            "sample_cooling_rate": "cooling_rate", "er_location_name": "location",
                            "sample_dip": "dip", "sample_date": "timestamp",
                            "sample_bed_dip_direction": "bed_dip_direction"}

#sample data translation samples.txt => pmag_samples.txt
samp_magic3_2_magic2_map = {'dir_n_specimens_planes': 'sample_n_planes', 'dir_n_specimens_lines': 'sample_n_lines',
                            'dir_r': 'sample_r', 'dir_n_specimens': 'sample_n', 'dir_k': 'sample_k',
                            'int_abs_sigma_perc' : 'sample_int_sigma_perc', 'int_n_specimens': 'sample_int_n',
                            'dir_alpha95': 'sample_alpha95', 'int_abs_sigma': 'sample_int_sigma',
                            'criteria': 'pmag_criteria_codes', "method_codes": "magic_method_codes",
                            'software_packages':'magic_software_packages', # LJ started adding here
                            "geologic_classes": "sample_class",
                            "lon": "sample_lon", "height": "sample_height", "sample": "er_sample_name",
                            "site": "er_site_name", "description": "sample_description",
                            "bed_dip": "sample_bed_dip", "scientists": "er_scientist_mail_names",
                            "citations": "er_citation_names", "texture": "sample_texture",
                            "azimuth_dec_correction": "sample_declination_correction",
                            "lithologies": "sample_lithology", "lat": "sample_lat", "lon": "sample_lon",
                            "geologic_types": "sample_type", "igsn": "sample_igsn",
                            "sample_alternatives": "er_sample_alternatives", "azimuth": "sample_azimuth",
                            "cooling_rate": "sample_cooling_rate", "location": "er_location_name",
                            "dip": "sample_dip", "timestamp": "sample_date",
                            "bed_dip_direction": "sample_bed_dip_direction"}

image_magic2_2_magic3_map = {"er_location_name": "location", "er_site_name": "site", "er_sample_name": "sample",
                             "er_specimen_name": "specimen", "er_image_name": "file", "image_type": "type",
                             "image_title": "title", "image_keywords": "keywords",
                             "er_image_description": "description", "image_date": "timestamp",
                             "er_analyst_mail_names": "analysts", "er_photographer_mail_names": "photographers",
                             "er_citation_names": "citations"}

image_magic3_2_magic_2_map = {"location": "er_location_name", "site": "er_site_name", "sample": "er_sample_name",
                              "specimen": "er_specimen_name", "file": "er_image_name", "type": "image_type",
                              "description": "er_image_description", "timestamp": "image_date",
                              "analysts": "er_analyst_mail_names", "photographers": "er_photographer_mail_names",
                              "citations": "er_citation_names"}

## orientation format --> 3.0.

# orientation headers: not all have a 3.0 sample equivalent (like mag_azimuth, for instance)
#site_name sample_name mag_azimuth field_dip date lat long sample_lithology sample_type sample_class shadow_angle hhmm stratigraphic_height bedding_dip_direction bedding_dip GPS_baseline image_name image_look image_photographer participants method_codes site_description sample_description GPS_Az, sample_igsn, sample_texture, sample_cooling_rate, cooling_rate_corr, cooling_rate_mcd

orient_magic_2_magic3_map = {"sample_name": "sample", "site_name": "site", "long": "lon",
                             "sample_lithology": "lithologies", "sample_type": "geologic_types",
                             "sample_class": "geologic_classes"}

magic3_2_orient_magic_map = {"sample": "sample_name", "site": "site_name", "lon": "long",
                             "lithologies": "sample_lithology", "geologic_types": "sample_type",
                             "geologic_classes": "sample_class"}





meas_magic2 = meas_magic3_2_magic2_map.values()
spec_magic2 = spec_magic3_2_magic2_map.values()
samp_magic2 = samp_magic3_2_magic2_map.values()
site_magic2 = site_magic3_2_magic2_map.values()


#specimen data translation pmag_speciemns,er_specimens -> specimens.txt


#samp_magic2 = ['sample_n_planes', 'sample_n_lines', 'sample_r', 'sample_n', 'sample_k', 'sample_int_sigma_perc', 'sample_int_n': 'sample_alpha95', 'sample_int_sigma': 'int_abs_sigma','pmag_criteria_codes':'criteria','magic_method_codes':'method_codes','magic_software_packages':'software_packages'}

#samp_magic3






#meas_magic3 = meas_magic3_2_magic2_map.keys()  # why are these here?
spec_magic3 = spec_magic2_2_magic3_map.keys()
#samp_magic3 = samp_magic3_2_magic2_map.keys()
site_magic3 = site_magic3_2_magic2_map.keys()



def convert_intensity_criteria(direction,crit):
    magic2 = ['specimen_coeff_det_sq', 'specimen_int_ptrm_tail_n', 'specimen_dpal', 'specimen_tail_drat', 'specimen_md', 'specimen_ac_n', 'specimen_dac',  'specimen_int_mad', 'specimen_int_ptrm_n', 'specimen_drat', 'specimen_z_md', 'specimen_frac', 'specimen_cdrat', 'specimen_dec', 'specimen_mdev', 'specimen_drats', 'specimen_z', 'specimen_maxdev', 'specimen_gmax', 'specimen_int_mad_anc', 'specimen_scat', 'specimen_r_sq', 'specimen_b_beta', 'specimen_dck', 'lab_dc_field', 'specimen_inc', 'specimen_mdrat', 'specimen_theta', 'specimen_ptrm', 'measurement_step_min', 'specimen_dtr', 'specimen_int_alpha', 'specimen_fvds', 'specimen_b_sigma', 'specimen_b', 'specimen_g', 'specimen_f', 'measurement_step_max', 'specimen_int_n', 'specimen_q', 'specimen_int_dang', 'specimen_k_sse', 'specimen_gamma', 'specimen_k', 'specimen_int_crm', 'specimen_dt', 'specimen_k_prime', 'specimen_k_prime_sse','sample_int_n','sample_int_sigma_perc','sample_int_sigma','site_int_n','site_int_sigma_perc','site_int_sigma','pmag_criteria_code']
    magic3 = ['specimens.int_r2_det', 'specimens.int_n_ptrm_tail', 'specimens.int_dpal', 'specimens.int_drat_tail', 'specimens.int_md', 'specimens.int_n_ac', 'specimens.int_dac', 'specimens.int_mad', 'specimens.int_n_ptrm', 'specimens.int_drat', 'specimens.int_z_md', 'specimens.int_frac', 'specimens.int_cdrat', 'specimens.dir_dec', 'specimens.int_mdev', 'specimens.int_drats', 'specimens.int_z', 'specimens.int_maxdev', 'specimens.int_gmax', 'specimens.int_mad_anc', 'specimens.int_scat', 'specimens.int_r2_corr', 'specimens.int_b_beta', 'specimens.int_dck', 'specimens.treat_dc_field', 'specimens.dir_inc', 'specimens.int_mdrat', 'specimens.int_theta', 'specimens.int_ptrm', 'specimens.meas_step_min', 'specimens.int_dtr', 'specimens.int_alpha', 'specimens.int_fvds', 'specimens.int_b_sigma', 'specimens.int_b', 'specimens.int_g', 'specimens.int_f', 'specimens.meas_step_max', 'specimens.int_n_measurements', 'specimens.int_q', 'specimens.int_dang',  'specimens.int_k_sse', 'specimens.int_gamma', 'specimens.int_k', 'specimens.int_crm', 'specimens.int_dt', 'specimens.int_k_prime', 'specimens.int_k_prime_sse','samples.int_n_specimens','samples.int_sigma_perc','samples.int_sigma','sites.int_n_specimens','sites.int_sigma_perc','sites.int_sigma','criterion']
    if direction=='magic2':
        if crit in magic3:
            return magic2[magic3.index(crit)]
        else:
            return ""
    else:
        if crit in magic2:
            return magic3[magic2.index(crit)]
        else:
            return crit

def convert_direction_criteria(direction,crit):
    if direction=='magic2':
        try:
            if 'specimens.' in crit:
                return spec_magic3_2_magic2_map[crit.lstrip('specimens.')]
            elif 'samples.' in crit:
                return samp_magic3_2_magic2_map[crit.lstrip('samples.')]
            elif 'sites.' in crit:
                return site_magic3_2_magic2_map[crit.lstrip('sites.')]
            else:
                return ""
        except KeyError as e: return ""
    else:
        try:
            if 'specimen' in crit:
                return 'specimens.' + spec_magic2_2_magic3_map[crit]
            elif 'sample' in crit:
                return 'samples.' + samp_magic2_2_magic3_map[crit]
            elif 'site' in crit:
                return 'sites.' + site_magic2_2_magic3_map[crit]
            else:
                return ""
        except KeyError as e: return ""

def convert_meas(direction,Rec):
    if direction=='magic3':
        columns=meas_magic2_2_magic3_map
        MeasRec={}
        for key in columns:
            if key in Rec.keys():
                MeasRec[columns[key]]=Rec[key] # transfer info and change column name to data model 3.0
        return MeasRec
    else: # haven't added this way yet
        pass

def convert_spec(direction,Rec):
    if direction=='magic3':
        columns=spec_magic2_2_magic3_map
        SpecRec={}
        for key in columns:
            if key in Rec.keys():
                SpecRec[columns[key]]=Rec[key] # transfer info and change column name to data model 3.0
        return SpecRec
    else: # haven't added this way yet
        pass

def convert_samp(direction,Rec):
    if direction=='magic3':
        columns=samp_magic2_2_magic3_map
        SampRec={}
        for key in columns:
            if key in Rec.keys():
                SampRec[columns[key]]=Rec[key] # transfer info and change column name to data model 3.0
        return SampRec
    else: # haven't added this way yet
        pass

def convert_site(direction,Rec):
    if direction=='magic3':
        columns=site_magic2_2_magic3_map
        SiteRec={}
        for key in columns:
            if key in Rec.keys():
                SiteRec[columns[key]]=Rec[key] # transfer info and change column name to data model 3.0
        return SiteRec
    else: # haven't added this way yet
        pass


def convert_aniso(direction,AniSpec):
    if direction=='magic2':
        columns=aniso_magic3_2_magic2_map
        AniRec={}
        s_data=AniSpec['aniso_s'].split(':')
        for key in columns:
            if key in AniSpec.keys():
                AniRec[columns[key]]=AniSpec[key] # transfer info and change column name to data model 2.5
        AniRec['anisotropy_s1']=s_data[0]# need to add these things
        AniRec['anisotropy_s2']=s_data[1]
        AniRec['anisotropy_s3']=s_data[2]
        AniRec['anisotropy_s4']=s_data[3]
        AniRec['anisotropy_s5']=s_data[4]
        AniRec['anisotropy_s6']=s_data[5]
        AniRec['anisotropy_F_crit']=""
        if 'result_description'  in AniSpec.keys():
            result_description=AniSpec['result_description'].split(";")
            for description in result_description:
              if "Critical F" in description:
                 desc=description.split(":")
                 AniRec['anisotropy_F_crit']=float(desc[1])
        return AniRec # converted to 2.5
    else:  # upgrade to 3.0
        columns=aniso_magic2_2_magic3_map
        # first fix aniso_s
        AniRec={}
        for key in columns:
            if key in AniSpec.keys():
                AniRec[columns[key]]=AniSpec[key] # transfer info and change column name to data model 3.0
        s_string=""
        s_string=s_string+ str(AniSpec['anisotropy_s1']) +' : '
        s_string=s_string+ str(AniSpec['anisotropy_s2']) +' : '
        s_string=s_string+ str(AniSpec['anisotropy_s3']) +' : '
        s_string=s_string+ str(AniSpec['anisotropy_s4']) +' : '
        s_string=s_string+ str(AniSpec['anisotropy_s5']) +' : '
        s_string=s_string+ str(AniSpec['anisotropy_s6'])
        AniRec['aniso_s']=s_string
        # do V1, etc.  here
#V1:  Anisotropy eigenparameters for the maximum eigenvalue (T1), a colon-delimited list of tau (T1), dec, inc, confidence ellipse type, and confidence ellipse parameters
        v_string=AniSpec['anisotropy_t1']+" : "+AniSpec['anisotropy_v1_dec']+" : "+AniSpec['anisotropy_v1_inc']
        AniRec['aniso_v1']=v_string
        v_string=AniSpec['anisotropy_t2']+" : "+AniSpec['anisotropy_v2_dec']+" : "+AniSpec['anisotropy_v2_inc']
        AniRec['aniso_v2']=v_string
        v_string=AniSpec['anisotropy_t3']+" : "+AniSpec['anisotropy_v3_dec']+" : "+AniSpec['anisotropy_v3_inc']
        AniRec['aniso_v3']=v_string
        return AniRec
