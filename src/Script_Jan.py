import xarray as xr
import numpy as np
import pandas as pd
import datetime
import Tracking_Functions

ds_ivtu = xr.open_dataset(
    '/work/aa0049/a271109/spice-v2.1/chain/work/polarres_WP4_MOSAiC_2020-04_11km/post/2020_04/IVTu_ts.ncz')
ds_ivtv = xr.open_dataset(
    '/work/aa0049/a271109/spice-v2.1/chain/work/polarres_WP4_MOSAiC_2020-04_11km/post/2020_04/IVTv_ts.ncz')

Time = np.array(pd.DataFrame(ds_ivtu.time.values, columns=['Datetime'])[
                'Datetime'].values.astype('datetime64[s]').tolist())
Time_sel = Time[(Time > datetime.datetime(2020, 4, 1, 0, 0)) &
                (Time < datetime.datetime(2020, 4, 3, 0, 0))]

ds_ivtu = ds_ivtu.sel(time=Time_sel)
ds_ivtv = ds_ivtv.sel(time=Time_sel)

Lon, Lat = xr.broadcast(ds_ivtu.rlon, ds_ivtu.rlat)[0].values.T,
xr.broadcast(ds_ivtu.rlon, ds_ivtu.rlat)[1].values.T[:, :]
Mask = 1*(Lat > -999)

ds_ivt_pctl = xr.open_dataset(
    '/work/aa0049/a271109/data_misc/AR_Guan/code/ivt_percentile_mlauer_removed-ens-lev_remapbilWP3domain.nc', decode_times=False)
IVTtrheshold = ds_ivt_pctl.ivt1.values

Tracking_Functions.moaap(Lon=Lon,                           # 2Dlongitude grid centers
                         Lat=Lat,                           # 2D latitude grid spacing
                         Time=Time_sel,                         # datetime vector of data
                         # integer - temporal frequency of data [hour]
                         dT=1,
                         # mask with dimensions [lat,lon] defining analysis region
                         Mask=Mask,

                         # zonal integrated vapor transport [kg m-1 s-1]
                         ivte=ds_ivtu.IVTu.values,
                         # meidional integrated vapor transport [kg m-1 s-1]
                         ivtn=ds_ivtv.IVTv.values,

                         # Integrated water vapor transport threshold for AR detection [kg m-1 s-1]
                         IVTtrheshold=ds_ivt_pctl.ivt1.values,
                         # JLa: additionall fixed threshold 100 in code

                         DataName='test',
                         OutputFolder='./output/'
                         )
