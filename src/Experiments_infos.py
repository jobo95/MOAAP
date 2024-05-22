from dataclasses import dataclass
from typing import Tuple


@dataclass
class ICONExperiment:
    scratch_path: str = "/work/aa0238/a271093/scratch/"
    slp_aac_name: str = "slp_daymean_1984-2015_remapped_3x_aac.nc"
    clustering_target_grid: str = (
        "/work/aa0238/a271093/data/regridding_files/ICON_rotated_grid_33x33km.nc"
    )
    IVT_thresh_path = "/work/aa0238/a271093/data/input/"

    slp_nc: str = "PMSL"
    lat_nc: str = "lat"
    lon_nc: str = "lon"
    time_nc: str = "time"


@dataclass
class ICON_ERA5(ICONExperiment):
    exp_name: str = "regional ICON forced by ERA5"
    slp_path: str = "/work/aa0238/a271093/data/ICON_ERA5/slp/"
    slp_path_raw: str = (
        "/work/aa0049/a271041/spice-v2.1/chain/work/run_era5_polarres_wp3_hindcast2/post/yearly/PMSL/"
    )


@dataclass
class ICON_NorESM_CONTROL(ICONExperiment):
    exp_name: str = "regional ICON forced by NorESM"
    

    path: str = (
        "/work/aa0238/a271093/data/Jan_runs/ICON_NorESM_control/NorESM_control_remapped_3x/"
    )
    slp_path: str = f"{path}slp/"
    
    path_raw: str = (
        "/work/aa0049/a271109/spice-v2.2/chain/work/polarres_wp3_cmip_NorESM/post/yearly/"
    )
    slp_path_raw: str = f"{path_raw}PMSL/"
    FI850p_path_raw: str = f"{path_raw}FI850p/"
    

    path_raw_gcm: str = (
        "/pool/data/CMIP6/data/CMIP/NCC/NorESM2-MM/historical/r1i1p1f1/day/"
    )
    slp_path_raw_gcm: str = f"{path_raw_gcm}psl/gn/v20191108/"
    slp_files_raw_gcm: str = (
        f"{slp_path_raw_gcm}psl_day_NorESM2-MM_historical_r1i1p1f1_gn_19800101-19891231.nc",
        f"{slp_path_raw_gcm}psl_day_NorESM2-MM_historical_r1i1p1f1_gn_19900101-19991231.nc",
        f"{slp_path_raw_gcm}psl_day_NorESM2-MM_historical_r1i1p1f1_gn_20000101-20091231.nc"
        f"{slp_path_raw_gcm}psl_day_NorESM2-MM_historical_r1i1p1f1_gn_20100101-20141231.nc"
    )


    gph_path_raw_gcm: str =f"{path_raw_gcm}zg/gn/v20191108/" 
    gph_files_raw_gcm: Tuple[str] = (
        f"{gph_path_raw_gcm}zg_day_NorESM2-MM_historical_r1i1p1f1_gn_19800101-19891231.nc",
        f"{gph_path_raw_gcm}zg_day_NorESM2-MM_historical_r1i1p1f1_gn_19900101-19991231.nc",
        f"{gph_path_raw_gcm}zg_day_NorESM2-MM_historical_r1i1p1f1_gn_20000101-20091231.nc",
        f"{gph_path_raw_gcm}zg_day_NorESM2-MM_historical_r1i1p1f1_gn_20100101-20141231.nc",
    )

    IVT_thresh_file_85: str = "IVT_85_percentiles_NorESM_control_3dx3dy.nc"
    IVTobj_out_path: str = (
        "/work/aa0238/a271093/results/MOAAP/IVT_Tracking/NorESM_control_remapped_3x/"
    )


@dataclass
class ICON_CNRM_CONTROL(ICONExperiment):
    exp_name: str = "regional ICON forced by CNRM"
    path: str =  "/work/aa0238/a271093/data/Jan_runs/ICON_CNRM_control/CNRM_control_remapped_3x/"
    
    
    slp_path: str = f"{path}slp/"
    
    path_raw :str= "/work/aa0049/a271109/spice-v2.1/chain/work/polarres_wp3_cmip_CNRM/post/yearly/"
    
    slp_path_raw: str = f"{path_raw}PMSL/"
    FI700p_path_raw: str = f"{path_raw}FI700p/"
    FI850p_path_raw: str = f"{path_raw}FI8500p/"
    
    path_raw_gcm: str = (
        "/pool/data/CMIP6/data/CMIP/CNRM-CERFACS/CNRM-ESM2-1/historical/r1i1p1f2/day/"
    )
    slp_file_gcm_raw: str = (
        f"{path_raw_gcm}psl/gr/v20181206/psl_day_CNRM-ESM2-1_historical_r1i1p1f2_gr_18500101-20141231.nc"
    )
    
    gph_path_raw_gcm: str =f"{path_raw_gcm}zg/gr/v20181206/"
    gph_files_raw_gcm: Tuple[str, str] = (
        f"{gph_path_raw_gcm}zg_day_CNRM-ESM2-1_historical_r1i1p1f2_gr_19750101-19991231.nc",
        f"{gph_path_raw_gcm}/zg_day_CNRM-ESM2-1_historical_r1i1p1f2_gr_20000101-20141231.nc",
    )
    IVT_thresh_file_85: str = "IVT_85_percentiles_CNMR_control_3dx3dy.nc"
    IVTobj_out_path: str = (
        "/work/aa0238/a271093/results/MOAAP/IVT_Tracking/CNRM_control_remapped_3x/"
    )


@dataclass
class ERA5(ICONExperiment):
    slp_path: str = (
        "/work/aa0238/a271093/data/ERA5/1984-2014/remapped_ICON_reg_30km/slp/"
    )
    slp_path_raw: str = (
        "/work/bm1159/XCES/data4xces/reanalysis/reanalysis/ECMWF/IFS/ERA5/1hr/atmos/psl/r1i1p1/"
    )
    slp_nc: str = "psl"


@dataclass
class Data:
    ICONEXP = ICONExperiment
    ICON_ERA5_EXP = ICON_ERA5
    ICON_NORESM_EXP = ICON_NorESM_CONTROL
    ICON_CNRM_EXP = ICON_CNRM_CONTROL
    ERA5 = ERA5
