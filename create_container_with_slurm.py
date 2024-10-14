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

exp = Experiments.ICON_CNRM_SSP.value
exp = Experiments.ICON_NORESM_SSP.value
#exp = Experiments.ICON_CNRM_CONTROL.value
#exp = Experiments.ICON_NORESM_CONTROL.value

input_path = exp.IVTobj_out_path

type_ = "IVT"
input_file_name_temp = exp.input_file_name_temp
#"MOAPP_ERA5_100and85controlperc_remapped_3x"

first_year = exp.year_start
last_year = exp.year_end

IVT_objs_ERA5 = load_tracking_objects(
    input_path,
    input_file_name_temp,
    type_,
    first_year,
    last_year,
    load_coordinates=True,
    compute_hist=True,
    load_clusters=True,
    # compute_hist = False,
    exp=exp,
    #var_names_ls=["IVT", "IWV"],
    #var_paths_ls=[
    #    "/work/aa0238/a271093/data/ERA5/1979-2023/ICON_remapped_3x/IVT/",
    #    "/work/aa0238/a271093/data/ERA5/1979-2023/ICON_remapped_3x/IWV/",
    #],
)
