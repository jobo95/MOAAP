import datetime
import pickle
import numpy as np
from itertools import product, chain
from dateutil import relativedelta
from collections import Counter
import pandas as pd


def create_datetime_lists(first_year, last_year, months=7, correct_last_endtime=True):
    ###TODO####
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


def count_objs_grid_points(objs, normalization_factor=24.0):
    """

    Args:
        objs (ObjectContainer): Object Container with tracking objects.
        normalization_factor (float, optional): Defaults to 24, converts the count unit to days in case of hourly input data.

    Returns:
        -lon: 1-D array of longitudes
        -lat: 1-D array of latitudes
        -z: 1-D array of count values

    """

    grid_point_counter = Counter()

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
    # return grid_point_counter

    
    
def read_cluster_csv(file_name):
    return pd.read_csv(file_name)
