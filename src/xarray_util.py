
import numpy as np
import xarray as xr
import pandas as pd
from metpy.units import units
from dateutil import relativedelta

from src.utils import *


class Object_container(list):

    

    def __init__(self, iterable):
        for item in iterable:
            if not isinstance(item,xr.Dataset):
                raise TypeError("Object container can only be initialized with a sequence that only contains xarray Datasets")

        super().__init__(iterable)

    def append(self, item: xr.Dataset) -> None:
        if not isinstance(item, xr.Dataset):
            raise TypeError(
                "Object container can only append xarray Dataset objects")
        return super().append(item)

    def sel_season(self, season):
        return Object_container([x for x in self if pd.to_datetime(x.get.start_date).month in season])

    def get_attributes(self, attr):
        return [getattr(x.get, attr) for x in self]

    def obj_means(self, attr):
        return np.squeeze([x.get.mean(attr) for x in self])

    def max(self, attr):
        return np.max([getattr(x.get, attr) for x in self])

    def min(self, attr):
        return np.max([getattr(x.get, attr) for x in self])

    def quantile(self, attr, quant):
        return np.quantile([x.get.mean(attr) for x in self], quant)

    def count(self):
        return len(self)

    def sortby(self, attr, reverse=False):

        return self.sort(reverse=reverse, key=lambda x: getattr(x.get, attr))

    def filter_by_mean(self, threshold, attr, above=True):
        if above:

            return Object_container([x for x in self  if x.get.mean(attr) > threshold])
        else:
            return Object_container([x for x in self  if x.get.mean(attr) < threshold])


def create_obj_from_dict(dict_, key, input_path, input_file_name_temp, start_date, end_date, input_field_grid,  nc_correct=True, load_coordinates=False):
    if nc_correct:
        end_date = end_date+relativedelta.relativedelta(months=1)
    
    if load_coordinates:
        ds = xr.Dataset(
            data_vars=dict(
                id_=key,
    
                nc_file=f'{input_path}ObjectMasks_{input_file_name_temp}_{get_datetime_str(start_date)}-{get_datetime_str(end_date)}.nc',
                size=(['times'], dict_[key]['size']*1e-6 ),  # * units('km^2')),
    
                total_IVT=(['times'], dict_[key]['tot']),  # * units('kg/m/s')),
                mean_IVT=(['times'], dict_[key]['mean']),  # * units('kg/m/s')),
                max_IVT=(['times'], dict_[key]['max']),  # * units('kg/m/s')),
                min_IVT=(['times'], dict_[key]['min']),  # * units('kg/m/s')),
    
                mass_center_rlat=(['times'], dict_[key]['mass_center_loc'][:, 0]),
                mass_center_rlon=(['times'], dict_[key]['mass_center_loc'][:, 1]),
    
                track_rlat=(['times'], dict_[key]['track'][:, 0]),
                track_rlon=(['times'], dict_[key]['track'][:, 1]),
    
                speed=(['times'], np.insert(
                    dict_[key]['speed'], 0, np.nan)),  # * units('m/s')),
                rlats=(['times'], get_coordinates(
                    key, dict_, input_field_grid)[0]),
                rlons=(['times'], get_coordinates(
                    key, dict_, input_field_grid)[1]),
    
            ),
            coords=dict(
                times=dict_[key]['times']
            )
        )

    else:
        ds = xr.Dataset(
            data_vars=dict(
                id_=key,
    
                nc_file=f'{input_path}ObjectMasks_{input_file_name_temp}_{get_datetime_str(start_date)}-{get_datetime_str(end_date)}.nc',
                size=(['times'], dict_[key]['size']*1e-6 ),  # * units('km^2')),
    
                total_IVT=(['times'], dict_[key]['tot']),  # * units('kg/m/s')),
                mean_IVT=(['times'], dict_[key]['mean']),  # * units('kg/m/s')),
                max_IVT=(['times'], dict_[key]['max']),  # * units('kg/m/s')),
                min_IVT=(['times'], dict_[key]['min']),  # * units('kg/m/s')),
    
                mass_center_rlat=(['times'], dict_[key]['mass_center_loc'][:, 0]),
                mass_center_rlon=(['times'], dict_[key]['mass_center_loc'][:, 1]),
    
                track_rlat=(['times'], dict_[key]['track'][:, 0]),
                track_rlon=(['times'], dict_[key]['track'][:, 1]),
                speed=(['times'], np.insert(
                    dict_[key]['speed'], 0, np.nan)),  # * units('m/s')),
                # regular_lats=(['times'], get_coordinates(key, dict_,regular_coords=True)[0]),
                # regular_lons=(['times'], get_coordinates(key, dict_,regular_coords=True)[1])
    
            ),
            coords=dict(
                times=dict_[key]['times']
            )
        )


    return ds


@xr.register_dataset_accessor("get")
class Accessor:
    def __init__(self, xarray_obj):
        self._obj = xarray_obj
        # self.start_date = None

    @property
    def start_date(self):
        return self._obj.times[0].values

    @property
    def nc_file(self):
        return self._obj.nc_file.values.tolist()

    def mean(self, attr):
        return np.mean(getattr(self._obj.get, attr))

    def min(self, attr):
        return np.min(getattr(self._obj.get, attr))

    def max(self, attr):
        return np.max(getattr(self._obj.get, attr))

    @property
    def duration(self):
        return self._obj.times.size

    @property
    def speed(self):
        return self._obj.speed


    @property
    def track_coord(self, rotated=True):
        lon = self._obj.track_rlon
        lat = self._obj.track_rlat

        if rotated:
            return lat,lon

        return convert_to_regcoord(lat,lon)

    @property
    def track_lat(self, rotated=True):
        return self._obj.track_rlat

    @property
    def track_lon(self,rotated=True):
        return self._obj.track_rlon

    @property
    def mass_center_lon(self,rotated=True):
        return self._obj.mass_center_rlon

    @property
    def mass_center_lat(self,rotated=True):
        return self._obj.mass_center_rlat

    @property
    def total_IVT(self):
        return self._obj.total_IVT

    @property
    def size(self):
        return self._obj.size

    @property
    def regular_lat_origin(self):
        return float(self.regular_lats.sel(times=self.times[0]))

    @property
    def rlat_origin(self):
        return float(self._obj.track_rlat.sel(times=self._obj.times[0]).values)

    @property
    def rlon_origin(self):
        return self._obj.track_rlon.sel(times=self._obj.times[0]).values

    #@cached_property


    # @property
    # def mean(self):
    #    return np.mean(getattr(self._obj, "size"))

    # @cached_property
    # def grid_points(self, cache =False):
    #    ds = xr.open_dataset(self._obj.get.nc_file, cache = cache)
    #    return ds


def get_coordinates(key, dict_, input_field_grid,  regular_coords=False):

    lat_idx_slice = dict_[key]['lat_idx_slice']
    lon_idx_slice = dict_[key]['lon_idx_slice']

    grid_field = xr.open_dataset(input_field_grid, cache=True)

    if regular_coords:
        regular_Lon = grid_field.lon.values
        regular_Lat = grid_field.lat.values

        lat_slice = regular_Lat[lat_idx_slice, lon_idx_slice]
        lon_slice = regular_Lon[lat_idx_slice, lon_idx_slice]

    else:

        rLon = xr.broadcast(grid_field.rlon, grid_field.rlat)[0].values.T
        rLat = xr.broadcast(grid_field.rlon, grid_field.rlat)[1].values.T
        lat_slice = rLat[lat_idx_slice, lon_idx_slice]
        lon_slice = rLon[lat_idx_slice, lon_idx_slice]

    indices = np.argwhere(~np.isnan(dict_[key]['data_slice']))  # [:,1]
    time_steps = np.unique(indices[:, 0])

    # coordinates_ls = []
    ls_lat = []
    ls_lon = []
    for tstep in time_steps:
        idx = indices[indices[:, 0] == tstep][:, 1:]

        sub_ls_lat = [lat_slice[tuple(x)] for x in idx]
        sub_ls_lon = [lon_slice[tuple(x)] for x in idx]

        # sub_coordinates_ls = [grid_point(lat,lon) for lat,lon in zip(sub_ls_lat,sub_ls_lon)]

        ls_lat.append(sub_ls_lat)
        ls_lon.append(sub_ls_lon)

        # np.append(arr,ls)
    return (np.array(ls_lat, dtype='object'), np.array(ls_lon, dtype='object'))
