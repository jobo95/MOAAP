import xarray as xr
from cdo import Cdo
import datetime
from itertools import product
from dateutil import relativedelta
import pickle
import os
import pandas as pd
import numpy as np
from datetime import datetime


class TrackingDataLoader:
    #####TODO Tracking DataLoader flexibler machen####
    """
    Class that loads and prepares input data for the MOAAP Tracking algorithm. Currently loads data in chunks of 7 months. (from January to August and from July to February respectively)
    Assumes that the input data are fiven in files that contain yearly data of the form:

    {path}/{variable}/{variable}_{year}010100-{year}23123_{suffix}{file_type},
    so for instance {path}/IVTu/IVTu_1986010100-1986123123_remapped_3x.nc

    If the dates of a data chunk range from 1.1-1.8, one single input file is simply loaded and the dates properly selected.
    As chunks with date ranging from 1.7-1.2 require data from two consecutive years, two yearly input files are first merged and accordingly the dates afterwards  properly selected.
    """

    scratch_path = "/work/aa0238/a271093/scratch/"

    def __init__(
        self,
        variable: str,
        path: str,
        start_date: datetime = None,
        end_date: datetime = None,
        suffix: str = "",
        file_type: str = "nc",
    ):
        """Initialize Tracking DataLoader

        Args:
            variable (str): Variable of intrest (e.g. IVTu)
            path (str): General data directory path.\n\n
            start_date (datetime, optional): Start date of Tracking data chunk. Defaults to None.
            end_date (datetime, optional): End date of Tracking data chunk. Defaults to None.
            suffix (str, optional): _description_. Defaults to "".
            file_type (str, optional): File Ending of input files. Defaults to "nc".
        """
        self._variable = variable
        self._path = path
        self._start_date = start_date
        self._end_date = end_date
        self._suffix = suffix
        self._file_type = file_type

    @property
    def start_date(self) -> datetime:
        """Set Start date of Tracking data chunk

        Raises:
            AttributeError: end_date has to be explicitly set.
        """
        if not self._start_date:
            raise AttributeError("start_date has to be set.")
        return self._start_date

    @start_date.setter
    def start_date(self, date: datetime):
        """Set start date of Tracking data chunk


        Args:
            date (datetime): start date

        Raises:
            TypeError: start date has to be of type datetime.datetime.
        """
        if not isinstance(date, datetime):
            raise TypeError("start_date has to be a datetime.datetime object")
        self._start_date = date

    @property
    def end_date(self) -> datetime:
        """End date of data chunk

        Raises:
            AttributeError: end_date has to be explicitly set.
        """
        if not self._end_date:
            raise AttributeError("end_date has to be set.")
        return self._end_date

    @end_date.setter
    def end_date(self, date: datetime):
        """Set end date of Tracking data chunk


        Args:
            date (datetime): end date

        Raises:
            TypeError: end date has to be of type datetime.datetime.
        """

        if not isinstance(date, datetime):
            raise TypeError("end_date has to be a datetime.datetime object")
        self._end_date = date

    @property
    def year_start(self) -> int:
        """
        Get start year of data chunk

        """
        return self._start_date.year

    @property
    def year_end(self):
        """
        Get end year of data chunk
        """
        return self._end_date.year

    @property
    def path_var(self):
        """
        Get directory path to variables' input files
        """
        return f"{self._path}{self._variable}/"

    @property
    def filename_year1(self):
        """
        Get filename of the first year.
        """
        return f"{self._variable}_{self.year_start}010100-{self.year_start}123123_{self._suffix}{self._file_type}"

    @property
    def filename_year2(self):
        """
        Get filename of the second year. Same as filename_year2 for date range (1.1-1.8)
        """
        return f"{self._variable}_{self.year_end}010100-{self.year_end}123123_{self._suffix}{self._file_type}"

    @property
    def filename_merged(self):
        """
        Get file name of merged netcdf file (only if date 1.7-1.2)
        """
        return f"merged{self._variable}_{self.year_start}_{self.year_end}_{self._suffix}{self._file_type}"

    def load_datasets(self, rm_nc=True) -> xr.Dataset:
        """Load

        Args:
            rm_nc (bool, optional): Remove merged netCDF4 files finally. Defaults to True.

        Returns:
            xr.Dataset: Dataset containing the input data for the Tracking algorithm, selected according to the specified data range
        """

        # if date range 1.7-1.2 merge netcdf input files of two consecutive years
        if self.year_start < self.year_end:
            self.merge_ncfiles()
            filename = self.filename_merged
            path = self.scratch_path

        # if date range 1.1-1.8 simply use one netcdf input file
        else:
            filename = self.filename_year1
            path = self.path_var

        ds = xr.open_dataset(path + filename)

        if rm_nc:
            os.remove(self.scratch_path + self.filename_merged)

        ds_sel = ds.sel(time=self._create_seltime_array(ds))
        del ds

        return ds_sel

    def _create_seltime_array(self, ds):
        time = self._create_time_array(ds)
        self.time_sel = time[(time > self.start_date) & (time < self.end_date)]

        return self.time_sel

    @staticmethod
    def _create_time_array(ds):

        return np.array(
            pd.DataFrame(ds.time.values, columns=["Datetime"])["Datetime"]
            .values.astype("datetime64[s]")
            .tolist()
        )

    def merge_ncfiles(self):
        """
        Merge netcdf files of two consecutive and save merged file in scratch path.
        """

        if not os.path.exists(f"{self.scratch_path}{self.filename_merged}"):

            cdo = Cdo()

            print(
                f"Mergetime {self.path_var+self.filename_year1} {self.path_var+self.filename_year2}  {self.scratch_path}{self.filename_merged}"
            )

            cdo.mergetime(
                input=f"{self.path_var+self.filename_year1} {self.path_var+self.filename_year2}",
                output=f"{self.scratch_path}{self.filename_merged}",
            )
