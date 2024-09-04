import datetime
import os
import pickle

import cartopy
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import scipy
import xarray as xr
from metpy.units import units

from src.Corrections import *
from src.Enumerations import Domains, Experiments, Month, Season
from src.utils import *
from src.xarray_util import (ObjectContainer, create_obj_from_dict,
                             load_tracking_objects)

exp_ICON_ERA5 = Experiments.ICON_ERA5.value
exp_ERA5 = Experiments.ERA5.value

input_path_ICON_ERA5 = exp_ICON_ERA5.path_IVT_tracking
input_path_ERA5 = exp_ERA5.path_IVT_tracking


type_ = "IVT"
input_file_name_temp_ERA5 = "MOAPP_ERA5_100and85controlperc_remapped_3x"
input_file_name_temp_ICON_ERA5 = "MOAPP_ICON_ERA5_100and85ERA5perc_remapped_3x"

first_year = 1979
last_year = 2022
num_years = last_year - first_year

IVT_objs_ERA5 = load_tracking_objects(
    input_path_ERA5,
    input_file_name_temp_ERA5,
    type_,
    first_year,
    last_year,
    load_coordinates=True,
    compute_hist=True,
    # compute_hist = False,
    exp=exp_ERA5,
    var_names_ls=["IVT", "IWV"],
    var_paths_ls=[
        "/work/aa0238/a271093/data/ERA5/1979-2023/ICON_remapped_3x/IVT/",
        "/work/aa0238/a271093/data/ERA5/1979-2023/ICON_remapped_3x/IWV/",
    ],
    suffix="_NEW",
)
