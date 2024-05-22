import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy
from numpy.typing import ArrayLike
import numpy as np


def plot_unstructured_rotated_grid(
    lon,
    lat,
    z,
    index,
    fig,
    levels=[1, 2, 3, 5, 7, 9, 12, 15, 20, 25, 30],
    subplts=(4, 1),
    pad=0.01,
    title="",
    cbar_label=None,
    cmap="Blues",
):
    """
    Plot data field over the regional ICON domain using rotated coordinates.
    Functions uses tricontourf, so it requires (unordered) 1-D arrays as input.

    Args:
        lon (ArrayLike): 1-D array of size N with longitudes
        lat (ArrayLike): 1-D array of size N with latitudes
        z (ArrayLike): 1-D array of size N
        fig: Figure instance
        levels (int or array-like): Number and position of contour lines. Default to [1, 2, 3, 5,7,9,12,15,20,25,30].
        subplts (tuple): number/shape of subplots. Default to (4,1).
        pad (float): padding to align the colorbar
        index (int): index for subplots.
        title (bool, optional): Set title. Defaults to None.
        cbar_label (bool, optional): Add colorbar. Defaults to ''.
        cmap (str,optional). Colorscheme. Default is "Blues".
    """

    ###TODO origin hier nicht festsetzen#####
    pole_lon = 0
    pole_lat = 6.55
    crs_arctic = ccrs.RotatedPole(pole_longitude=pole_lon, pole_latitude=pole_lat)

    ax = fig.add_subplot(subplts[0], subplts[1], index + 1, projection=crs_arctic)

    # ax = plt.axes(projection=crs_arctic)

    ax.set_extent([-180, 180, 58, 90], crs=ccrs.PlateCarree())
    ax.add_feature(cartopy.feature.OCEAN, color="white", zorder=0)
    ax.add_feature(
        cartopy.feature.LAND,
        color="lightgray",
        zorder=0,
        linewidth=0.5,
        edgecolor="black",
    )
    ax.gridlines(
        linewidth=0.5,
        color="gray",
        xlocs=range(-180, 180, 45),
        ylocs=range(-90, 90, 10),
        linestyle=":",
    )  # draw_labels=True,
    ax.coastlines(linewidth=0.3, color="black")

    plot = plt.tricontourf(
        lon,
        lat,
        z,
        levels=levels,
        cmap=cmap,
        transform=crs_arctic,
    )
    cbar = plt.colorbar(plot, ax=ax, pad=pad)
    cbar.set_label(cbar_label)
    plt.title(title)

    # plt.show()
    
def plot_contourf_rotated_grid(
    lon,
    lat,
    z,
    index,
    fig,
    levels=[1, 2, 3, 5, 7, 9, 12, 15, 20, 25, 30],
    subplts=(4, 1),
    pad=0.01,
    title="",
    cbar_label=None,
    cmap="Blues",
):
    

    ###TODO origin hier nicht festsetzen#####
    pole_lon = 0
    pole_lat = 6.55
    crs_arctic = ccrs.RotatedPole(pole_longitude=pole_lon, pole_latitude=pole_lat)

    ax = fig.add_subplot(subplts[0], subplts[1], index + 1, projection=crs_arctic)

    # ax = plt.axes(projection=crs_arctic)
    xx,yy = np.meshgrid(lon, lat)
    ax.set_extent([-180, 180, 58, 90], crs=ccrs.PlateCarree())
    ax.add_feature(cartopy.feature.OCEAN, color="white", zorder=0)
    ax.add_feature(
        cartopy.feature.LAND,
        color="lightgray",
        zorder=0,
        linewidth=0.5,
        edgecolor="black",
    )
    ax.gridlines(
        linewidth=0.5,
        color="gray",
        xlocs=range(-180, 180, 45),
        ylocs=range(-90, 90, 10),
        linestyle=":",
    )  # draw_labels=True,
    ax.coastlines(linewidth=0.3, color="black")

    plot = plt.contourf(
        xx,
        yy,
        z,
        levels=levels,
        cmap=cmap,
        transform=crs_arctic,
    )
    cbar = plt.colorbar(plot, ax=ax, pad=pad)
    cbar.set_label(cbar_label)
    plt.title(title)

    # plt.show()
    
    

