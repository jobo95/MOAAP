#%load_ext autoreload
#%autoreload 2
import xarray as xr
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy
import datetime
import cartopy
import cartopy.crs as ccrs
import pickle
#import Tracking_Functions
from dateutil import relativedelta
import os

import src.Tracking_Functions as Tracking_Functions
from src.TrackingDataLoader import load_tracking_data, get_datetime_array_from_ds 
from src.utils import * 
from src.Corrections import * 
from src.Enumerations import Experiments


#data_path = '/work/aa0049/a271109/spice-v2.1/chain/work/polarres_wp3_cmip_CNRM/post/yearly/'
#exp = Data.ICON_NORESM_EXP.value


suffix = 'remapped_3x'
file_type = '.nc'

#######ICON########

#exp = Experiments.ICON_NORESM_CONTROL.value

#first_year = 1984
#last_year = 1985

#data_path = exp.path
#output_path = exp.IVTobj_out_path
#output_path = "/work/aa0238/a271093/scratch/test/"

#output_file_name_temp = f'MOAPP_ICON_100and85controlperc_{suffix}'

#output_path = '/work/aa0238/a271093/scratch/Track_test/'
#threshold_file = exp.IVT_thresh_path+exp.IVT_thresh_file_85

#ds_ivt_pctl=xr.open_dataset(threshold_file,decode_times=False)
#IVTtrheshold=ds_ivt_pctl.IVT_85perc.values



#####ERA5######
exp = Experiments.ERA5.value

first_year = 1979
last_year = 2024


data_path = exp.path_IVT
#output_path = exp.IVTobj_out_path
output_path = "/work/aa0238/a271093/results/MOAAP/IVT_Tracking/ERA5_ICON_ARlat0_remapped_3x/"
output_file_name_temp = f'MOAPP_ERA5_100and85controlperc_{suffix}'
#threshold_file = exp.threshold_path+'ivt_percentile_mlauer_removed-ens-lev_remapbilWP3domain_3dx3dy.nc'
threshold_file = exp.IVT_thresh_path+exp.IVT_thresh_file_85

ds_ivt_pctl=xr.open_dataset(threshold_file,decode_times=False)
IVTtrheshold=ds_ivt_pctl.ivt1.values

#######ICON SSP/NWP###########
#exp = Experiments.ICON_NWP_REFINED.value
#output_file_name_temp = f'MOAPP_ICON_100and85ERA5perc_{suffix}'


#first_year = exp.year_start
#last_year = exp.year_end

#data_path = exp.path_IVT
#output_path = exp.IVTobj_out_path
#output_path = "/work/aa0238/a271093/scratch/test/"
#output_path = "/work/aa0238/a271093/scratch/test/"
#first_year = 2013


#threshold_file = exp.IVT_thresh_path+exp.IVT_thresh_file_85

#ds_ivt_pctl=xr.open_dataset(threshold_file,decode_times=False)
#IVTtrheshold=ds_ivt_pctl.IVT_85_perc.values
#IVTtrheshold=ds_ivt_pctl.ivt1.values



###### ICON-ERA5###########
#exp = Experiments.ICON_ERA5.value

#first_year = exp.year_start
#last_year = exp.year_end

#data_path = exp.path_IVT
#output_path = exp.IVTobj_out_path
#output_path = "/work/aa0238/a271093/scratch/test/"

#output_file_name_temp = f'MOAPP_ICON_ERA5_100and85ERA5perc_{suffix}'

#threshold_file = exp.IVT_thresh_path+exp.IVT_thresh_file_85

#ds_ivt_pctl=xr.open_dataset(threshold_file,decode_times=False)
#IVTtrheshold=ds_ivt_pctl.ivt1.values


#########ICON NWP





start_date_list, end_date_list = create_datetime_lists(first_year,last_year) 
first_processed_date = start_date_list[0]
last_processed_date = end_date_list[-1]


dict_keys_offset = 0

dict_keys_offset = 0

for start_date, end_date in zip(start_date_list, end_date_list):
    
    print ("\n \n \n \n")
    print (start_date, end_date)


    IVTudata = load_tracking_data(var_path=data_path,
                       var_name="IVTu",
                      start_date = start_date,
                      end_date = end_date)

    IVTvdata = load_tracking_data(var_path=data_path,
                       var_name="IVTv",
                      start_date = start_date,
                      end_date = end_date)
    

    

    rLon = xr.broadcast(IVTudata.rlon, IVTudata.rlat)[0].values.T
    rLat = xr.broadcast(IVTudata.rlon, IVTudata.rlat)[1].values.T

    Lon = xr.broadcast(IVTudata.lon, IVTudata.lat)[0].values
    Lat = xr.broadcast(IVTudata.lon, IVTudata.lat)[1].values

    Mask=1*(rLat>-999)
    Time_sel = get_datetime_array_from_ds(IVTudata)
    
    output_file_name = f'{output_file_name_temp}_{get_datetime_str(start_date)}-{get_datetime_str(end_date)}'

    

    Tracking_Functions.moaap(Lon = rLon,                            # 2Dlongitude grid centers
                              Lat = rLat,                           # 2D latitude grid spacing
                              Time = Time_sel,                      # datetime vector of data
                              dT = 1,                               # integer - temporal frequency of data [hour]
                              Mask = Mask,                          # mask with dimensions [lat,lon] defining analysis region

                              ivte = IVTudata.IVTu.values,          # zonal integrated vapor transport [kg m-1 s-1]
                              ivtn = IVTvdata.IVTv.values,          # meidional integrated vapor transport [kg m-1 s-1]
                              regular_Lon = Lon,
                              regular_Lat = Lat,
                              IVTtrheshold = IVTtrheshold,          # Integrated water vapor transport threshold for AR detection [kg m-1 s-1]
                                                                    # JLa: additionall fixed threshold 100 in code
                              AR_Lat = 0,
                              DataName = output_file_name,
                              OutputFolder=output_path ,
                              dict_keys_offset = dict_keys_offset
                            )
                       
                             
    cleanup_dicts(output_path,
                  output_file_name_temp,
                  start_date,
                  end_date, 
                  last_processed_date,
                  type_='IVT'
                 )
        
    cleanup_dicts(output_path,
                  output_file_name_temp,
                  start_date,
                  end_date, 
                  last_processed_date,
                  type_='ARs'
                 )
    
    correct_nc_file(output_path,
                    output_file_name_temp, 
                    start_date,
                    end_date,
                    last_processed_date
                   )
                             
    dict_keys_offset +=5000
