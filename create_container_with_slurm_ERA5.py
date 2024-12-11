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

exp_ERA5=Experiments.ERA5.value

input_path_ERA5= exp_ERA5.IVTobj_out_path


type_='IVT'
input_file_name_temp_ERA5 = 'MOAPP_ERA5_100and85controlperc_remapped_3x'

first_year = 1979
last_year = 2022
num_years = last_year-first_year

IVT_objs_ERA5 = load_tracking_objects(input_path_ERA5,
                                      input_file_name_temp_ERA5,
                                      type_,
                                      first_year,
                                      last_year,
                                      load_coordinates=True,
                                      compute_hist = True,
                                      load_clusters=True,
                                      #compute_hist = False,
                                      exp=exp_ERA5,
                                      
                                      
                                      )