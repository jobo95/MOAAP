import cartopy.crs as ccrs
import matplotlib.path as mpath
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import sklearn


def cosine_cor(data, lat, lon):
    cos = np.sqrt(np.cos((np.pi / 180) * (np.abs(lat))))
    print(lon.size)
    t = 0
    for k in range(data.shape[1]):
        data[:, k] = data[:, k] * cos[t]

        if k >= (t + 1) * lon.size:
            t = t + 1

    return data


def inv_cosine_cor(data, lat, lon):
    cos = np.sqrt(np.cos((np.pi / 180) * (np.abs(lat))))

    t = 0
    for k in range(data.shape[1]):
        data[:, k] = data[:, k] / cos[t]

        if k >= (t + 1) * lon[:].size:
            t = t + 1

    return data


def reduce_dim(data, n_components=10):
    pca = sklearn.decomposition.PCA(n_components=n_components)
    pca.fit(data)
    data = pca.transform(data)

    return data


def sel_months(data_frame, num_month):

    if num_month[0] <= num_month[-1]:
        sel_data_frame = data_frame[
            (data_frame.index.month >= num_month[0])
            & (data_frame.index.month <= num_month[-1])
        ]
    else:
        sel_data_frame = data_frame[
            (data_frame.index.month >= num_month[0])
            | (data_frame.index.month <= num_month[-1])
        ]

    return sel_data_frame


def get_full_dates(num_month, year_start, year_end):

    #'month' name string for plots
    dic = {
        1: "J",
        2: "F",
        3: "M",
        4: "A",
        5: "M",
        6: "J",
        7: "J",
        8: "A",
        9: "S",
        10: "O",
        11: "N",
        12: "D",
    }
    mon_name = dic[num_month[0]]
    for j in range(len(num_month) - 1):
        mon_name = mon_name + dic[num_month[j + 1]]

    # create datetime
    dates = pd.date_range(str(year_start) + "-01", str(year_end) + "-12-31", freq="D")

    # remove leap year
    leap = []
    for each in dates:
        if each.month == 2 and each.day == 29:
            leap.append(each)

    return dates.drop(leap)


def plot_cluster(
    plot_dat,
    lat,
    lon,
    plot_size=(15, 9),
    plot_shape=[5, 1],
    cbar_size=1.0,
    cbar_ticks=[-20, -10, -5, -3, -2, -1, 1, 2, 3, 5, 10, 20],
    font_size=9,
    unit="hPa",
    color_lev=[-20, -10, -5, -3, -2, -1, 1, 2, 3, 5, 10, 20],
    square=False,
    cmap="seismic",
    set_title=True,
    titles=None,
):

    sort = np.arange(plot_shape[1])
    xx, yy = np.meshgrid(lon, lat)
    fig_cluster = plt.figure(figsize=plot_size)
    for j, val in enumerate(sort):
        ax = fig_cluster.add_subplot(
            plot_shape[0], plot_shape[1], j + 1, projection=ccrs.NorthPolarStereo()
        )

        theta = np.linspace(
            -np.radians(lon[0]) + np.pi, -np.radians(lon[-1] + 1.125) + np.pi, 100
        )
        center, radius = [0.5, 0.5], 0.5

        verts = np.vstack([np.sin(theta), np.cos(theta)]).T
        verts = np.vstack((verts, [0, 0]))
        circle = mpath.Path(verts * radius + center)
        if square is False:
            ax.set_boundary(circle, transform=ax.transAxes)
        if square is False:
            ax.set_extent([-180, 180, 90, 20], ccrs.PlateCarree())

        ax.coastlines()
        ax.gridlines()

        g = ax.contourf(
            xx,
            yy,
            plot_dat[val, :, :],
            cmap=cmap,
            levels=color_lev,
            extend="both",
            transform=ccrs.PlateCarree(),
        )
        cbar = plt.colorbar(
            g, ax=ax, ticks=cbar_ticks, orientation="horizontal", shrink=cbar_size
        )
        cbar.set_label(unit, size=font_size)
        cbar.ax.tick_params(labelsize=font_size)
        if set_title:
            ax.set_title(titles[j])
    plt.tight_layout()
    return fig_cluster
