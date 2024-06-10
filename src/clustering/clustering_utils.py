
import numpy as np
import sklearn
import netCDF4
import pandas as pd
import matplotlib.tri as tri
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.path as mpath
import matplotlib.patches as mpatches
import xarray as xr
from src.utils import load_pkl,save_as_pkl

def cosine_cor(data,lat,lon):
    cos = np.sqrt(np.cos((np.pi/180)*(np.abs(lat))))
    t = 0
    for k in range(data.shape[1]):
        data[:, k] = data[:, k]*cos[t]

        if k >= (t + 1)*lon.size:
            t = t + 1
    return data
            
            
def inv_cosine_cor(data,lat,lon):
    cos = np.sqrt(np.cos((np.pi/180)*(np.abs(lat))))
    
    t = 0
    for k in range(data.shape[1]):
        data[:,k] = data[:,k]/cos[t]

        if k >= (t + 1)*lon[:].size:
            t = t + 1
    return data

def load_clustering_data(path_in:str, file_name:str):
    data_xr =xr.load_dataset(path_in+file_name)
    data_aux = np.squeeze(data_xr.zg.values)

    data_ar = np.reshape(data_aux,(data_aux.shape[0], data_aux.shape[1]*data_aux.shape[2])) 
    
    lat = data_xr.lat.values
    lon = data_xr.lon.values
    time_frame = data_xr.time.values
    
    return lat,lon,time_frame,data_ar


def plot_cluster(plot_dat,lat,lon,plot_size=(15,9),plot_shape=[5,1],cbar_size=1.0,cbar_ticks=[-20, -10, -5, -3, -2, -1, 1, 2, 3, 5, 10, 20],font_size=9,unit='hPa',color_lev = [-20, -10, -5, -3, -2, -1, 1, 2, 3, 5, 10, 20],square=False,cmap='seismic',set_title=True,titles = None):
    extent=[lon[0],lon[-1],90,lat[-1]]
    
    sort = np.arange(plot_shape[1])
    xx,yy = np.meshgrid(lon,lat)
    fig_cluster = plt.figure(figsize = plot_size)
    for j, val in enumerate(sort):
        ax = fig_cluster.add_subplot(plot_shape[0],plot_shape[1],j+1,projection=ccrs.NorthPolarStereo())
        
    
        
        theta = np.linspace(-np.radians(lon[0])+np.pi, -np.radians(lon[-1]+1.125)+np.pi, 100)
        center, radius = [0.5, 0.5], 0.5
    
        verts = np.vstack([np.sin(theta), np.cos(theta)]).T
        verts = np.vstack((verts,[0,0]))
        circle = mpath.Path(verts * radius + center)
        if square is False:
            ax.set_boundary(circle, transform=ax.transAxes)
        if square is False:
            ax.set_extent([-180, 180, 90, 20], ccrs.PlateCarree())

        ax.coastlines()
        ax.gridlines()
        
        g = ax.contourf(xx, yy, plot_dat[val,:,:],cmap=cmap,levels=color_lev,extend='both', transform=ccrs.PlateCarree())
        cbar = plt.colorbar(g,
                            ax=ax,
                            ticks=cbar_ticks,
                            orientation="horizontal",
                            shrink=cbar_size)
        cbar.set_label(unit,size=font_size)
        cbar.ax.tick_params(labelsize=font_size)
        if set_title == True:
            ax.set_title(titles[j])
    plt.tight_layout()
    return (fig_cluster)



def plot_cluster_3D(plot_dat,lat,lon,plot_size=(15,9),plot_shape=[5,1],cbar_size=1.0,cbar_ticks=[-20, -10, -5, -3, -2, -1, 1, 2, 3, 5, 10, 20],font_size=9,unit='hPa',color_lev = [-20, -10, -5, -3, -2, -1, 1, 2, 3, 5, 10, 20],titles = None,sort=None,pad=0.15,Pacific=False):
    extent=[np.min(lon),np.max(lon),90,np.min(lat)]
    import warnings 

    xx,yy = np.meshgrid(lon,lat)
    warnings.filterwarnings('ignore')
    
    if sort == None:
        sort = np.arange(plot_shape[1])
    else:
        sort = sort
    #sort=np.arange(36)
    if Pacific is True:
        central_longitude=180
        lon_b_down=-90
        lon_b_up =90
    else:
        central_longitude=0
    
    fig_cluster = plt.figure(figsize = plot_size,dpi=200)
    for j, val in enumerate(sort):
        
        #ax = fig_cluster.add_subplot(plot_shape[0],plot_shape[1],j+1,projection=ccrs.NorthPolarStereo(central_longitude=central_longitude))
        ax = fig_cluster.add_subplot(plot_shape[0],plot_shape[1],j+1,projection=ccrs.Orthographic(central_longitude=0,central_latitude=55))
        
    

        ax.add_feature(cfeature.OCEAN, zorder=0)
        ax.add_feature(cfeature.LAND, zorder=0,color="bisque", edgecolor='black')

        
        #ax.set_title("EOF "+str(j+1)+"\n "+str(titles[j])+"%",size=font_size*2.6,fontweight="bold")
        ax.set_title(titles[j],size=font_size)
        ax.coastlines(linewidth=0.5,color='black',resolution='50m')
        #ax.gridlines(zorder=4)
        ax.set_global()
        g = ax.contourf(xx, yy, plot_dat[val,:,:],cmap='RdBu_r',levels=color_lev, extend='both',transform=ccrs.PlateCarree())
        f = ax.contour(xx, yy, plot_dat[val,:,:],colors="grey",levels=color_lev, transform=ccrs.PlateCarree(),linewidths=1)

        cbar = plt.colorbar(g,
                            ax=ax,
                            ticks=cbar_ticks,
                            orientation="horizontal",
                            shrink=cbar_size)
        cbar.set_label(unit,size=font_size)
        cbar.ax.tick_params(labelsize=font_size)

        lat_corners = np.array([20,88,88,20])
        lon_corners = np.array([ -90, -90,90, 90])
        poly_corners = np.zeros((len(lat_corners), 2), np.float64)
        poly_corners[:,0] = lon_corners
        poly_corners[:,1] = lat_corners

        poly = mpatches.Polygon(poly_corners, closed=True, ec='r', fill=False, lw=0.3, transform=ccrs.PlateCarree())
        #ax.add_patch(poly)
        path1_lon=np.ones(100)*lon_corners[0]
        path1_lat=np.linspace(lat_corners[0],lat_corners[1],100)

        path2_lat=np.ones(100)*lat_corners[1]
        path2_lon=np.linspace(lon_corners[1],lon_corners[2],100)

        path3_lon=np.ones(100)*lon_corners[2]
        path3_lat=np.linspace(lat_corners[2],lat_corners[3],100)

        path4_lat=np.ones(100)*lat_corners[3]
        path4_lon=np.linspace(lon_corners[3],lon_corners[0],100)

        import itertools
        path_lat = list(itertools.chain(path1_lat,path2_lat,path3_lat,path4_lat))
        path_lon = list(itertools.chain(path1_lon,path2_lon,path3_lon,path4_lon))


        plt.plot(path_lon,path_lat,linewidth=1, transform=ccrs.PlateCarree(),color='black')
    #plt.tight_layout()
    return (fig_cluster)