from __future__ import annotations

from typing import List

import numpy as np
import pandas as pd
import xarray as xr

from src.GridPoints import Domain, select_by_gridpoint_fraction


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
            raise TypeError("Object container can only be initialized with a sequence that only contains xarray Datasets")

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

    def sel_season(self, season) -> ObjectContainer:
        """Select tracking objects that start in a specific season

        Args:
            season (Enum or list-like): Season to be selected

        Returns:
            ObjectContainer
        """
        return ObjectContainer([x for x in self if pd.to_datetime(x.get.start_date).month in season])

    def get_attributes(self, attr: str) -> List:
        """Get  a specific attribute from all Tracking objects in Container.

        Args:
            attr (str): Attribute name

        Returns:
            list: List with attribute values of individual Tracking Objects
        """

        if not isinstance(attr, str):
            raise TypeError("attr must be a string")

        return [getattr(x.get, attr) for x in self]

    def obj_means(self, attr: str):
        """
        Calculate mean values of attribute for each individual Tracking object in Container.'

        Args:
            attr (str): Attribute name

        Returns:
            Array-like: attribute's mean value for each individual Tracking object
        """

        if not isinstance(attr, str):
            raise TypeError("attr must be a string")

        return np.squeeze([x.get.mean(attr) for x in self])

    def obj_medians(self, attr: str):
        """
        Calculate median values of attribute for each individual Tracking object in Container.'

        Args:
            attr (str): Attribute name

        Returns:
            Array-like: attribute's median value for each individual Tracking object
        """
        if not isinstance(attr, str):
            raise TypeError("attr must be a string")
        return np.squeeze([x.get.median(attr) for x in self])

    def max(self, attr: str) -> float:
        """
        Get the attributes' maximum value among all Tracking objects.

        Args:
            attr (str):Attribute name

        Returns:
            float: max value
        """
        if not isinstance(attr, str):
            raise TypeError("attr must be a string")
        return float(np.max([getattr(x.get, attr) for x in self]))

    def quantile(self, attr: str, quant: float) -> float:
        """Compute quantile of attribute over all Tracking Objects.

        Args:
            attr (str): Attribute name
            quant (float): quantile

        Returns:
            float:quantile of attribute
        """
        if not isinstance(attr, str):
            raise TypeError("attr must be a string")
        if quant < 0 or quant > 1:
            raise ValueError("quant must be between 0 and 1")
        if not isinstance(quant, float):
            raise TypeError("quant must be a float")

        return np.quantile([x.get.mean(attr) for x in self], quant)

    def count(self) -> int:
        """

        Returns:
            int: Number of Tracking objects in Container
        """
        return len(self)

    def sortby(self, attr: str, reverse: bool = False) -> ObjectContainer:
        """Sort Objects in container according to some attribute

        Args:
            attr (str): Object attribute that should be used for sorting
            reverse (bool, optional): If True, sort in descending order. Defaults to False.

        Returns:
            ObjectContainer: sorted Container
        """
        if not isinstance(attr, str):
            raise TypeError("attr must be a string")

        if not isinstance(reverse, bool):
            raise TypeError("reverse must be a boolean")

        return self.sort(reverse=reverse, key=lambda x: getattr(x.get, attr))

    def filter_by_median(self, threshold: float, attr: str, above: bool = True) -> ObjectContainer:
        """Select only those Tracking Objects in Container which attributes' median value are below/above a certain threshold

        Args:
            threshold (float): Treshold value
            attr (str): Attribute name
            above (bool, optional): Select only objects with attriubte median value above threshold. Defaults to True.

        Returns:
            Object_container: Selected Tracking objects
        """

        if not isinstance(attr, str):
            raise TypeError("attr must be a string")
        if not isinstance(threshold, float):
            raise TypeError("threshold must be a float")
        if not isinstance(above, bool):
            raise TypeError("above must be a boolean")

        if above:

            return ObjectContainer([x for x in self if x.get.median(attr) > threshold])
        else:
            return ObjectContainer([x for x in self if x.get.median(attr) < threshold])

    def filter_by_attr_category(self, attr: str, category: str) -> ObjectContainer:
        """Filter out only those elements, for which the median of a specific attribute falls into a certain category ("small", "medium", "large").
            "small" refers to all objects with attributes value below the  0.33 quantiles (quantile determined from all objects)
            "medium" refers to all objects with attributes value between 0.33 and 0.66 quantiles
            "large" refers to all objects with attributes value above the 0.66 quantiles

        Args:
            attr (str): Attribute name
            category (str): "small", "medium" or "large"

        Returns:
            ObjectContainer: Filtered Object Container
        """

        if not isinstance(attr, str):
            raise TypeError("attr must be a string")
        if not isinstance(category, str):
            raise TypeError("category must be a string")
        if category not in ["Small", "Medium", "Large"]:
            raise ValueError("category must be one of 'Small', 'Medium' or 'Large'")

        q033 = self.quantile(attr=attr, quant=0.33)
        q066 = self.quantile(attr=attr, quant=0.66)

        if category == "Small":
            return self.filter_by_median(threshold=q033, attr=attr, above=False)

        if category == "Medium":
            return self.filter_by_median(threshold=q033, attr=attr, above=True).filter_by_median(threshold=q066, attr=attr, above=False)

        if category == "Large":
            return self.filter_by_median(threshold=q066, attr=attr, above=True)

    def seltimesteps(self, time_slice: slice) -> ObjectContainer:
        """Select timesteps from individual objects

        Args:
            time_slice (slice): time indices to be selected

        Returns:
            ObjectContainer: Object container with objects which time steps have been selected
        """
        if not isinstance(time_slice, slice):
            raise TypeError("time_slice must be a slice")

        return ObjectContainer([x.isel(times=time_slice) for x in self if x.isel(times=time_slice).times.size > 0])

    def sel_by_time(self, time: np.datetime64) -> ObjectContainer:
        """Select only those object which live at a certain time stamp

        Args:
            time (np.datetime64): Time stamp

        """
        if not isinstance(time, np.datetime64):
            raise TypeError("time must be a np.datetime64")

        return ObjectContainer([x for x in self if time in x.times])

    def sel_by_domain(
        self,
        domain: Domain,
        type_: str,
        domain_frac: float = None,
        object_frac: float = None,
        select_last_timesteps: bool = False,
    ) -> ObjectContainer:
        """Select objects which trajectories are in a certain domain (at their origin, end or at any time). Selections for "start" and "end" are currently only  based on regular tracks.
        If "domain_frac" and "object_frac" are not set, the track is used for selection. If one of "domain_frac" or "object_frac" is set, both parameters have to be set.


        Args:
            domain (Domain): Domain object
            type_ (str): Can be either 'origin', 'end' or 'anytime'
            domain_frac (float, optional): Fraction of domain covered by object. If set than the spatial extend of the object is considered. Defaults to None.
            object_frac (float, optional): Fraction of total object size that is inside the Domain. Defaults to None.
            select_last_timesteps (bool, optional): If True, only the last timesteps of each object, that is the time steps after entering the domain, are selected. Defaults to False.

        Returns:
            ObjectContainer: Selected Object Container
        """
        if not isinstance(domain, Domain):
            raise TypeError("domain must be of type {type(Domain)}")

        if not isinstance(type_, str):
            raise TypeError("type_ must be a string")
        if type_ not in ["origin", "end", "anytime"]:
            raise ValueError("type_ must be one of 'origin', 'end' or 'anytime'")

        if not isinstance(domain_frac, float):
            raise TypeError("domain_frac must be a float")

        if domain_frac < 0 or domain_frac > 1:
            raise ValueError("domain_frac must be between 0 and 1")

        if not isinstance(select_last_timesteps, bool):
            raise TypeError("select_last_timesteps must be a boolean")



        if type_ == "origin":
            return ObjectContainer([x for x in self if x.get.regular_track[0] in domain])
        elif type_ == "end":
            return ObjectContainer([x for x in self if x.get.regular_track[-1] in domain])
        elif type_ == "anytime":
            if domain_frac or object_frac:
                if not domain_frac:
                    raise ValueError("domain_frac must be set if object_frac has been set")
                if not object_frac:
                    raise ValueError("object_frac must be set if domain_frac has been set")
                
                domain_grid_point_field = domain.get_gridpoint_field(regular=False)

                return ObjectContainer(
                    [
                        select_by_gridpoint_fraction(
                            x,
                            domain_grid_point_field,
                            domain_frac,
                            object_frac,
                            select_last_timesteps=select_last_timesteps,
                        )
                        for x in self
                        if select_by_gridpoint_fraction(
                            x,
                            domain_grid_point_field,
                            domain_frac,
                            object_frac,
                            select_last_timesteps=select_last_timesteps,
                        )
                        is not None
                    ]
                )

            return ObjectContainer([x for x in self if any(y in domain for y in x.get.regular_track)])

        else:
            raise ValueError("type_ has to be either 'origin', 'end' or 'anytime'")

    def sel_by_regime(self, regime_name: str) -> ObjectContainer:
        def get_idx(obj_, regime_name):
            list_ = list(obj_.get.clusters)
            idx = [i for i in range(len(list_)) if list_[i] == regime_name]
            return idx

        container = ObjectContainer([obj_.isel(times=get_idx(obj_, regime_name)) for obj_ in self])
        return ObjectContainer([x for x in container if x.times.size > 0])

    def get_index_by_id(self, obj_id: int) -> xr.Dataset:
        """Get the objects index in the ObjectContainer list based on its object id

        Args:
            obj_id (int): Object id

        """

        for ind, obj in enumerate(self):
            if int(obj_id) == int(obj.id_):
                return ind
            else:
                continue
             
