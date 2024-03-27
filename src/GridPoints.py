import xarray as xr
import numpy as np
from abc import ABC



class GridPoint():
    ###### grid file anpassbar machen####

    input_field_grid = '/work/aa0238/a271093/data/input/IVT_85_percentiles_CNMR_control_3dx3dy.nc'
    grid_field = xr.open_dataset(input_field_grid, cache = True)
    
    regular_lat_grid = grid_field.lat.values
    regular_lon_grid = grid_field.lon.values
    
    rotated_lat_grid = xr.broadcast(grid_field.rlon, grid_field.rlat)[1].values.T
    rotated_lon_grid = xr.broadcast(grid_field.rlon, grid_field.rlat)[0].values.T



    def __init__(self, lat, lon):
        self.lat = lat
        self.lon = lon
        
    def __str__(self):
        return f'{self.__class__.__name__}(lat={self.lat}, lon={self.lon})'
    
    def __repr__(self):
        return f'{self.__class__.__name__}(lat={self.lat}, lon={self.lon})'

    

class RegularGridPoint(GridPoint):
    
    def __init__(self,lat,lon):
        if lon<-180 or lon > 180:
            raise ValueError("Longitude of RegularGridPoint object has to stay between -180 and 180.")
                             
        super().__init__(lat,lon)

    def to_rotated(self):
        lat_idx = np.argwhere(GridPoint.regular_lat_grid ==self.lat)[0,0]
        lon_idx = np.argwhere(GridPoint.regular_lon_grid ==self.lon)[0,1]
                
        lat = GridPoint.rotated_lat_grid[lat_idx,lon_idx]
        lon = GridPoint.rotated_lon_grid[lat_idx,lon_idx]

        return RotatedGridPoint(lat,lon)



class RotatedGridPoint(GridPoint):

    def to_regular(self):
        lat_idx = np.argwhere(GridPoint.rotated_lat_grid ==self.lat)[0,0]
        lon_idx = np.argwhere(GridPoint.rotated_lon_grid ==self.lon)[0,1]
                
        lat = GridPoint.regular_lat_grid[lat_idx,lon_idx]
        lon = GridPoint.regular_lon_grid[lat_idx,lon_idx]

        return RegularGridPoint(lat,lon)

class Domain():
    """
    not finished yet
    """
    
    def __init__(self, 
                 p_sw : RegularGridPoint,
                 p_nw : RegularGridPoint,
                 p_ne : RegularGridPoint,
                 p_se : RegularGridPoint,
                ):

        if (not isinstance(p_sw,RegularGridPoint) or
            not isinstance(p_nw,RegularGridPoint) or
            not isinstance(p_ne,RegularGridPoint) or
            not isinstance(p_se,RegularGridPoint)): 
            
            raise TypeError("Domain corners have to be instances of RegularGridPoint.")

        self.p_sw = p_sw
        self.p_nw = p_nw
        self.p_ne = p_ne
        self.p_se = p_se

    def __contains__(self, p : RegularGridPoint):
        #if not isinstance(p, RegularGridPoint):
        #    raise TypeError("Can only check if RegularGridPoint objects are located within the domain.")
        pass 
