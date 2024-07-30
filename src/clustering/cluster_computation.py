import os

import numpy as np
import pandas as pd
from sklearn import cluster, decomposition

from src.clustering.clustering_utils import (cosine_cor, inv_cosine_cor,
                                             load_clustering_data)
from src.Enumerations import Experiments, Season
from src.utils import load_pkl, save_as_pkl


def compute_and_save_cluster(
    EXP: Experiments,
    season: Season,
    num_cluster: int,
    back_trafo_centroids: bool = True,
    pca_ref: str = None,
    kmeans_ref: str = None,
    num_iter: int = 10,
    n_components: int = 20,
    level: int = 70000,
    save_pca: bool = False,
    save_kmeans: bool = False,
    save_BMUs: bool = False,
    save_centroids: bool = False,
    cluster_names_dict: dict = {},
    BMU_projection_flag: str = "",
) -> dict[str, np.ndarray]:
    """Compute and/or save circulation regimes with kmeans.

    Args:
        EXP (Experiments): Experiment Type
        num_cluster (int, optional): Number of clusters if kmeans is fitted. Defaults to 4.
        back_trafo_centroids (bool, optional): Backtransform cluster centroids via inverse cosine and pca transformation. Defaults to True.
        pca_ref (str, optional): File pointing to a saved reference PCA object that is used for  dimensionality reduction. Defaults to None.
        kmeans_ref (str, optional): File pointing to a saved reference kmeans object that is used for cluster assignment. Defaults to None.
        num_iter (int, optional): Number of kmeans inetilizations if fitted. Defaults to 10.
        n_components (int, optional): Number of PCs if pca is fitted. Defaults to 20.
        level (int, optional): Geopotential heigth level. Defaults to 70000.
        save_pca (bool, optional): If True, save fitted    pca object. Defaults to False.
        save_kmeans (bool, optional): If True, save fitted kmeans object. Defaults to False.
        save_BMUs (bool, optional): If True, save BMU dataframe. Defaults to False.
        save_centroids (bool, optional): If true, save cluster centroids. Defaults to False.
        cluster_names_dict (dict, optional): Dictionary that describes which clustering label corresponds to which regime name.  Defaults to {}.
        BMU_projection_flag (str, optional): Additional suffix for the BMU csv file output. Defaults to "".

    Returns:
        dict[str, np.ndarray]: dictionary containing values for cluster centers, BMUs, lat and lon
    """

    exp = EXP.value
    season = season
    year_start = exp.year_start
    year_end = exp.year_end
    path_in = exp.clustering_data_path
    path_out = os.path.dirname(path_in.rstrip("/")) + "/"
    file_name = f"{exp.exp_name}_gph{level}_{year_start}_{year_end}_reglonlat_-90_90_20_88_1deg_{season.name}_fldmean_detrend_del29feb_aac.nc"
    print(30 * "#")
    print(exp.exp_name)
    print(30 * "#")
    n_components = n_components  # dimensionality of reduced phase space

    # kmeans parameter#
    num_cluster = num_cluster
    num_iter = num_iter  # initiate algorithm n_times randomly and pick best result

    lat, lon, time_frame, data_ar = load_clustering_data(path_in, file_name)

    data_ar = cosine_cor(data_ar, lat, lon)

    # dimensionality reduction ############

    if pca_ref:
        fitted_pca = load_pkl(pca_ref)
        print(f"loaded pca {pca_ref}")

    else:
        pca = decomposition.PCA(n_components=n_components)
        fitted_pca = pca.fit(data_ar)
        print("fitted new pca")

    data_ar = fitted_pca.transform(data_ar)

    if save_pca:
        save_pca_file = (
            f"{path_out}regime_output/PCA/PCA_{file_name[0:-3]}_{n_components}PCs"
        )
        save_as_pkl(fitted_pca, save_pca_file)
        print(f"saved pca {save_pca_file}")

    # kmeans

    if kmeans_ref:
        fitted_means = load_pkl(kmeans_ref)
        print(f"loaded kmeans {kmeans_ref}")

    else:
        means = cluster.KMeans(
            n_clusters=num_cluster,
            n_init=num_iter,
            max_iter=900,
            random_state=42,
            algorithm="lloyd",
        )

        fitted_means = means.fit(data_ar)
        print("fitted new kmeans")

    cluster_centers = fitted_means.cluster_centers_
    BMU = fitted_means.predict(data_ar)

    if save_kmeans:
        save_kmeans_file = f"{path_out}regime_output/Kmeans/Kmeans_{file_name[0:-3]}_{n_components}PCs_{num_cluster}clusters"
        save_as_pkl(fitted_means, save_kmeans_file)
        print(f"saved kmeans {save_kmeans_file}")

    if back_trafo_centroids:
        cluster_centers = fitted_pca.inverse_transform(cluster_centers)

        cluster_centers = inv_cosine_cor(cluster_centers, lat, lon)

    if save_BMUs:
        BMU_file = f"{path_out}regime_output/BMU/{file_name[0:-3]}_{n_components}PCs_{num_cluster}clusters{BMU_projection_flag}.csv"
        BMU_df = pd.DataFrame(BMU, index=time_frame)
        BMU_df.index.name = "time"
        BMU_df.columns = ["cluster_id"]
        if cluster_names_dict:
            BMU_df["cluster_name"] = BMU_df.apply(
                lambda row: cluster_names_dict[row["cluster_id"]], axis=1
            )
            print("added regime names to BMU Dataframe")
        BMU_df.to_csv(BMU_file)
        print(f"saved BMUs in {BMU_file}")

    if save_centroids:
        cluster_centers_file = f"{path_out}regime_output/centroids/Centroids_{file_name[0:-3]}_{n_components}PCs_{num_cluster}clusters"
        save_as_pkl(cluster_centers, cluster_centers_file)
        print(f"saved centroids in {cluster_centers_file}")

    dict_ = {
        "cluster_centers": cluster_centers,
        "BMU": BMU,
        "lat": lat,
        "lon": lon,
        "time_frame": time_frame,
        # "save_kmeans_file":save_kmeans_file
    }

    return dict_
