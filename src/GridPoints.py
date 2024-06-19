from __future__ import annotations

import numpy as np
import xarray as xr


class GridPoint:
    """
    Parrent class for grid points.
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
