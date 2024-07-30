from __future__ import annotations

from typing import List

import numpy as np
import pandas as pd
import xarray as xr

from src.Enumerations import Domains


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
    def __getitem__(self, index):
        result = super().__getitem__(index)
        if isinstance(index, slice):
            return ObjectContainer(result)
        else:
            return result
        
        
    def append(self, item) -> None:
        """Append Tracking

        Args:
            item (xr.Dataset): Tracking Object to append

        Raises:
            TypeError: If appended Tracking object is not a xr.Dataset

        """

        # if not isinstance(item, xr.Dataset):
        #    raise TypeError("Object container can only append xarray Dataset objects")
        return super().append(item)

    def sel_season(self, season  ) -> ObjectContainer:
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

    def sortby(self, attr, reverse=False):

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

    def filter_by_attr_category(self, attr, category) -> ObjectContainer:
        q033 = self.quantile(attr=attr, quant=0.33)
        q066 = self.quantile(attr=attr, quant=0.66)

        if category == "Small":
            return self.filter_by_median(threshold=q033, attr=attr, above=False)

        if category == "Medium":
            return self.filter_by_median(
                threshold=q033, attr=attr, above=True
            ).filter_by_median(threshold=q066, attr=attr, above=False)

        if category == "Large":
            return self.filter_by_median(threshold=q066, attr=attr, above=True)

    def seltimesteps(self, time_slice: slice) -> ObjectContainer:
        """Select timesteps from individual objects

        Args:
            time_slice (slice): time indices to be selected

        """

        return ObjectContainer([x.isel(times=time_slice) for x in self])

    def sel_by_time(self,time : np.datetime64) -> ObjectContainer:
        return ObjectContainer([x for x in self if time in x.times])

    def sel_by_domain(self, domain: Domains, origin: bool = True) -> ObjectContainer:
        if origin:
            return ObjectContainer(
                [x for x in self if x.get.regular_track[0] in domain.value]
            )
        else:
            return ObjectContainer(
                [x for x in self if x.get.regular_track[-1] in domain.value]
            )

    def sel_by_regime(self, regime_name: str) -> ObjectContainer:
        def get_idx(obj_, regime_name):
            list_ = list(obj_.get.clusters)
            idx = [i for i in range(len(list_)) if list_[i] == regime_name]
            return idx

        container = ObjectContainer(
            [obj_.isel(times=get_idx(obj_, regime_name)) for obj_ in self]
        )
        return ObjectContainer([x for x in container if x.times.size > 0])

    def get_index_by_id(self, obj_id :int) -> xr.Dataset:
        for ind,obj in enumerate(self):
            if int(obj_id) == int(obj.id_):
                return ind
            else:
                continue
            

