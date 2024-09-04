import datetime
import pickle
from collections import Counter
from itertools import chain, product

import numpy as np
import pandas as pd
import xarray as xr
from dateutil import relativedelta

from src.GridPoints import RegularGridPoint
from src.Objectcontainer import ObjectContainer

# from src.decorators import measure_time_func, measure_time_func_lines
from src.GridPoints import RotatedGridPoint
from src.Variable_classes import *


def create_datetime_lists(
    first_year: int, last_year: int, months: int = 7, correct_last_endtime: bool = True
):
    """
       Creates two lists with 1-month overlap

    Args:
        first_year (datetime): First year
        last_year (datetime): Last year
        months (int, optional):time step in months between subseuent dates. Defaults to 7.
        correct_last_endtime (bool, optional): If true, set. Defaults to True.

    Returns:
        - start_date_list
        - end_date_list
    """

    start_year_ar = np.arange(first_year, last_year)
    start_month_ar = [1, 7]
    start_date_list = [
        datetime.datetime(x, y, 1, 0, 0)
        for x, y in product(start_year_ar, start_month_ar)
    ]
    end_date_list = [
        x + relativedelta.relativedelta(months=months) for x in start_date_list
    ]

    if correct_last_endtime:
        end_date_list[-1] = end_date_list[-1] - relativedelta.relativedelta(months=1)

    # end_date_list[0].strftime("%Y_%m_%d")
    return start_date_list, end_date_list


def get_datetime_str(dt) -> str:
    """Convert datetime object to string.

    Args:
        dt (datetime): datetime object

    Returns:
        str: String of datetime object.
    """
    return dt.strftime("%Y_%m_%d")


def load_pkl(file_name) -> dict:
    """
    Load pickle file

    Args:
        file_name (str): Name of the pickle file (without .pkl suffix)

    Returns:
        dict: nested dictionary with Tracking Object Information.
    """

    with open(file_name + ".pkl", "rb") as pickle_file:
        ob_dict = pickle.load(pickle_file)
    return ob_dict


def save_as_pkl(dict_, output_name) -> None:
    """Save (dict) objects as pickle file-

    Args:
        dict_ (dict): Object to be saved
        output_name (str): Name of saved pickle file
    """

    with open(output_name + ".pkl", "wb") as handle:
        pickle.dump(dict_, handle, protocol=pickle.HIGHEST_PROTOCOL)


def count_objs_grid_points(
    objs: ObjectContainer, normalization_factor: float = 24.0
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Counts the absolute number of objects at each grid point over all objects' time steps

    Args:
        objs (ObjectContainer): Object Container with tracking objects.
        normalization_factor (float, optional): Defaults to 24, converts the count unit to days in case of hourly input data.

    Returns:
        -lon: 1-D array of longitudes
        -lat: 1-D array of latitudes
        -z: 1-D array of count values

    """
    counter_init_dict = dict.fromkeys(RotatedGridPoint.get_all_gridpoints(), 0)
    grid_point_counter = Counter(counter_init_dict)

    for idx in range(len(objs)):
        points = objs[idx].gridpoints.values

        # flatten grid points into list
        points_flattened = list(chain.from_iterable(points))

        grid_point_counter.update(points_flattened)

    grid_point_ls = list(grid_point_counter.keys())
    z = np.array(list(grid_point_counter.values())) / normalization_factor

    lat = np.array([x.lat for x in grid_point_ls])
    lon = np.array([x.lon for x in grid_point_ls])

    return lon, lat, z


def calculate_average_ellapsed_time(
    objs: ObjectContainer, normalization_factor: float = 1
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Calculate the average ellapsed time an object needs to reach a certain grid point (not the objects' track, but any grid point covered by the object)

    Args:
        objs (ObjectContainer): IVT Objects
        normalization_factor (float, optional): Factor that scales the average ellapsed time returned (e.g. to days). Defaults to 1.

    Returns:
        tuple[np.ndarray, np.ndarray, np.ndarray]: lat, lon, averaged ellapsed time
    """

    # initialize counter with all grid point counts set to zero
    counter_init_dict = dict.fromkeys(RotatedGridPoint.get_all_gridpoints(), 0)
    grid_point_counter_time = Counter(counter_init_dict)
    grid_point_counter_normal = Counter(counter_init_dict)

    # iterate over all objects
    for idx in range(len(objs)):
        points = objs[idx].gridpoints.values

        # iterate over all time steps of object
        for j in range(len(points)):

            # save the ellapsed time the object needed to reach the grid points
            grid_point_counter_time.update(points[j] * (j + 1))

            # count the absolute number of grid point occurrences
            grid_point_counter_normal.update(points[j])

    grid_point_ls = list(grid_point_counter_normal.keys())

    z_time = np.array(list(grid_point_counter_time.values()))
    z_normal = np.array(list(grid_point_counter_normal.values()))

    # compute the average time from the sumed up times and the average number of grid points occurrences
    z = np.array(
        [
            i / j / normalization_factor if j != 0 else -20
            for i, j in zip(z_time, z_normal)
        ]
    )

    lat = np.array([x.lat for x in grid_point_ls])
    lon = np.array([x.lon for x in grid_point_ls])

    return lon, lat, z


def calculate_variable_sum(objs: ObjectContainer,
                           attr :str, 
                           average_per_object :bool = False,
                           consider_history:bool = False
                            ) -> tuple[np.ndarray, np.ndarray, np.ndarray]:

    # initialize counter with all grid point counts set to zero
    counter_init_dict = dict.fromkeys(RotatedGridPoint.get_all_gridpoints(), 0)

    grid_point_counter = Counter(counter_init_dict)
    variable_dict = counter_init_dict

    # iterate over all objects
    for idx in range(len(objs)):
        #get objects' grid points and variables
        points = objs[idx].gridpoints.values
        variable = getattr(objs[idx],attr).values

        # iterate over all time steps of object
        for tstep in range(len(points)):
            
            # count the absolute number of grid point occurrences
            grid_point_counter.update(points[tstep])

            # iterate over all grid points at time step  and add the variable value to dict
            for i,point in enumerate(points[tstep]):
                variable_dict[point] += variable[tstep][i]

    z =list(variable_dict.values())

    z = np.array([x.value if isinstance(x, str_to_variable_class(attr)) else x for x in z])
    #z = np.array([x.value if isinstance(x, IWV) else x for x in z])

    if average_per_object:
        z = z.item()
        z= np.array([val/point if point != 0 else -20 for val, point in zip(z, grid_point_counter.values())])

    

    grid_point_ls = list(grid_point_counter.keys())
    lat = np.array([x.lat for x in grid_point_ls])
    lon = np.array([x.lon for x in grid_point_ls])          
    
    return lon, lat, z 


def read_cluster_csv(file_name: str) -> pd.DataFrame:

    return pd.read_csv(file_name)


def str_to_variable_class(class_name: str):

    return globals()[class_name]
