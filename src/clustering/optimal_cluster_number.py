import numpy as np
import pandas as pd
from typing import List
from sklearn.cluster import KMeans
from sklearn.metrics import calinski_harabasz_score


def get_lag_autocorrelation(
    time_series_collection: np.ndarray, lag: int = 1
) -> List[float]:
    """Compute the  lagged autocorrelation of individual time series

    Args:
        time_series_collection (np.ndarray): NxM numpy array with M time series of length N
        lag (int, optional): time lag. Defaults to 1.

    Returns:
        List[float]: Lagged Autocorrelation for each time series
    """

    # Shift each time series by one time step
    shifted_series = np.roll(time_series_collection, lag, axis=0)

    # Compute the Pearson correlation coefficient between each original and shifted time series
    lag1_correlations = [
        np.corrcoef(time_series_collection[:, i], shifted_series[:, i])[0, 1]
        for i in range(time_series_collection.shape[1])
    ]

    return lag1_correlations


def create_AR1_timeseries(time_series_collection: np.ndarray) -> np.ndarray:
    """Create AR1 time series according to the individual imput time series

    Args:
        time_series_collection (np.ndarray): NxM numpy array with M time series of length N. For each individual time series a synthetic time series is created

    Returns:
        np.ndarray: collection of synthetic AR1 times series
    """
    var = np.var(time_series_collection, axis=0)
    mean = np.mean(time_series_collection, axis=0)
    lag1 = get_lag_autocorrelation(time_series_collection)
    std_noise = np.sqrt((1 - np.power(lag1, 2)) * var)

    x = np.zeros(time_series_collection.shape)
    for i in range(x.shape[0] - 1):
        x[i + 1, :] = mean + lag1 * (x[i, :] - mean) + np.random.normal(mean, std_noise)

    return x


def compute_synthetic_variance_ratios(
    time_series: np.ndarray, M: int, cluster_range: List[int]
) -> pd.DataFrame:
    """compute the kmeans clustering calinski_harabasz variance ratio for different  synthetic AR1 time series for different cluster numbers.

    Args:
        time_series (np.ndarray): NxM numpy array with M time series of length N
        M (int): Number of synthetic time series.
        cluster_range (List[int]): Range of cluster numbers to be considered

    Returns:
        pd.DataFrame: DataFrame with variance ratio score for the different cluster numbers and different synthetic time series.
    """

    df = pd.DataFrame(index=cluster_range)
    df.index.name = "cluster_number"

    df["original_time_series"] = np.nan
    for m in range(M):
        df[f"sample_{m}"] = np.nan

    #
    synthetic_var_ratio = np.empty((len(cluster_range), M))
    original_var_ratio = np.empty(len(cluster_range))

    for n, n_clusters in enumerate(cluster_range):
        print(f"{n_clusters=}")
        original_kmeans = KMeans(n_clusters=n_clusters, init="random").fit(time_series)
        df.loc[n_clusters, "original_time_series"] = calinski_harabasz_score(
            time_series, original_kmeans.labels_
        )  # original_kmeans.inertia_

        for m in range(M):
            synthetic_time_series = create_AR1_timeseries(time_series)
            kmeans = KMeans(n_clusters=n_clusters, init="random").fit(
                synthetic_time_series
            )
            df.loc[n_clusters, f"sample_{m}"] = calinski_harabasz_score(
                synthetic_time_series, kmeans.labels_
            )  # kmeans.inertia_

    return df
