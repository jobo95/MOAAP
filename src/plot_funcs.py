import cartopy
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import griddata

from src.Enumerations import Domains


def plot_unstructured_rotated_grid(
    lon,
    lat,
    z,
    index,
    fig,
    levels=[1, 2, 3, 5, 7, 9, 12, 15, 20, 25, 30],
    subplts=(4, 1),
    pad=0.01,
    use_contourf: bool = True,
    title="",
    cbar_label=None,
    cmap="Blues",
    plot_domains: dict[Domains, str] = None,
    cbar: bool = True,
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

    # TODO origin hier nicht festsetzen
    pole_lon = 0
    pole_lat = 6.55
    crs_arctic = ccrs.RotatedPole(pole_longitude=pole_lon, pole_latitude=pole_lat)

    ax = fig.add_subplot(
        subplts[0], subplts[1], index + 1, projection=ccrs.Orthographic(0, 90)
    )

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

    xx = lat.reshape((194, 193))
    yy = lon.reshape((194, 193))
    zz = z.reshape((194, 193))
    # plot = plt.contourf(
    #    xx,
    #    yy,
    #    zz,
    #    # levels=levels,
    #    cmap=cmap,
    #    transform=crs_arctic,
    # )

    if use_contourf:
        x = lon
        y = lat
        grid_x, grid_y = np.mgrid[
            np.min(lon) : np.max(lon) : 100j, np.min(lat) : np.max(lat) : 100j
        ]

        # Interpolate using 'linear' scheme
        # grid_z_linear = griddata((x, y), z, (grid_x, grid_y), method='linear')

        # Interpolate using 'cubic' scheme
        grid_z_cubic = griddata((x, y), z, (grid_x, grid_y), method="cubic")

        # Define a grid for interpolation
        grid_x, grid_y = np.mgrid[
            np.min(lon) : np.max(lon) : 100j, np.min(lat) : np.max(lat) : 100j
        ]
        plot = plt.contourf(
            grid_x,
            grid_y,
            grid_z_cubic,
            levels=levels,
            cmap=cmap,
            transform=crs_arctic,
        )
    else:
        plot = plt.tricontourf(
            lon,
            lat,
            z,
            levels=levels,
            cmap=cmap,
            transform=crs_arctic,
        )
    if plot_domains:
        for domain, color in plot_domains.items():
            d = domain.value
            plt.plot(
                np.linspace(d.west, d.west),
                np.linspace(d.south, d.north),
                transform=ccrs.PlateCarree(),
                color=color,
                linewidth=2,
            )
            plt.plot(
                np.linspace(d.west, d.east),
                np.linspace(d.north, d.north),
                transform=ccrs.PlateCarree(),
                color=color,
                linewidth=2,
            )
            plt.plot(
                np.linspace(d.east, d.east),
                np.linspace(d.north, d.south),
                transform=ccrs.PlateCarree(),
                color=color,
                linewidth=2,
            )
            plt.plot(
                np.linspace(d.east, d.west),
                np.linspace(d.south, d.south),
                transform=ccrs.PlateCarree(),
                color=color,
                linewidth=2,
            )

    plt.title(title)

    # if one_cbar:
    #    if (index + 1) % subplts[1] == 0:
    #        rows = subplts[0]

    #        cbar_width = 0.01
    #        cbar_padding = 0.05  # Abstand zwischen den Colorbars
    #        cbar_height = (1 - (rows + 1) * cbar_padding) / rows

    #        r = (index) // rows
    #        cbar_bottom = 1 - (r * (cbar_height + cbar_padding / 2))
    #        fig.subplots_adjust(right=0.8)
    #        print(f"{r=}", f"{cbar_bottom=}", f"{cbar_width=}", f"{cbar_height=}")
    #        print(f"{rows}", f"{index}")
    #        cbar_ax = fig.add_axes([0.81, cbar_bottom, cbar_width, cbar_height])
    #        cbar = plt.colorbar(plot, cax=cbar_ax)
    #        cbar.set_label(cbar_label)
    if cbar:
        cbar = plt.colorbar(plot, ax=ax, pad=pad)
        cbar.set_label(cbar_label)

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
    reglat=None,
    reglon=None,
    quiver_dat=None,
    quiver_thinning=5,
    quiver_scale=100,
    quiver_unit_scale=10,
):

    # TODO origin hier nicht festsetzen
    pole_lon = 0
    pole_lat = 6.55
    crs_arctic = ccrs.RotatedPole(pole_longitude=pole_lon, pole_latitude=pole_lat)

    ax = fig.add_subplot(
        subplts[0], subplts[1], index + 1, projection=ccrs.NorthPolarStereo()
    )

    # ax = plt.axes(projection=crs_arctic)
    xx, yy = np.meshgrid(lon, lat)
    # xx = lon
    # yy = lat

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

    plot = ax.contourf(
        xx,
        yy,
        z,
        levels=levels,
        cmap=cmap,
        transform=crs_arctic,
    )
    if quiver_dat is not None:
        plot_dat_u = quiver_dat[0].flatten()
        plot_dat_v = quiver_dat[1].flatten()

        step = quiver_thinning

        # Ausdünnen der Daten
        xx_thin = reglon.flatten()[::step]
        yy_thin = reglat.flatten()[::step]
        plot_dat_u_thin = plot_dat_u[::step]
        plot_dat_v_thin = plot_dat_v[::step]

        quiv = ax.quiver(
            xx_thin,
            yy_thin,
            plot_dat_u_thin,
            plot_dat_v_thin,
            units="width",
            scale=quiver_scale,
            headwidth=6,
            transform=ccrs.PlateCarree(),
            color="black",
        )
        ax.quiverkey(
            quiv,
            0.95,
            1.06,
            quiver_unit_scale,
            str(quiver_unit_scale) + r"$ \frac{kg}{m \cdot s}$",
            labelpos="E",
            fontproperties={"size": 10},
        )

    cbar = plt.colorbar(plot, ax=ax, pad=pad)
    cbar.set_label(cbar_label)
    plt.title(title)

    # plt.show()


def plot_tracks_rotated_grid(
    tracks,
    fig,
    index,
    levels=[1, 2, 3, 4, 5],
    title=None,
    cbar_label=None,
    subplts=(4, 1),
    plot_domains: dict[str, Domains] = {},
):

    pole_lon = 0
    pole_lat = 6.55
    crs_arctic = ccrs.RotatedPole(pole_longitude=pole_lon, pole_latitude=pole_lat)

    ax = fig.add_subplot(
        subplts[0], subplts[1], index + 1, projection=ccrs.Orthographic(0, 90)
    )

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

    for track in tracks:
        lons = [x.lon for x in track]
        lats = [x.lat for x in track]

        ax.plot(lons, lats, lw=1, transform=crs_arctic)
        ax.plot(lons, lats, marker="o", markersize=1, transform=crs_arctic)

    if plot_domains:
        for domain, color in plot_domains.items():
            d = domain.value
            plt.plot(
                np.linspace(d.west, d.west),
                np.linspace(d.south, d.north),
                transform=ccrs.PlateCarree(),
                color=color,
                linewidth=2,
            )
            plt.plot(
                np.linspace(d.west, d.east),
                np.linspace(d.north, d.north),
                transform=ccrs.PlateCarree(),
                color=color,
                linewidth=2,
            )
            plt.plot(
                np.linspace(d.east, d.east),
                np.linspace(d.north, d.south),
                transform=ccrs.PlateCarree(),
                color=color,
                linewidth=2,
            )
            plt.plot(
                np.linspace(d.east, d.west),
                np.linspace(d.south, d.south),
                transform=ccrs.PlateCarree(),
                color=color,
                linewidth=2,
            )


