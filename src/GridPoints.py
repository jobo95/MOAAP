from __future__ import annotations

from abc import ABC, abstractmethod

import numpy as np
import xarray as xr


class GridPoint(ABC):
    """
    Base class for grid points.
    """

    input_field_grid = (
        "/work/aa0238/a271093/data/input/IVT_85_percentiles_CNMR_control_3dx3dy.nc"
    )

    grid_field = xr.open_dataset(input_field_grid, cache=True)

    # lat and lon array of regular coordinates
    regular_lat_grid = grid_field.lat.values
    regular_lon_grid = grid_field.lon.values

    # corresponding lat and lon array of rotated coordinates
    rotated_lat_grid = xr.broadcast(grid_field.rlon, grid_field.rlat)[1].values.T
    rotated_lon_grid = xr.broadcast(grid_field.rlon, grid_field.rlat)[0].values.T

    def __new__(cls, lat, lon):
        """
        Forbid creation of GridPoint instances and check whether some Grid point instance has already been created and exists in memory
        """

        if cls is GridPoint:
            raise TypeError(
                "Can only create Regular-or Rotated Gridpoint instances, no instances of the GridPoint parent class."
            )

        coord = (lat, lon)
        if coord in cls._instances:
            return cls._instances[coord]
        else:
            instance = super().__new__(cls)
            cls._instances[coord] = instance
            return instance

    def __getnewargs__(self):
        return self.lat, self.lon

    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon

    def __hash__(self) -> int:
        return hash((self.lat, self.lon))

    def __eq__(self, other):
        return self.lat == other.lat and self.lon == other.lon

    def __str__(self):
        return f"{self.__class__.__name__}(lat={self.lat}, lon={self.lon})"

    def __repr__(self):
        return f"{self.__class__.__name__}(lat={self.lat}, lon={self.lon})"

    @abstractmethod
    def get_all_gridpoints(cls) -> list[GridPoint]:
        pass


class RegularGridPoint(GridPoint):
    """
    Class that represents grid points in a regular lon-lat coordinate system.
    """

    _instances = {}

    def __init__(self, lat, lon):

        if lon < -180 or lon > 180:
            raise ValueError(
                "Longitude of RegularGridPoint object has to stay between -180 and 180."
            )
        super().__init__(lat, lon)

    @classmethod
    def get_all_gridpoints(cls) -> list[RegularGridPoint]:
        lats, lons = cls.regular_lat_grid.flatten(), cls.regular_lon_grid.flatten()
        gridpoint_ls = [RegularGridPoint(lat, lon) for lat, lon in zip(lats, lons)]
        return gridpoint_ls

    def to_rotated(self) -> RotatedGridPoint:
        """Convert to rotated Gridpoint

        Returns:
            RotatedGridPoint: Corresponding rotated grid point instance
        """
        lat_idx = np.argwhere(GridPoint.regular_lat_grid == self.lat)[0, 0]
        lon_idx = np.argwhere(GridPoint.regular_lon_grid == self.lon)[0, 1]

        lat = GridPoint.rotated_lat_grid[lat_idx, lon_idx]
        lon = GridPoint.rotated_lon_grid[lat_idx, lon_idx]

        # crs_target=ccrs.RotatedPole(pole_longitude=0, pole_latitude=6.55)
        # crs_source=ccrs.PlateCarree()
        # lon,lat = crs_target.transform_point(self.lon, self.lat, src_crs=crs_source)
        return RotatedGridPoint(lat, lon)


class RotatedGridPoint(GridPoint):
    """
    Class that represents grid points in a rotated coordinate system.
    """

    _instances = {}

    @classmethod
    def get_all_gridpoints(cls) -> list[RotatedGridPoint]:
        lats, lons = cls.rotated_lat_grid.flatten(), cls.rotated_lon_grid.flatten()
        gridpoint_ls = [RotatedGridPoint(lat, lon) for lat, lon in zip(lats, lons)]
        return gridpoint_ls

    def to_regular(self) -> RegularGridPoint:
        """Convert to regular Gridpoint

        Returns:
            RegularGridPoint: Corresponding regular grid point instance
        """

        lat_idx = np.argwhere(GridPoint.rotated_lat_grid == self.lat)[0, 0]
        lon_idx = np.argwhere(GridPoint.rotated_lon_grid == self.lon)[0, 1]

        lat = GridPoint.regular_lat_grid[lat_idx, lon_idx]
        lon = GridPoint.regular_lon_grid[lat_idx, lon_idx]

        # crs_source=ccrs.RotatedPole(pole_longitude=0, pole_latitude=6.55)
        # crs_target=ccrs.PlateCarree()
        # lon,lat = crs_target.transform_point(self.lon, self.lat, src_crs=crs_source)
        return RegularGridPoint(lat, lon)


class Domain:
    def __init__(
        self,
        north: float,
        south: float,
        east: float,
        west: float,
    ):

        self.south = south
        self.north = north
        self.east = east
        self.west = west

    def __contains__(self, p: RegularGridPoint):
        """
        Check if RegularGridPoint is in Domain ("Gridpoint in Domain" syntax)
        """

        if not isinstance(p, RegularGridPoint):
            raise TypeError(
                "Can only check if RegularGridPoint objects are located within the domain."
            )
        if self.east > self.west:
            return (
                p.lat > self.south
                and p.lat < self.north
                and p.lon > self.west
                and p.lon < self.east
            )

        else:
            return (
                p.lat > self.south
                and p.lat < self.north
                and abs(p.lon) > self.west
                and abs(p.lon) > self.east
            )

    def get_gridpoint_field(self, regular: bool = True) -> list[GridPoint]:
        """
        Get all gridpoints that are in the specific domain

        Args:
            regular (bool, optional): If true return regular coordinates, else Rotated Coordinates. Defaults to True.

        Returns:
            list[GridPoint]: List of gridpoints inside the domain
        """
        gridpoints = RegularGridPoint.get_all_gridpoints()

        if regular:
            return [
                gridpoint for gridpoint in gridpoints if self.__contains__(gridpoint)
            ]

        return [
            gridpoint.to_rotated()
            for gridpoint in gridpoints
            if self.__contains__(gridpoint)
        ]


def get_Gridpoint_field(key, dict_):

    lat_idx_slice = dict_[key]["lat_idx_slice"]
    lon_idx_slice = dict_[key]["lon_idx_slice"]

    lat_slice = GridPoint.rotated_lat_grid[lat_idx_slice, lon_idx_slice]
    lon_slice = GridPoint.rotated_lon_grid[lat_idx_slice, lon_idx_slice]

    indices = np.argwhere(~np.isnan(dict_[key]["data_slice"]))
    time_steps = np.unique(indices[:, 0])

    gridpoint_ls = []
    for tstep in time_steps:
        idx = indices[indices[:, 0] == tstep][:, 1:]

        sub_ls_lat = [lat_slice[tuple(x)] for x in idx]
        sub_ls_lon = [lon_slice[tuple(x)] for x in idx]

        sub_gridpoint_ls = [
            RotatedGridPoint(lat, lon) for lat, lon in zip(sub_ls_lat, sub_ls_lon)
        ]

        gridpoint_ls.append(sub_gridpoint_ls)
    return np.array(gridpoint_ls, dtype="object")
    
# @measure_time_func_lines
def select_by_gridpoint_fraction(
    obj: xr.Dataset,
    domain_grid_point_field: list[RegularGridPoint],
    domain_fraction: float = 0.5,
    object_fraction: float = 0.8,
    select_last_timesteps: bool = False,
    step: int = 1,
) -> xr.Dataset:
    """Select only those objects that, at  any time step, cover a certain fraction of the domain OR whose overall object size lies within a certain fraction of the domain.

    Args:
        obj (xr.Dataset): IVT object
        domain_grid_point_field (list[RegularGridPoint]): list of regular grid points that lie within the domain
        domain_fraction (float, optional): Fraction of domain that has to be covered by object. Defaults to 0.5. If 0 all objects are selected.
        object_fraction (float, optional): Fraction of object that has to lie inside the domain. Defaults to 0.8.
        select_last_timesteps (bool, optional): If an object covers the domains at timestep i, then select only the i-th to the last timesteps of the object (if set to True). Defaults to False.
        step (int, optional): . Defaults to 1.

    Returns:
        - xr.Dataset: selected objects or None if condition not met
    """
    points_domain = set(domain_grid_point_field)
    points_domain_length = len(points_domain)
    for i, points in enumerate(obj.gridpoints.values[::step]):
        sel_points = set(points).intersection(points_domain)

        # fraction of domain covered by  object grid points
        frac1 = len(sel_points) / points_domain_length

        # fraction of object grid points that are in the domain
        frac2 = len(sel_points) / len(points)

        if frac1 >= domain_fraction or frac2 >= object_fraction:
            if select_last_timesteps:
                return obj.isel(times=slice(i * step, None))
            return obj

