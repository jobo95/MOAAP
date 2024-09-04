import glob
from dataclasses import dataclass
from typing import Tuple


@dataclass
class ICONExperiment:
    scratch_path: str = "/work/aa0238/a271093/scratch/"
    slp_aac_name: str = "slp_daymean_1984-2015_remapped_3x_aac.nc"
    reginal_30km_target_grid: str = "/work/aa0238/a271093/data/regridding_files/ICON_rotated_grid_33x33km.nc"
    clustering_target_grid: str = "/work/aa0238/a271093/data/regridding_files/NH_-90_90_20_88_reglonlat_1degree.nc"
    IVT_thresh_path = "/work/aa0238/a271093/data/input/IVT_thresholds/"

    slp_nc: str = "PMSL"
    lat_nc: str = "lat"
    lon_nc: str = "lon"
    time_nc: str = "time"
    BMU_path: str = "/work/aa0238/a271093/data/clustering/regime_output/BMU/"
    container_pkl_file: str = "Object_container"


@dataclass
class SSP_EXPERIMENT:
    year_start: int = 2014
    year_end: int = 2100


@dataclass
class CONTROL_EXPERIMENT:
    year_start: int = 1984
    year_end: int = 2014


@dataclass
class CNRM_EXPERIMENT:

    control_aac_file_del29feb: str = "/work/aa0238/a271093/data/clustering/CNRM_control/CNRM_ICON_control_gph70000_1984_2014_reglonlat_-90_90_20_88_1deg_"
    control_aac_file: str = "/work/aa0238/a271093/data/clustering/CNRM_control/CNRM_ICON_control_gph70000_1984_2014_reglonlat_-90_90_20_88_1deg_"


@dataclass
class NorESM_EXPERIMENT:

    control_aac_file_del29feb: str = "/work/aa0238/a271093/data/clustering/NorESM_control/NORESM_ICON_control_gph70000_1984_2014_reglonlat_-90_90_20_88_1deg_"
    control_aac_file: str = "/work/aa0238/a271093/data/clustering/NorESM_control/NORESM_ICON_control_gph70000_1984_2014_reglonlat_-90_90_20_88_1deg_"


@dataclass
class ICON_NorESM_CONTROL(ICONExperiment, CONTROL_EXPERIMENT, NorESM_EXPERIMENT):
    exp_name: str = "NORESM_ICON_control"

    path: str = "/work/aa0238/a271093/data/Jan_runs/ICON_NorESM_control/NorESM_control_remapped_3x/"
    slp_path: str = f"{path}slp/"

    path_raw: str = "/work/aa0049/a271109/spice-v2.2/chain/work/polarres_wp3_cmip_NorESM/post/yearly/"
    slp_path_raw: str = f"{path_raw}PMSL/"
    FI850p_path_raw: str = f"{path_raw}FI850p/"

    path_raw_gcm: str = "/pool/data/CMIP6/data/CMIP/NCC/NorESM2-MM/historical/r1i1p1f1/day/"
    slp_path_raw_gcm: str = f"{path_raw_gcm}psl/gn/v20191108/"
    slp_files_raw_gcm: str = (
        f"{slp_path_raw_gcm}psl_day_NorESM2-MM_historical_r1i1p1f1_gn_19800101-19891231.nc",
        f"{slp_path_raw_gcm}psl_day_NorESM2-MM_historical_r1i1p1f1_gn_19900101-19991231.nc",
        f"{slp_path_raw_gcm}psl_day_NorESM2-MM_historical_r1i1p1f1_gn_20000101-20091231.nc" f"{slp_path_raw_gcm}psl_day_NorESM2-MM_historical_r1i1p1f1_gn_20100101-20141231.nc",
    )

    gph_path_raw_gcm: str = f"{path_raw_gcm}zg/gn/v20191108/"
    gph_files_raw_gcm: Tuple[str] = (
        f"{gph_path_raw_gcm}zg_day_NorESM2-MM_historical_r1i1p1f1_gn_19800101-19891231.nc",
        f"{gph_path_raw_gcm}zg_day_NorESM2-MM_historical_r1i1p1f1_gn_19900101-19991231.nc",
        f"{gph_path_raw_gcm}zg_day_NorESM2-MM_historical_r1i1p1f1_gn_20000101-20091231.nc",
        f"{gph_path_raw_gcm}zg_day_NorESM2-MM_historical_r1i1p1f1_gn_20100101-20141231.nc",
    )

    IVT_thresh_file_85: str = "IVT_85_percentiles_NorESM_control_3dx3dy.nc"
    IVTobj_out_path: str = "/work/aa0238/a271093/results/MOAAP/IVT_Tracking/NorESM_control_remapped_3x/"
    clustering_data_path: str = "/work/aa0238/a271093/data/clustering/NorESM_control/"

    BMU_file: str = "NORESM_ICON_control_gph70000_1984_2014_reglonlat_-90_90_20_88_1deg_DJF_fldmean_detrend_del29feb_aac_20PCs_4clusters_Ref_ERA5KmeansPCA.csv"


@dataclass
class ICON_CNRM_CONTROL(ICONExperiment, CONTROL_EXPERIMENT, CNRM_EXPERIMENT):
    exp_name: str = "CNRM_ICON_control"
    path: str = "/work/aa0238/a271093/data/Jan_runs/ICON_CNRM_control/CNRM_control_remapped_3x/"
    path_IVT_tracking: str = "/work/aa0238/a271093/results/MOAAP/IVT_Tracking/CNRM_control_remapped_3x/"
    slp_path: str = f"{path}slp/"

    path_raw: str = "/work/aa0049/a271109/spice-v2.1/chain/work/polarres_wp3_cmip_CNRM/post/yearly/"

    slp_path_raw: str = f"{path_raw}PMSL/"
    FI250p_path_raw: str = f"{path_raw}FI250p/"
    FI500p_path_raw: str = f"{path_raw}FI500p/"
    FI700p_path_raw: str = f"{path_raw}FI700p/"
    FI850p_path_raw: str = f"{path_raw}FI850p/"

    path_raw_gcm: str = "/pool/data/CMIP6/data/CMIP/CNRM-CERFACS/CNRM-ESM2-1/historical/r1i1p1f2/day/"
    slp_files_raw_gcm: str = f"{path_raw_gcm}psl/gr/v20181206/psl_day_CNRM-ESM2-1_historical_r1i1p1f2_gr_18500101-20141231.nc"

    gph_path_raw_gcm: str = f"{path_raw_gcm}zg/gr/v20181206/"
    gph_files_raw_gcm: Tuple[str, str] = (
        f"{gph_path_raw_gcm}zg_day_CNRM-ESM2-1_historical_r1i1p1f2_gr_19750101-19991231.nc",
        f"{gph_path_raw_gcm}/zg_day_CNRM-ESM2-1_historical_r1i1p1f2_gr_20000101-20141231.nc",
    )
    IVT_thresh_file_85: str = "IVT_85_percentiles_CNMR_control_3dx3dy.nc"
    IVTobj_out_path: str = "/work/aa0238/a271093/results/MOAAP/IVT_Tracking/CNRM_control_remapped_3x/"
    clustering_data_path: str = "/work/aa0238/a271093/data/clustering/CNRM_control/"

    BMU_file: str = "CNRM_ICON_control_gph70000_1984_2014_reglonlat_-90_90_20_88_1deg_DJF_fldmean_detrend_del29feb_aac_20PCs_4clusters_Ref_ERA5KmeansPCA.csv"


@dataclass
class ICON_NorESM_SSP(ICONExperiment, NorESM_EXPERIMENT, SSP_EXPERIMENT):
    exp_name: str = "NorESM_ICON_SSP"

    path_IVT: str = "/work/aa0238/a271093/data/Jan_runs/ICON_NorESM_ssp/NorESM_ssp_remapped_3x/"
    path_raw: str = "/work/aa0049/a271109/spice-v2.2/chain/work/polarres_wp3_cmip_NorESM_ssp370/post/yearly/"
    path_raw_gcm: str = "/pool/data/CMIP6/data/ScenarioMIP/NCC/NorESM2-MM/ssp370/r1i1p1f1/day/"
    gph_path_raw_gcm: str = f"{path_raw_gcm}zg/gn/v20191108/"
    gph_files_raw_gcm: Tuple[str] = tuple(sorted(glob.glob(gph_path_raw_gcm + "*")))
    clustering_data_path: str = "/work/aa0238/a271093/data/clustering/NorESM_ssp/"
    IVTobj_out_path: str = "/work/aa0238/a271093/results/MOAAP/IVT_Tracking/NorESM_ssp_remapped_3x/"
    IVT_thresh_file_85: str = "IVT_85_percentiles_CNMR_ssp_3dx3dy.nc"

    BMU_file: str = "NorESM_ICON_SSP_gph70000_2015_2100_reglonlat_-90_90_20_88_1deg_DJF_fldmean_detrend_del29feb_aac_20PCs_4clusters_Ref_ERA5KmeansPCA.csv"


class ICON_CNRM_SSP(ICONExperiment, CNRM_EXPERIMENT, SSP_EXPERIMENT):
    exp_name: str = "CNRM_ICON_SSP"

    path_IVT: str = "/work/aa0238/a271093/data/Jan_runs/ICON_CNRM_ssp/CNRM_ssp_remapped_3x/"
    path_raw: str = "/work/aa0049/a271109/spice-v2.2/chain/work/polarres_wp3_cmip_CNRM_ssp370/post/yearly/"
    path_raw_gcm: str = "/pool/data/CMIP6/data/ScenarioMIP/CNRM-CERFACS/CNRM-ESM2-1/ssp370/r1i1p1f2/day/"
    gph_path_raw_gcm: str = f"{path_raw_gcm}zg/gr/v20190328/"

    gph_files_raw_gcm: Tuple[str] = tuple(sorted(glob.glob(gph_path_raw_gcm + "*")))
    clustering_data_path: str = "/work/aa0238/a271093/data/clustering/CNRM_ssp/"

    IVTobj_out_path: str = "/work/aa0238/a271093/results/MOAAP/IVT_Tracking/CNRM_ssp_remapped_3x/"
    IVT_thresh_file_85: str = "IVT_85_percentiles_CNMR_ssp_3dx3dy.nc"

    BMU_file: str = "CNRM_ICON_SSP_gph70000_2015_2100_reglonlat_-90_90_20_88_1deg_DJF_fldmean_detrend_del29feb_aac_20PCs_4clusters_Ref_ERA5KmeansPCA.csv"


@dataclass
class ERA5(ICONExperiment):
    exp_name: str = "ERA5"
    path_IVT_tracking: str = "/work/aa0238/a271093/results/MOAAP/IVT_Tracking/ERA5_ICON_remapped_3x/"
    year_start: int = 1984
    year_end: int = 2014
    # year_start: int = 1979
    # year_end: int = 2022
    path_IVT: str = "/work/aa0238/a271093/data/ERA5/1979-2023/ICON_remapped_3x/"
    slp_path: str = "/work/aa0238/a271093/data/ERA5/1984-2014/remapped_ICON_reg_30km/slp/"
    slp_path_raw: str = "/work/bm1159/XCES/data4xces/reanalysis/reanalysis/ECMWF/IFS/ERA5/1hr/atmos/psl/r1i1p1/"
    slp_nc: str = "psl"

    gph_path_raw_gcm: str = "/work/bm1159/XCES/data4xces/reanalysis/reanalysis/ECMWF/IFS/ERA5/day/atmos/zg/r1i1p1-070000Pa/"
    gph_files_raw_gcm: Tuple[str] = tuple(sorted(glob.glob(gph_path_raw_gcm + "*")))
    clustering_data_path: str = "/work/aa0238/a271093/data/clustering/ERA5/"

    control_aac_file_del29feb: str = "/work/aa0238/a271093/data/clustering/ERA5/ERA5_gph70000_1984_2014_reglonlat_-90_90_20_88_1deg_"
    control_aac_file: str = "/work/aa0238/a271093/data/clustering/ERA5/ERA5_gph70000_1984_2014_reglonlat_-90_90_20_88_1deg_"

    BMU_file_DJF: str = "ERA5_gph70000_1984_2014_reglonlat_-90_90_20_88_1deg_DJF_fldmean_detrend_del29feb_aac_20PCs_5clusters_Ref_ERA5KmeansPCA.csv"
    BMU_file_MAM: str = "ERA5_gph70000_1984_2014_reglonlat_-90_90_20_88_1deg_MAM_fldmean_detrend_del29feb_aac_20PCs_5clusters_Ref_ERA5KmeansPCA.csv"


@dataclass
class ICON_ERA5(ICONExperiment):
    exp_name: str = "ICON-ERA5"
    year_start: int = 1998
    year_end: int = 2023
    slp_path: str = "/work/aa0238/a271093/data/ICON_ERA5/slp/"
    slp_path_raw: str = "/work/aa0049/a271041/spice-v2.1/chain/work/run_era5_polarres_wp3_hindcast2/post/yearly/PMSL/"
    path_IVT: str = "/work/aa0238/a271093/data/ICON_ERA5/1998-2022/remapped_3x/"
    path_IVT_tracking: str = "/work/aa0238/a271093/results/MOAAP/IVT_Tracking/ICON_DRIVENBY_ERA5_remapped_3x/"
    BMU_file_DJF: str = "ERA5_gph70000_1984_2014_reglonlat_-90_90_20_88_1deg_DJF_fldmean_detrend_del29feb_aac_20PCs_5clusters_Ref_ERA5KmeansPCA.csv"
    BMU_file_MAM: str = "ERA5_gph70000_1984_2014_reglonlat_-90_90_20_88_1deg_MAM_fldmean_detrend_del29feb_aac_20PCs_5clusters_Ref_ERA5KmeansPCA.csv"
    IVT_thresh_file_85: str = "ivt_percentile_mlauer_removed-ens-lev_remapbilWP3domain_3dx3dy.nc"


@dataclass
class ICON_NWP_refined(ICONExperiment):
    year_start: int = 1985
    year_end: int = 2014
    exp_name: str = "ICON-NWP-Refined"
    path_IVT: str = "/work/aa0238/a271093/data/Raphael_runs/ICON_NWP_refined/ICON_NWP_refined_remapped_3x/"
    path_IVT_tracking: str = "/work/aa0238/a271093/results/MOAAP/IVT_Tracking/ICON_NWP_refined_remapped_3x/"

    IVT_thresh_file_85: str = "ivt_percentile_mlauer_removed-ens-lev_remapbilWP3domain_3dx3dy.nc"


@dataclass
class Data:
    # ICONEXP = ICONExperiment
    # ICON_ERA5_EXP = ICON_ERA5
    ICON_NORESM_CONTROL = ICON_NorESM_CONTROL
    ICON_CNRM_CONTROL = ICON_CNRM_CONTROL
    ICON_CNRM_SSP = ICON_CNRM_SSP
    ICON_NORESM_SSP = ICON_NorESM_SSP  # ICON_CNRM_EXP = ICON_CNRM_CONTROL
    ERA5 = ERA5
    ICON_ERA5 = ICON_ERA5
