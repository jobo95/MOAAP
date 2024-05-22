from __future__ import annotations
import numpy as np
import xarray as xr
import pandas as pd
from metpy.units import units
from dateutil import relativedelta
from src.utils import *
from src.GridPoints import *
from typing import Sequence
from numpy.typing import ArrayLike


class ObjectContainer(list):
    """
    Custom list-like class, which elements are xr.dataset objects and contain information about different Tracking Objects.
    Implements  custom  methods to conveniently access and compute statistics of attributes of Tracking objects.
    """

    def __init__(self, iterable) -> None:
        """Initialize container instance.

        Args:
            iterable: Sequence containing initial Tracking objects ()

        Raises:
            TypeError: If Sequence objects are not  xr.Dataset objects
        """

        if not all(map(lambda x: isinstance(x, xr.Dataset), iterable)):
            raise TypeError(
                "Object container can only be initialized with a sequence that only contains xarray Datasets"
            )

        super().__init__(iterable)

    def append(self, item) -> None:
        """Append Tracking

        Args:
            item (xr.Dataset): Tracking Object to append

        Raises:
            TypeError: If appended Tracking object is not a xr.Dataset

        """

        if not isinstance(item, xr.Dataset):
            raise TypeError("Object container can only append xarray Dataset objects")
        return super().append(item)

    def sel_season(self, season) -> ObjectContainer:
        """Select tracking objects that start in a specific season

        Args:
            season (Enum or list-like): Season to be selected

        Returns:
            ObjectContainer
        """
        return ObjectContainer(
            [x for x in self if pd.to_datetime(x.get.start_date).month in season]
        )

    def get_attributes(self, attr: str) -> List:
        """Get  a specific attribute from all Tracking objects in Container.

        Args:
            attr (str): Attribute name

        Returns:
            list: List with attribute values of individual Tracking Objects
        """

        return [getattr(x.get, attr) for x in self]

    def obj_means(self, attr: str):
        """
        Calculate mean values of attribute for each individual Tracking object in Container.'

        Args:
            attr (str): Attribute name

        Returns:
            Array-like: attribute's mean value for each individual Tracking object
        """
        return np.squeeze([x.get.mean(attr) for x in self])

    def obj_medians(self, attr: str):
        """
        Calculate median values of attribute for each individual Tracking object in Container.'

        Args:
            attr (str): Attribute name

        Returns:
            Array-like: attribute's mean value for each individual Tracking object
        """
        return np.squeeze([x.get.median(attr) for x in self])

    def max(self, attr: str) -> float:
        """
        Get the attributes' maximum value among all Tracking objects.

        Args:
            attr (str):Attribute name

        Returns:
            float: max value
        """
        return float(np.max([getattr(x.get, attr) for x in self]))

    def quantile(self, attr: str, quant: float) -> float:
        """Compute quantile of attribute over all Tracking Objects.

        Args:
            attr (str): Attribute name
            quant (float): quantile

        Returns:
            float:quantile of attribute
        """
        return np.quantile([x.get.mean(attr) for x in self], quant)

    def count(self) -> int:
        """

        Returns:
            int: Number of Tracking objects in Container
        """
        return len(self)

    def sortby(self, attr, reversel=False):

        return self.sort(reverse=reverse, key=lambda x: getattr(x.get, attr))

    def filter_by_median(self, threshold, attr, above=True) -> ObjectContainer:
        """Select only those Tracking Objects in Container which attributes' median value are below/above a certain threshold

        Args:
            threshold (float): Treshold value
            attr (str): Attribute name
            above (bool, optional): Select only objects with attriubte median value above threshold. Defaults to True.

        Returns:
            Object_container: Selected Tracking objects
        """
        if above:

            return ObjectContainer([x for x in self if x.get.median(attr) > threshold])
        else:
            return ObjectContainer([x for x in self if x.get.median(attr) < threshold])

    def seltimesteps(self, time_slice:slice) -> ObjectContainer:
        
        return ObjectContainer([x.isel(times=time_slice) for x in self])

@xr.register_dataset_accessor("get")
class Accessor:
    ### TODO accessor overriding warning######
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
    def track_lat(self):
        return [x.lat for x in self._obj.track.values]

    @property
    def track_lon(self):
        return [x.lon for x in self._obj.track.values]

    def track(self, rotated: bool = True):

        ls = self._obj.track.values

        if rotated:
            return ls
        else:
            return [x.to_regular() for x in ls]

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
    dict_,
    key,
    load_coordinates=False,
):
    """Create Tracking object xr.Dataset from Dictionary

    Args:
        dict_ (dict): Dictionary that contains different attributes of a particular Tracking object
        key (str): Id of the Tracking object
        load_coordinates (bool, optional): Load Tracking objects' Grid points into Dataset. Memory intense. Defaults to False.

    Returns:
        xr.Dataset: Dataset that contains characteristics of tracking object
    """

    if load_coordinates:
        ds = xr.Dataset(
            data_vars=dict(
                id_=key,
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
                # track_rlat=(['times'], dict_[key]['track'][:, 0]),
                # track_rlon=(['times'], dict_[key]['track'][:, 1]),
                # track=(
                #    ["times"],
                #    [RotatedGridPoint(x, y) for x, y in dict_[key]["track"]],
                # ),
                speed=(
                    ["times"],
                    np.insert(dict_[key]["speed"], 0, np.nan),
                ),  # * units('m/s')),
                gridpoints=(["times"], get_Gridpoint_field(key, dict_)),
            ),
            coords=dict(times=dict_[key]["times"]),
        )

    else:
        #### TODO get rid of boilerplate code######
        ds = xr.Dataset(
            data_vars=dict(
                id_=key,
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
                # track_rlat=(['times'], dict_[key]['track'][:, 0]),
                # track_rlon=(['times'], dict_[key]['track'][:, 1]),
                # track=(
                #    ["times"],
                #    [RotatedGridPoint(x, y) for x, y in dict_[key]["track"]],
                # ),
                speed=(
                    ["times"],
                    np.insert(dict_[key]["speed"], 0, np.nan),
                ),  # * units('m/s')),
            ),
            coords=dict(times=dict_[key]["times"]),
        )

    return ds
