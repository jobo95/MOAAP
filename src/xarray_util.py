from __future__ import annotations

import glob
import os
import sys
from datetime import datetime

import numpy as np
import pandas as pd
import xarray as xr
from dateutil.relativedelta import relativedelta

from src.GridPoints import GridPoint, RotatedGridPoint, get_Gridpoint_field
from src.object_history import compute_history
from src.Objectcontainer import ObjectContainer
from src.utils import (
    create_datetime_lists,
    get_datetime_str,
    load_pkl,
    save_as_pkl,
    str_to_variable_class,
)

# from memory_profiler import profile


@xr.register_dataset_accessor("get")
class Accessor:
    # TODO accessor overriding warning
    """
    Add some additional accessors to the xr.Datasets
    """

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
        return np.nanmean(getattr(self._obj.get, attr))

    def median(self, attr):
        return np.nanmedian(getattr(self._obj.get, attr))

    def min(self, attr):
        return np.min(getattr(self._obj.get, attr))

    def max(self, attr):
        return np.max(getattr(self._obj.get, attr))

    @property
    def duration(self):
        return self._obj.times.size

    @property
    def speed(self):
        return self._obj.speed.values

    @property
    def gridpoints(self):
        return self._obj.gridpoints.values

    @property
    def clusters(self):
        return self._obj.clusters.values

    @property
    def exp(self):
        return self._obj.exp.values.item()

    def track(self, rotated: bool = True):

        ls = self._obj.track.values

        if rotated:
            return ls
        else:
            return [x.to_regular() for x in ls]

    @property
    def rotated_track(self):
        return self._obj.get.track(rotated=True)

    @property
    def regular_track(self):
        return self._obj.get.track(rotated=False)

    @property
    def mass_center_idx(self):
        return self._obj.mass_center_idx.values

    @property
    def mass_center_idy(self):
        return self._obj.mass_center_idy.values

    @property
    def total_IVT(self):
        return self._obj.total_IVT.values

    @property
    def size(self):
        return self._obj.size

    @property
    def origin(self):

        return self._obj.track.sel(times=self._obj.times[0])


def create_obj_from_dict(
    dict_: dict,
    key: str,
    load_coordinates: bool = False,
    exp=None,
    load_clusters=False,
    var_names_ls: list[str] = None,
    var_dataset_ls: list[xr.Dataset] = None,
):
    """Create Tracking object xr.Dataset from Dictionary

    Args:
        dict_ (dict): Dictionary that contains different attributes of a particular Tracking object
        key (str): Id of the Tracking object
        load_coordinates (bool, optional): Load Tracking objects' Grid points into Dataset. Memory intense. Defaults to False.

    Returns:
        xr.Dataset: Dataset that contains characteristics of tracking object
    """
    cluster_allocations_DJF = pd.read_csv(exp.BMU_path + exp.BMU_file_DJF)
    cluster_allocations_MAM = pd.read_csv(exp.BMU_path + exp.BMU_file_MAM)
    cluster_allocations_JJA = pd.read_csv(exp.BMU_path + exp.BMU_file_JJA)
    cluster_allocations_SON = pd.read_csv(exp.BMU_path + exp.BMU_file_SON)
    cluster_allocations = pd.concat(
        [
            cluster_allocations_DJF,
            cluster_allocations_MAM,
            cluster_allocations_JJA,
            cluster_allocations_SON,
        ]
    )

    ds = xr.Dataset(
        data_vars=dict(
            id_=key,
            exp=exp,
            # nc_file=f'{input_path}ObjectMasks_{input_file_name_temp}_{get_datetime_str(start_date)}-{get_datetime_str(end_date)}.nc',
            # * units('km^2')),
            size=(["times"], dict_[key]["size"] * 1e-6),
            # * units('kg/m/s')),
            total_IVT=(["times"], dict_[key]["tot"]),
            # * units('kg/m/s')),
            mean_IVT=(["times"], dict_[key]["mean"]),
            max_IVT=(["times"], dict_[key]["max"]),  # * units('kg/m/s')),
            min_IVT=(["times"], dict_[key]["min"]),  # * units('kg/m/s')),
            mass_center_idy=(["times"], dict_[key]["mass_center_loc"][:, 0]),
            mass_center_idx=(["times"], dict_[key]["mass_center_loc"][:, 1]),
            # clusters=(
            #    ["times"],
            #    load_cluster_for_container(
            #        cluster_allocations, dict_[key]["times"]
            #    ),
            # ),
            track=(
                ["times"],
                [RotatedGridPoint(x, y) for x, y in dict_[key]["track"]],
            ),
            speed=(
                ["times"],
                np.insert(dict_[key]["speed"], 0, np.nan),
            ),  # * units('m/s')),
        ),
        coords=dict(times=dict_[key]["times"]),
    )

    if load_coordinates:
        ds = ds.assign(gridpoints=(["times"], get_Gridpoint_field(key, dict_)))

    if var_names_ls is not None:
        # ds = ds.assign(**{var_name: (["times"], get_var_field(key, dict_, var_dataset, var_name)) for var_name in var_names})
        ds = ds.assign(**{var_name: (["times"], get_var_field(key, dict_, var_dataset, var_name)) for var_name, var_dataset in zip(var_names_ls, var_dataset_ls)})

    if load_clusters:
        ds = ds.assign(
            clusters=(
                ["times"],
                load_cluster_for_container(cluster_allocations, dict_[key]["times"]),
            )
        )

    return ds


def load_cluster_for_container(df: pd.Dataframe, times: np.ndarray[datetime]) -> list[str]:
    date_list = pd.to_datetime(times).normalize()
    df["time"] = pd.to_datetime(df["time"])
    df["date"] = df["time"].dt.normalize()

    selected_cluster = []
    for x in date_list:
        app = df[df["date"] == x].cluster_name.values
        
        if len(app) == 1:
            selected_cluster.append(df[df["date"] == x].cluster_name.values.item())
        else:
            selected_cluster.append(np.nan)

    # [df[df["date"] == x].cluster_name.values.item() for x in date_list] or 0
    return selected_cluster


# @profile
def load_tracking_objects(
    input_path: str,
    input_file_name_temp: str,
    type_: str,
    first_year: int,
    last_year: int,
    load_coordinates: bool = False,
    load_clusters: bool = False,
    var_paths_ls: list[str] = None,
    var_names_ls: list[str] = None,
    exp=None,
    save_pkl: bool = True,
    compute_hist: bool = False,
    correct_last_endtime: bool = False,
    suffix: str = "",
):

    start_date_list, end_date_list = create_datetime_lists(first_year, last_year, months_step=6, correct_last_endtime=correct_last_endtime)
    pkl_container_path = f"{exp.IVTobj_out_path}{exp.container_pkl_file}_{first_year}-{last_year}{suffix}"
    if load_clusters:
        pkl_container_path = pkl_container_path + "_withClusters"

    if var_names_ls is not None:
        pkl_container_path = pkl_container_path + "_" + "_".join(var_names_ls)

    if os.path.isfile(pkl_container_path + ".pkl"):
        print(f"{pkl_container_path} exists. Loading...")
        IVTobj_ls = load_pkl(pkl_container_path)

    else:
        print (f"{pkl_container_path} does not exist. Creating...")
        IVTobj_ls = ObjectContainer([])

        for start_date, end_date in zip(start_date_list, end_date_list):
            print(start_date)
            pickle_file_path = f"{input_path}{type_}_{input_file_name_temp}_{get_datetime_str(start_date)}-{get_datetime_str(end_date)}_corrected"

            dict_ = load_pkl(pickle_file_path)

            var_ds_ls = None
            if var_paths_ls is not None:
                var_ds_ls = []
                for var_path in var_paths_ls:
                    files = glob.glob(var_path + "*.nc")
                    full_var_ds = xr.open_mfdataset(files)

                    var_ds = full_var_ds.sel(time=slice(start_date, end_date + relativedelta(months=1))).load()

                    var_ds_ls.append(var_ds)

            for object_id in dict_.keys():
                # print (object_id)
                try:
                    ds = create_obj_from_dict(
                        dict_,
                        object_id,
                        load_coordinates=load_coordinates,
                        load_clusters=load_clusters,
                        exp=exp,
                        var_dataset_ls=var_ds_ls,
                        var_names_ls=var_names_ls,
                    )
                except ValueError:
                    continue

                IVTobj_ls.append(ds)

        if save_pkl:
            print(f"Saving {pkl_container_path}")
            save_as_pkl(IVTobj_ls, pkl_container_path)

    if compute_hist:
        pkl_container_path = pkl_container_path + "_withHist"

        if os.path.isfile(pkl_container_path + ".pkl"):
            print(f"{pkl_container_path} exists. Loading...")
            IVTobj_ls = load_pkl(pkl_container_path)
        else:
            print("Computing history")
            IVTobj_ls = compute_history(IVTobj_ls)

        if save_pkl:
            print(f"Saving {pkl_container_path}")
            save_as_pkl(IVTobj_ls, pkl_container_path)

    return IVTobj_ls


def get_var_field(key, dict_, var_dataset, var_name):

    lat_idx_slice = dict_[key]["lat_idx_slice"]
    lon_idx_slice = dict_[key]["lon_idx_slice"]

    # lat_slice = GridPoint.rotated_lat_grid[lat_idx_slice, lon_idx_slice]
    # lon_slice = GridPoint.rotated_lon_grid[lat_idx_slice, lon_idx_slice]

    var_slice_temp = getattr(var_dataset.sel(time=dict_[key]["times"]), var_name)
    var_slice = var_slice_temp.values[:, lat_idx_slice, lon_idx_slice]

    indices = np.argwhere(~np.isnan(dict_[key]["data_slice"]))
    time_steps = np.unique(indices[:, 0])

    ls = []
    for tstep in time_steps:
        idx = indices[indices[:, 0] == tstep][:, 1:]

        # sub_ls_lat = [lat_slice[tuple(x)] for x in idx]
        # sub_ls_lon = [lon_slice[tuple(x)] for x in idx]
        sub_ls_var = [var_slice[tstep, x[0], x[1]] for x in idx]

        # sub_dict = {
        #    RotatedGridPoint(lat, lon): str_to_variable_class(var_name)(var)
        #    for lat, lon, var in zip(sub_ls_lat, sub_ls_lon, sub_ls_var)
        # }
        sub_dict = [str_to_variable_class(var_name)(var) for var in sub_ls_var]
        ls.append(sub_dict)
    return np.array(ls, dtype="object")
