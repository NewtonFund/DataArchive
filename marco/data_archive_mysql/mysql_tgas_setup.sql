CREATE TABLE DA (
 Teff FLOAT,
 logg FLOAT,
 Msun FLOAT,
 Mbol FLOAT,
 BC FLOAT,
 U FLOAT,
 B FLOAT,
 V FLOAT,
 R FLOAT,
 I FLOAT,
 J FLOAT,
 H FLOAT,
 K FLOAT,
 sdssu FLOAT,
 sdssg FLOAT,
 sdssr FLOAT,
 sdssi FLOAT,
 sdssz FLOAT,
 stromy FLOAT,
 stromby FLOAT,
 stromub FLOAT,
 stromvy FLOAT,
 VI FLOAT,
 GR FLOAT,
 UV FLOAT,
 UG FLOAT,
 BV FLOAT,
 Age FLOAT
);

load data local infile '/Users/marcolam/Desktop/DA.csv' into table DA fields terminated by ','
  enclosed by '"'
  lines terminated by '\n'
IGNORE 1 LINES
    (Teff, logg, Msun, Mbol, BC, U, B, V, R, I, J, H, K, sdssu, sdssg, sdssr, sdssi, sdssz, stromy, stromby, stromub, stromvy, VI, GR, UV, UG, BV, Age);





CREATE TABLE tgas (
hip TEXT,
tycho2_id TEXT,
solution_id LONG,
source_id LONG,
random_index LONG,
ref_epoch FLOAT,
ra FLOAT,
ra_error FLOAT,
declination FLOAT,
dec_error FLOAT,
parallax FLOAT,
parallax_error FLOAT,
pmra FLOAT,
pmra_error FLOAT,
pmdec FLOAT,
pmdec_error FLOAT,
ra_dec_corr FLOAT,
ra_parallax_corr FLOAT,
ra_pmra_corr FLOAT,
ra_pmdec_corr FLOAT,
dec_parallax_corr FLOAT,
dec_pmra_corr FLOAT,
dec_pmdec_corr FLOAT,
parallax_pmra_corr FLOAT,
parallax_pmdec_corr FLOAT,
pmra_pmdec_corr FLOAT,
astrometric_n_obs_al INT,
astrometric_n_obs_ac INT,
astrometric_n_good_obs_al INT,
astrometric_n_good_obs_ac INT,
astrometric_n_bad_obs_al INT,
astrometric_n_bad_obs_ac INT,
astrometric_delta_q TEXT,
astrometric_excess_noise FLOAT,
astrometric_excess_noise_sig FLOAT,
astrometric_primary_flag TEXT,
astrometric_relegation_factor FLOAT,
astrometric_weight_al FLOAT,
astrometric_weight_ac TEXT,
astrometric_priors_used INT,
matched_observations BOOLEAN,
duplicated_source TEXT,
scan_direction_strength_k1 FLOAT,
scan_direction_strength_k2 FLOAT,
scan_direction_strength_k3 FLOAT,
scan_direction_strength_k4 FLOAT,
scan_direction_mean_k1 FLOAT,
scan_direction_mean_k2 FLOAT,
scan_direction_mean_k3 FLOAT,
scan_direction_mean_k4 FLOAT,
phot_g_n_obs INT,
phot_g_mean_flux FLOAT,
phot_g_mean_flux_error FLOAT,
phot_g_mean_mag FLOAT,
phot_variable_flag TEXT,
l FLOAT,
b FLOAT,
ecl_lon FLOAT,
ecl_lat FLOAT
);





load data local infile '/Users/marcolam/Documents/tgas_source/tgas_source/TgasSource_000-000-000.csv' into table tgas fields terminated by ','
  enclosed by '"'
  lines terminated by '\n'
IGNORE 1 LINES
    (hip,tycho2_id,solution_id,source_id,random_index,ref_epoch,ra,ra_error,declination,dec_error,parallax,parallax_error,pmra,pmra_error,pmdec,pmdec_error,ra_dec_corr,ra_parallax_corr,ra_pmra_corr,ra_pmdec_corr,dec_parallax_corr,dec_pmra_corr,dec_pmdec_corr,parallax_pmra_corr,parallax_pmdec_corr,pmra_pmdec_corr,astrometric_n_obs_al,astrometric_n_obs_ac,astrometric_n_good_obs_al,astrometric_n_good_obs_ac,astrometric_n_bad_obs_al,astrometric_n_bad_obs_ac,astrometric_delta_q,astrometric_excess_noise,astrometric_excess_noise_sig,astrometric_primary_flag,astrometric_relegation_factor,astrometric_weight_al,astrometric_weight_ac,astrometric_priors_used,matched_observations,duplicated_source,scan_direction_strength_k1,scan_direction_strength_k2,scan_direction_strength_k3,scan_direction_strength_k4,scan_direction_mean_k1,scan_direction_mean_k2,scan_direction_mean_k3,scan_direction_mean_k4,phot_g_n_obs,phot_g_mean_flux,phot_g_mean_flux_error,phot_g_mean_mag,phot_variable_flag,l,b,ecl_lon,ecl_lat);


load data local infile '/Users/marcolam/Documents/tgas_source/tgas_source/TgasSource_000-000-001.csv' into table tgas fields terminated by ','
  enclosed by '"'
  lines terminated by '\n'
IGNORE 1 LINES
    (hip,tycho2_id,solution_id,source_id,random_index,ref_epoch,ra,ra_error,declination,dec_error,parallax,parallax_error,pmra,pmra_error,pmdec,pmdec_error,ra_dec_corr,ra_parallax_corr,ra_pmra_corr,ra_pmdec_corr,dec_parallax_corr,dec_pmra_corr,dec_pmdec_corr,parallax_pmra_corr,parallax_pmdec_corr,pmra_pmdec_corr,astrometric_n_obs_al,astrometric_n_obs_ac,astrometric_n_good_obs_al,astrometric_n_good_obs_ac,astrometric_n_bad_obs_al,astrometric_n_bad_obs_ac,astrometric_delta_q,astrometric_excess_noise,astrometric_excess_noise_sig,astrometric_primary_flag,astrometric_relegation_factor,astrometric_weight_al,astrometric_weight_ac,astrometric_priors_used,matched_observations,duplicated_source,scan_direction_strength_k1,scan_direction_strength_k2,scan_direction_strength_k3,scan_direction_strength_k4,scan_direction_mean_k1,scan_direction_mean_k2,scan_direction_mean_k3,scan_direction_mean_k4,phot_g_n_obs,phot_g_mean_flux,phot_g_mean_flux_error,phot_g_mean_mag,phot_variable_flag,l,b,ecl_lon,ecl_lat);


load data local infile '/Users/marcolam/Documents/tgas_source/tgas_source/TgasSource_000-000-002.csv' into table tgas fields terminated by ','
  enclosed by '"'
  lines terminated by '\n'
IGNORE 1 LINES
    (hip,tycho2_id,solution_id,source_id,random_index,ref_epoch,ra,ra_error,declination,dec_error,parallax,parallax_error,pmra,pmra_error,pmdec,pmdec_error,ra_dec_corr,ra_parallax_corr,ra_pmra_corr,ra_pmdec_corr,dec_parallax_corr,dec_pmra_corr,dec_pmdec_corr,parallax_pmra_corr,parallax_pmdec_corr,pmra_pmdec_corr,astrometric_n_obs_al,astrometric_n_obs_ac,astrometric_n_good_obs_al,astrometric_n_good_obs_ac,astrometric_n_bad_obs_al,astrometric_n_bad_obs_ac,astrometric_delta_q,astrometric_excess_noise,astrometric_excess_noise_sig,astrometric_primary_flag,astrometric_relegation_factor,astrometric_weight_al,astrometric_weight_ac,astrometric_priors_used,matched_observations,duplicated_source,scan_direction_strength_k1,scan_direction_strength_k2,scan_direction_strength_k3,scan_direction_strength_k4,scan_direction_mean_k1,scan_direction_mean_k2,scan_direction_mean_k3,scan_direction_mean_k4,phot_g_n_obs,phot_g_mean_flux,phot_g_mean_flux_error,phot_g_mean_mag,phot_variable_flag,l,b,ecl_lon,ecl_lat);


load data local infile '/Users/marcolam/Documents/tgas_source/tgas_source/TgasSource_000-000-003.csv' into table tgas fields terminated by ','
  enclosed by '"'
  lines terminated by '\n'
IGNORE 1 LINES
    (hip,tycho2_id,solution_id,source_id,random_index,ref_epoch,ra,ra_error,declination,dec_error,parallax,parallax_error,pmra,pmra_error,pmdec,pmdec_error,ra_dec_corr,ra_parallax_corr,ra_pmra_corr,ra_pmdec_corr,dec_parallax_corr,dec_pmra_corr,dec_pmdec_corr,parallax_pmra_corr,parallax_pmdec_corr,pmra_pmdec_corr,astrometric_n_obs_al,astrometric_n_obs_ac,astrometric_n_good_obs_al,astrometric_n_good_obs_ac,astrometric_n_bad_obs_al,astrometric_n_bad_obs_ac,astrometric_delta_q,astrometric_excess_noise,astrometric_excess_noise_sig,astrometric_primary_flag,astrometric_relegation_factor,astrometric_weight_al,astrometric_weight_ac,astrometric_priors_used,matched_observations,duplicated_source,scan_direction_strength_k1,scan_direction_strength_k2,scan_direction_strength_k3,scan_direction_strength_k4,scan_direction_mean_k1,scan_direction_mean_k2,scan_direction_mean_k3,scan_direction_mean_k4,phot_g_n_obs,phot_g_mean_flux,phot_g_mean_flux_error,phot_g_mean_mag,phot_variable_flag,l,b,ecl_lon,ecl_lat);


load data local infile '/Users/marcolam/Documents/tgas_source/tgas_source/TgasSource_000-000-004.csv' into table tgas fields terminated by ','
  enclosed by '"'
  lines terminated by '\n'
IGNORE 1 LINES
    (hip,tycho2_id,solution_id,source_id,random_index,ref_epoch,ra,ra_error,declination,dec_error,parallax,parallax_error,pmra,pmra_error,pmdec,pmdec_error,ra_dec_corr,ra_parallax_corr,ra_pmra_corr,ra_pmdec_corr,dec_parallax_corr,dec_pmra_corr,dec_pmdec_corr,parallax_pmra_corr,parallax_pmdec_corr,pmra_pmdec_corr,astrometric_n_obs_al,astrometric_n_obs_ac,astrometric_n_good_obs_al,astrometric_n_good_obs_ac,astrometric_n_bad_obs_al,astrometric_n_bad_obs_ac,astrometric_delta_q,astrometric_excess_noise,astrometric_excess_noise_sig,astrometric_primary_flag,astrometric_relegation_factor,astrometric_weight_al,astrometric_weight_ac,astrometric_priors_used,matched_observations,duplicated_source,scan_direction_strength_k1,scan_direction_strength_k2,scan_direction_strength_k3,scan_direction_strength_k4,scan_direction_mean_k1,scan_direction_mean_k2,scan_direction_mean_k3,scan_direction_mean_k4,phot_g_n_obs,phot_g_mean_flux,phot_g_mean_flux_error,phot_g_mean_mag,phot_variable_flag,l,b,ecl_lon,ecl_lat);


load data local infile '/Users/marcolam/Documents/tgas_source/tgas_source/TgasSource_000-000-005.csv' into table tgas fields terminated by ','
  enclosed by '"'
  lines terminated by '\n'
IGNORE 1 LINES
    (hip,tycho2_id,solution_id,source_id,random_index,ref_epoch,ra,ra_error,declination,dec_error,parallax,parallax_error,pmra,pmra_error,pmdec,pmdec_error,ra_dec_corr,ra_parallax_corr,ra_pmra_corr,ra_pmdec_corr,dec_parallax_corr,dec_pmra_corr,dec_pmdec_corr,parallax_pmra_corr,parallax_pmdec_corr,pmra_pmdec_corr,astrometric_n_obs_al,astrometric_n_obs_ac,astrometric_n_good_obs_al,astrometric_n_good_obs_ac,astrometric_n_bad_obs_al,astrometric_n_bad_obs_ac,astrometric_delta_q,astrometric_excess_noise,astrometric_excess_noise_sig,astrometric_primary_flag,astrometric_relegation_factor,astrometric_weight_al,astrometric_weight_ac,astrometric_priors_used,matched_observations,duplicated_source,scan_direction_strength_k1,scan_direction_strength_k2,scan_direction_strength_k3,scan_direction_strength_k4,scan_direction_mean_k1,scan_direction_mean_k2,scan_direction_mean_k3,scan_direction_mean_k4,phot_g_n_obs,phot_g_mean_flux,phot_g_mean_flux_error,phot_g_mean_mag,phot_variable_flag,l,b,ecl_lon,ecl_lat);


load data local infile '/Users/marcolam/Documents/tgas_source/tgas_source/TgasSource_000-000-006.csv' into table tgas fields terminated by ','
  enclosed by '"'
  lines terminated by '\n'
IGNORE 1 LINES
    (hip,tycho2_id,solution_id,source_id,random_index,ref_epoch,ra,ra_error,declination,dec_error,parallax,parallax_error,pmra,pmra_error,pmdec,pmdec_error,ra_dec_corr,ra_parallax_corr,ra_pmra_corr,ra_pmdec_corr,dec_parallax_corr,dec_pmra_corr,dec_pmdec_corr,parallax_pmra_corr,parallax_pmdec_corr,pmra_pmdec_corr,astrometric_n_obs_al,astrometric_n_obs_ac,astrometric_n_good_obs_al,astrometric_n_good_obs_ac,astrometric_n_bad_obs_al,astrometric_n_bad_obs_ac,astrometric_delta_q,astrometric_excess_noise,astrometric_excess_noise_sig,astrometric_primary_flag,astrometric_relegation_factor,astrometric_weight_al,astrometric_weight_ac,astrometric_priors_used,matched_observations,duplicated_source,scan_direction_strength_k1,scan_direction_strength_k2,scan_direction_strength_k3,scan_direction_strength_k4,scan_direction_mean_k1,scan_direction_mean_k2,scan_direction_mean_k3,scan_direction_mean_k4,phot_g_n_obs,phot_g_mean_flux,phot_g_mean_flux_error,phot_g_mean_mag,phot_variable_flag,l,b,ecl_lon,ecl_lat);


load data local infile '/Users/marcolam/Documents/tgas_source/tgas_source/TgasSource_000-000-007.csv' into table tgas fields terminated by ','
  enclosed by '"'
  lines terminated by '\n'
IGNORE 1 LINES
    (hip,tycho2_id,solution_id,source_id,random_index,ref_epoch,ra,ra_error,declination,dec_error,parallax,parallax_error,pmra,pmra_error,pmdec,pmdec_error,ra_dec_corr,ra_parallax_corr,ra_pmra_corr,ra_pmdec_corr,dec_parallax_corr,dec_pmra_corr,dec_pmdec_corr,parallax_pmra_corr,parallax_pmdec_corr,pmra_pmdec_corr,astrometric_n_obs_al,astrometric_n_obs_ac,astrometric_n_good_obs_al,astrometric_n_good_obs_ac,astrometric_n_bad_obs_al,astrometric_n_bad_obs_ac,astrometric_delta_q,astrometric_excess_noise,astrometric_excess_noise_sig,astrometric_primary_flag,astrometric_relegation_factor,astrometric_weight_al,astrometric_weight_ac,astrometric_priors_used,matched_observations,duplicated_source,scan_direction_strength_k1,scan_direction_strength_k2,scan_direction_strength_k3,scan_direction_strength_k4,scan_direction_mean_k1,scan_direction_mean_k2,scan_direction_mean_k3,scan_direction_mean_k4,phot_g_n_obs,phot_g_mean_flux,phot_g_mean_flux_error,phot_g_mean_mag,phot_variable_flag,l,b,ecl_lon,ecl_lat);


load data local infile '/Users/marcolam/Documents/tgas_source/tgas_source/TgasSource_000-000-008.csv' into table tgas fields terminated by ','
  enclosed by '"'
  lines terminated by '\n'
IGNORE 1 LINES
    (hip,tycho2_id,solution_id,source_id,random_index,ref_epoch,ra,ra_error,declination,dec_error,parallax,parallax_error,pmra,pmra_error,pmdec,pmdec_error,ra_dec_corr,ra_parallax_corr,ra_pmra_corr,ra_pmdec_corr,dec_parallax_corr,dec_pmra_corr,dec_pmdec_corr,parallax_pmra_corr,parallax_pmdec_corr,pmra_pmdec_corr,astrometric_n_obs_al,astrometric_n_obs_ac,astrometric_n_good_obs_al,astrometric_n_good_obs_ac,astrometric_n_bad_obs_al,astrometric_n_bad_obs_ac,astrometric_delta_q,astrometric_excess_noise,astrometric_excess_noise_sig,astrometric_primary_flag,astrometric_relegation_factor,astrometric_weight_al,astrometric_weight_ac,astrometric_priors_used,matched_observations,duplicated_source,scan_direction_strength_k1,scan_direction_strength_k2,scan_direction_strength_k3,scan_direction_strength_k4,scan_direction_mean_k1,scan_direction_mean_k2,scan_direction_mean_k3,scan_direction_mean_k4,phot_g_n_obs,phot_g_mean_flux,phot_g_mean_flux_error,phot_g_mean_mag,phot_variable_flag,l,b,ecl_lon,ecl_lat);


load data local infile '/Users/marcolam/Documents/tgas_source/tgas_source/TgasSource_000-000-009.csv' into table tgas fields terminated by ','
  enclosed by '"'
  lines terminated by '\n'
IGNORE 1 LINES
    (hip,tycho2_id,solution_id,source_id,random_index,ref_epoch,ra,ra_error,declination,dec_error,parallax,parallax_error,pmra,pmra_error,pmdec,pmdec_error,ra_dec_corr,ra_parallax_corr,ra_pmra_corr,ra_pmdec_corr,dec_parallax_corr,dec_pmra_corr,dec_pmdec_corr,parallax_pmra_corr,parallax_pmdec_corr,pmra_pmdec_corr,astrometric_n_obs_al,astrometric_n_obs_ac,astrometric_n_good_obs_al,astrometric_n_good_obs_ac,astrometric_n_bad_obs_al,astrometric_n_bad_obs_ac,astrometric_delta_q,astrometric_excess_noise,astrometric_excess_noise_sig,astrometric_primary_flag,astrometric_relegation_factor,astrometric_weight_al,astrometric_weight_ac,astrometric_priors_used,matched_observations,duplicated_source,scan_direction_strength_k1,scan_direction_strength_k2,scan_direction_strength_k3,scan_direction_strength_k4,scan_direction_mean_k1,scan_direction_mean_k2,scan_direction_mean_k3,scan_direction_mean_k4,phot_g_n_obs,phot_g_mean_flux,phot_g_mean_flux_error,phot_g_mean_mag,phot_variable_flag,l,b,ecl_lon,ecl_lat);


load data local infile '/Users/marcolam/Documents/tgas_source/tgas_source/TgasSource_000-000-010.csv' into table tgas fields terminated by ','
  enclosed by '"'
  lines terminated by '\n'
IGNORE 1 LINES
    (hip,tycho2_id,solution_id,source_id,random_index,ref_epoch,ra,ra_error,declination,dec_error,parallax,parallax_error,pmra,pmra_error,pmdec,pmdec_error,ra_dec_corr,ra_parallax_corr,ra_pmra_corr,ra_pmdec_corr,dec_parallax_corr,dec_pmra_corr,dec_pmdec_corr,parallax_pmra_corr,parallax_pmdec_corr,pmra_pmdec_corr,astrometric_n_obs_al,astrometric_n_obs_ac,astrometric_n_good_obs_al,astrometric_n_good_obs_ac,astrometric_n_bad_obs_al,astrometric_n_bad_obs_ac,astrometric_delta_q,astrometric_excess_noise,astrometric_excess_noise_sig,astrometric_primary_flag,astrometric_relegation_factor,astrometric_weight_al,astrometric_weight_ac,astrometric_priors_used,matched_observations,duplicated_source,scan_direction_strength_k1,scan_direction_strength_k2,scan_direction_strength_k3,scan_direction_strength_k4,scan_direction_mean_k1,scan_direction_mean_k2,scan_direction_mean_k3,scan_direction_mean_k4,phot_g_n_obs,phot_g_mean_flux,phot_g_mean_flux_error,phot_g_mean_mag,phot_variable_flag,l,b,ecl_lon,ecl_lat);


load data local infile '/Users/marcolam/Documents/tgas_source/tgas_source/TgasSource_000-000-011.csv' into table tgas fields terminated by ','
  enclosed by '"'
  lines terminated by '\n'
IGNORE 1 LINES
    (hip,tycho2_id,solution_id,source_id,random_index,ref_epoch,ra,ra_error,declination,dec_error,parallax,parallax_error,pmra,pmra_error,pmdec,pmdec_error,ra_dec_corr,ra_parallax_corr,ra_pmra_corr,ra_pmdec_corr,dec_parallax_corr,dec_pmra_corr,dec_pmdec_corr,parallax_pmra_corr,parallax_pmdec_corr,pmra_pmdec_corr,astrometric_n_obs_al,astrometric_n_obs_ac,astrometric_n_good_obs_al,astrometric_n_good_obs_ac,astrometric_n_bad_obs_al,astrometric_n_bad_obs_ac,astrometric_delta_q,astrometric_excess_noise,astrometric_excess_noise_sig,astrometric_primary_flag,astrometric_relegation_factor,astrometric_weight_al,astrometric_weight_ac,astrometric_priors_used,matched_observations,duplicated_source,scan_direction_strength_k1,scan_direction_strength_k2,scan_direction_strength_k3,scan_direction_strength_k4,scan_direction_mean_k1,scan_direction_mean_k2,scan_direction_mean_k3,scan_direction_mean_k4,phot_g_n_obs,phot_g_mean_flux,phot_g_mean_flux_error,phot_g_mean_mag,phot_variable_flag,l,b,ecl_lon,ecl_lat);


load data local infile '/Users/marcolam/Documents/tgas_source/tgas_source/TgasSource_000-000-012.csv' into table tgas fields terminated by ','
  enclosed by '"'
  lines terminated by '\n'
IGNORE 1 LINES
    (hip,tycho2_id,solution_id,source_id,random_index,ref_epoch,ra,ra_error,declination,dec_error,parallax,parallax_error,pmra,pmra_error,pmdec,pmdec_error,ra_dec_corr,ra_parallax_corr,ra_pmra_corr,ra_pmdec_corr,dec_parallax_corr,dec_pmra_corr,dec_pmdec_corr,parallax_pmra_corr,parallax_pmdec_corr,pmra_pmdec_corr,astrometric_n_obs_al,astrometric_n_obs_ac,astrometric_n_good_obs_al,astrometric_n_good_obs_ac,astrometric_n_bad_obs_al,astrometric_n_bad_obs_ac,astrometric_delta_q,astrometric_excess_noise,astrometric_excess_noise_sig,astrometric_primary_flag,astrometric_relegation_factor,astrometric_weight_al,astrometric_weight_ac,astrometric_priors_used,matched_observations,duplicated_source,scan_direction_strength_k1,scan_direction_strength_k2,scan_direction_strength_k3,scan_direction_strength_k4,scan_direction_mean_k1,scan_direction_mean_k2,scan_direction_mean_k3,scan_direction_mean_k4,phot_g_n_obs,phot_g_mean_flux,phot_g_mean_flux_error,phot_g_mean_mag,phot_variable_flag,l,b,ecl_lon,ecl_lat);


load data local infile '/Users/marcolam/Documents/tgas_source/tgas_source/TgasSource_000-000-013.csv' into table tgas fields terminated by ','
  enclosed by '"'
  lines terminated by '\n'
IGNORE 1 LINES
    (hip,tycho2_id,solution_id,source_id,random_index,ref_epoch,ra,ra_error,declination,dec_error,parallax,parallax_error,pmra,pmra_error,pmdec,pmdec_error,ra_dec_corr,ra_parallax_corr,ra_pmra_corr,ra_pmdec_corr,dec_parallax_corr,dec_pmra_corr,dec_pmdec_corr,parallax_pmra_corr,parallax_pmdec_corr,pmra_pmdec_corr,astrometric_n_obs_al,astrometric_n_obs_ac,astrometric_n_good_obs_al,astrometric_n_good_obs_ac,astrometric_n_bad_obs_al,astrometric_n_bad_obs_ac,astrometric_delta_q,astrometric_excess_noise,astrometric_excess_noise_sig,astrometric_primary_flag,astrometric_relegation_factor,astrometric_weight_al,astrometric_weight_ac,astrometric_priors_used,matched_observations,duplicated_source,scan_direction_strength_k1,scan_direction_strength_k2,scan_direction_strength_k3,scan_direction_strength_k4,scan_direction_mean_k1,scan_direction_mean_k2,scan_direction_mean_k3,scan_direction_mean_k4,phot_g_n_obs,phot_g_mean_flux,phot_g_mean_flux_error,phot_g_mean_mag,phot_variable_flag,l,b,ecl_lon,ecl_lat);


load data local infile '/Users/marcolam/Documents/tgas_source/tgas_source/TgasSource_000-000-014.csv' into table tgas fields terminated by ','
  enclosed by '"'
  lines terminated by '\n'
IGNORE 1 LINES
    (hip,tycho2_id,solution_id,source_id,random_index,ref_epoch,ra,ra_error,declination,dec_error,parallax,parallax_error,pmra,pmra_error,pmdec,pmdec_error,ra_dec_corr,ra_parallax_corr,ra_pmra_corr,ra_pmdec_corr,dec_parallax_corr,dec_pmra_corr,dec_pmdec_corr,parallax_pmra_corr,parallax_pmdec_corr,pmra_pmdec_corr,astrometric_n_obs_al,astrometric_n_obs_ac,astrometric_n_good_obs_al,astrometric_n_good_obs_ac,astrometric_n_bad_obs_al,astrometric_n_bad_obs_ac,astrometric_delta_q,astrometric_excess_noise,astrometric_excess_noise_sig,astrometric_primary_flag,astrometric_relegation_factor,astrometric_weight_al,astrometric_weight_ac,astrometric_priors_used,matched_observations,duplicated_source,scan_direction_strength_k1,scan_direction_strength_k2,scan_direction_strength_k3,scan_direction_strength_k4,scan_direction_mean_k1,scan_direction_mean_k2,scan_direction_mean_k3,scan_direction_mean_k4,phot_g_n_obs,phot_g_mean_flux,phot_g_mean_flux_error,phot_g_mean_mag,phot_variable_flag,l,b,ecl_lon,ecl_lat);


load data local infile '/Users/marcolam/Documents/tgas_source/tgas_source/TgasSource_000-000-015.csv' into table tgas fields terminated by ','
  enclosed by '"'
  lines terminated by '\n'
IGNORE 1 LINES
    (hip,tycho2_id,solution_id,source_id,random_index,ref_epoch,ra,ra_error,declination,dec_error,parallax,parallax_error,pmra,pmra_error,pmdec,pmdec_error,ra_dec_corr,ra_parallax_corr,ra_pmra_corr,ra_pmdec_corr,dec_parallax_corr,dec_pmra_corr,dec_pmdec_corr,parallax_pmra_corr,parallax_pmdec_corr,pmra_pmdec_corr,astrometric_n_obs_al,astrometric_n_obs_ac,astrometric_n_good_obs_al,astrometric_n_good_obs_ac,astrometric_n_bad_obs_al,astrometric_n_bad_obs_ac,astrometric_delta_q,astrometric_excess_noise,astrometric_excess_noise_sig,astrometric_primary_flag,astrometric_relegation_factor,astrometric_weight_al,astrometric_weight_ac,astrometric_priors_used,matched_observations,duplicated_source,scan_direction_strength_k1,scan_direction_strength_k2,scan_direction_strength_k3,scan_direction_strength_k4,scan_direction_mean_k1,scan_direction_mean_k2,scan_direction_mean_k3,scan_direction_mean_k4,phot_g_n_obs,phot_g_mean_flux,phot_g_mean_flux_error,phot_g_mean_mag,phot_variable_flag,l,b,ecl_lon,ecl_lat);






CREATE TABLE astrogrid (
  astro GEOMETRY NOT NULL,
  SPATIAL KEY astro (astro) )
ENGINE=MYISAM;


INSERT INTO astrogrid
SELECT ST_GEOMFROMTEXT( CONCAT('POINT(', declination, ' ', ra, ')') ) AS astro from tgas;


CREATE FUNCTION vincenty (lat1 DOUBLE, long1 DOUBLE, lat2 DOUBLE, long2 DOUBLE) RETURNS FLOAT
  RETURN DEGREES(
    ATAN2(
      SQRT(
         POW(COS(RADIANS(lat1))*SIN(RADIANS(IF (long1 % 360 - long2 % 360 > 180, 360 - long1 % 360 - long2 % 360, long1 % 360 - long2 % 360))), 2) +
           POW(COS(RADIANS(lat2))*SIN(RADIANS(lat1)) -
           (SIN(RADIANS(lat2))*COS(RADIANS(lat1)) *
            COS(RADIANS(IF (long1 % 360 - long2 % 360 > 180, 360 - long1 % 360 - long2 % 360, long1 % 360 - long2 % 360)))), 2)),
      SIN(RADIANS(lat2))*SIN(RADIANS(lat1)) +
        COS(RADIANS(lat2))*
        COS(RADIANS(lat1))*
        COS(RADIANS(IF (long1 % 360 - long2 % 360 > 180, 360 - long1 % 360 - long2 % 360, long1 % 360 - long2 % 360)))
    )
  );

