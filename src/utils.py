import datetime
import pickle
from collections import Counter
from itertools import chain, product

import numpy as np
import pandas as pd
from dateutil import relativedelta

from src.GridPoints import RotatedGridPoint
from src.Enumerations import Domains
import xarray as xr
from src.decorators import measure_time_func, measure_time_func_lines

from typing import TYPE_CHECKING
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


def count_objs_grid_points(objs, normalization_factor:float=24.0):
    """

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
def calculate_average_ellapsed_time(objs, normalization_factor:float=1):
    
    counter_init_dict = dict.fromkeys(RotatedGridPoint.get_all_gridpoints(), 0)
    grid_point_counter_time = Counter(counter_init_dict)
    grid_point_counter_normal = Counter(counter_init_dict)

    for idx in range(len(objs)):
        points = objs[idx].gridpoints.values
        
        for j in range(len(points)):

            grid_point_counter_time.update(points[j]*(j+1))
            grid_point_counter_normal.update(points[j])

    grid_point_ls = list(grid_point_counter_normal.keys())
    
    z_time = np.array(list(grid_point_counter_time.values())) 
    z_normal = np.array(list(grid_point_counter_normal.values())) 

    z =np.array([i/j/normalization_factor if j !=0 else -20 for i,j in zip(z_time,z_normal)])
    
    lat = np.array([x.lat for x in grid_point_ls])
    lon = np.array([x.lon for x in grid_point_ls])

    return lon, lat, z

    
#@measure_time_func_lines
def select_by_gridpoint_fraction(obj: xr.Dataset,
                                 domain_grid_point_field : list,
                                 domain_fraction:float=0.5, 
                                 object_fraction:float=0.8,
                                 select_last_timesteps:bool = False,
                                 step:int = 1
                                 ) -> xr.Dataset:
    """Select only those objects that, at  any time step, cover a certain fraction of the domain OR whose overall object size lies within a certain fraction of the domain.

    Args:
        obj (xr.Dataset): object
        domain_grid_point_field (list): list of regular grid points that lie within the domain
        domain_fraction (float, optional): Fraction of domain that has to be covered by object. Defaults to 0.5. If 0 all objects are selected.
        object_fraction (float, optional): Fraction of object that has to lie inside the domain. Defaults to 0.8. 
        select_last_timesteps (bool, optional): If an object covers the domains at timestep i, then select only the i-th to the last timesteps of the object (if set to True). Defaults to False.
        step (int, optional): . Defaults to 1.

    Returns:
        - xr.Dataset: selected objects or None if condition not met
    """
    points_domain=set(domain_grid_point_field)
    points_domain_length=len(points_domain)
    for i,points in enumerate(obj.gridpoints.values[::step]):
        sel_points = set(points).intersection(points_domain)
    
        # fraction of domain covered by  object grid points
        frac1 = len(sel_points)/points_domain_length
        
        # fraction of object grid points that are in the domain
        frac2 = len(sel_points)/len(points)
        
        if frac1>=domain_fraction or frac2>= object_fraction:
            if select_last_timesteps:
                return obj.isel(times=slice(i*step,None))
            return obj
        


    

def read_cluster_csv(file_name:str) -> pd.DataFrame:
    
    return pd.read_csv(file_name)
