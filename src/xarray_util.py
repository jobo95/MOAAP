from __future__ import annotations

import os
from datetime import datetime

import numpy as np
import pandas as pd
import xarray as xr

from src.GridPoints import RotatedGridPoint, get_Gridpoint_field
from src.object_history import compute_history
from src.Objectcontainer import ObjectContainer
from src.utils import (create_datetime_lists, get_datetime_str, load_pkl,
                       save_as_pkl)


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


def create_obj_from_dict(dict_: dict, key :str, load_coordinates :bool =False, exp=None,load_clusters=False):
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
    cluster_allocations = pd.concat([cluster_allocations_DJF, cluster_allocations_MAM])
    #if load_coordinates:
    #    ds = xr.Dataset(
    #        data_vars=dict(
    #            id_=key,
    #            # exp=exp,
    #            # nc_file=f'{input_path}ObjectMasks_{input_file_name_temp}_{get_datetime_str(start_date)}-{get_datetime_str(end_date)}.nc',
    #            # * units('km^2')),
    #            size=(["times"], dict_[key]["size"] * 1e-6),
    #            # * units('kg/m/s')),
    #            total_IVT=(["times"], dict_[key]["tot"]),
    #            # * units('kg/m/s')),
    #            mean_IVT=(["times"], dict_[key]["mean"]),
    #            max_IVT=(["times"], dict_[key]["max"]),  # * units('kg/m/s')),
    #            min_IVT=(["times"], dict_[key]["min"]),  # * units('kg/m/s')),
    #            mass_center_idy=(["times"], dict_[key]["mass_center_loc"][:, 0]),
    #            mass_center_idx=(["times"], dict_[key]["mass_center_loc"][:, 1]),
    #            
    #            track=(
    #                ["times"],
    #                [RotatedGridPoint(x, y) for x, y in dict_[key]["track"]],
    #            ),
    #            speed=(
    #                ["times"],
    #                np.insert(dict_[key]["speed"], 0, np.nan),
    #            ),  # * units('m/s')),
    #            gridpoints=(["times"], get_Gridpoint_field(key, dict_)),
    #             #clusters=(
    #             #   ["times"],
    #             #   load_cluster_for_container(
    #             #       cluster_allocations, dict_[key]["times"]
    #             #   ),
    #             #),
    #        ),
    #        coords=dict(times=dict_[key]["times"]),
    #    )

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
            #clusters=(
            #    ["times"],
            #    load_cluster_for_container(
            #        cluster_allocations, dict_[key]["times"]
            #    ),
            #),
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

    if load_clusters:
        ds = ds.assign(clusters=(["times"], load_cluster_for_container(cluster_allocations, dict_[key]["times"])))

    return ds


def load_cluster_for_container(
    df: pd.Dataframe, times: np.ndarray[datetime]
) -> list[str]:
    date_list = pd.to_datetime(times).normalize()
    df["time"] = pd.to_datetime(df["time"])
    df["date"] = df["time"].dt.normalize()
    #print (df['date'])
    #print( [df[df["date"] == x] for x in date_list])

    selected_cluster = []
    for x in date_list:
        app = df[df["date"] == x].cluster_name.values
        if len(app) == 1:
            selected_cluster.append(df[df["date"] == x].cluster_name.values.item())
        else:
            selected_cluster.append(np.nan) 
            
    #[df[df["date"] == x].cluster_name.values.item() for x in date_list] or 0
    #print (type(selected_cluster))
    #print (date_list[0])
    #print (len(selected_cluster))

    return selected_cluster
    


def load_tracking_objects(
    input_path :str,
    input_file_name_temp :str,
    type_ :str,
    first_year :int,
    last_year :int,
    load_coordinates :bool=False,
    load_clusters :bool=False,
    exp =None,
    save_pkl : bool =True,
    compute_hist :bool =False,
    correct_last_endtime :bool =False,
    suffix :str = "",
):

    start_date_list, end_date_list = create_datetime_lists(
        first_year, last_year, months=6, correct_last_endtime=correct_last_endtime
    )
    pkl_container_path = (
        f"{exp.path_IVT_tracking}{exp.container_pkl_file}_{first_year}-{last_year}{suffix}"
    )
    if  load_clusters:
        pkl_container_path = pkl_container_path + "_withClusters"


    if os.path.isfile(pkl_container_path + ".pkl"):
        print(f"{pkl_container_path} exists. Loading...")
        IVTobj_ls = load_pkl(pkl_container_path)

    else:
        IVTobj_ls = ObjectContainer([])

        for start_date, end_date in zip(start_date_list, end_date_list):
            print(start_date)
            pickle_file_path = f"{input_path}{type_}_{input_file_name_temp}_{get_datetime_str(start_date)}-{get_datetime_str(end_date)}_corrected"

            dict_ = load_pkl(pickle_file_path)
            for object_id in dict_.keys():
                #print (object_id)
                try:
                    ds = create_obj_from_dict(
                        dict_, object_id, load_coordinates=load_coordinates, load_clusters=load_clusters, exp=exp
                    )
                except ValueError as ex:
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
            print ("Computing history")
        else:
            IVTobj_ls = compute_history(IVTobj_ls)

        if save_pkl:
            print(f"Saving {pkl_container_path}")
            save_as_pkl(IVTobj_ls, pkl_container_path)
        
    

    return IVTobj_ls
