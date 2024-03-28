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


class TrackingDataLoader():

    scratch_path = '/work/aa0238/a271093/scratch/'

    def __init__(self, variable, path, start_date = None, end_date=None, suffix ='', file_type = 'ncz'):
        self._variable = variable
        self._path = path
        self._start_date = start_date
        self._end_date = end_date
        self._suffix = suffix
        self._file_type = file_type

    @property
    def start_date(self):
        if not self._start_date:
            raise AttributeError("start_date has to be set.")
        return self._start_date

    @start_date.setter
    def start_date(self,date):
        if not isinstance(date,datetime):
            raise TypeError("start_date has to be a datetime.datetime object")
        self._start_date = date   

    @property
    def end_date(self):
        if not self._end_date:
            raise AttributeError("end_date has to be set.")
        return self._end_date

    @end_date.setter
    def end_date(self,date):
        if not isinstance(date,datetime):
            raise TypeError("end_date has to be a datetime.datetime object")
        self._end_date = date   

    @property
    def year_start(self):
        return self._start_date.year

    @property
    def year_end(self):
        return self._end_date.year

    @property
    def path_var(self):
        return f'{self._path}{self._variable}/'

    @property
    def filename_year1(self):
        return f'{self._variable}_{self.year_start}010100-{self.year_start}123123_{self._suffix}{self._file_type}'

    @property
    def filename_year2(self):
        return f'{self._variable}_{self.year_end}010100-{self.year_end}123123_{self._suffix}{self._file_type}'

    @property
    def filename_merged(self):
        return f'merged{self._variable}_{self.year_start}_{self.year_end}_{self._suffix}{self._file_type}'

    def load_datasets(self, rm_nc=True):
        if self.year_start < self.year_end:
            self.merge_ncfiles()
            filename = self.filename_merged
            path = self.scratch_path
        else:
            filename = self.filename_year1
            path = self.path_var

        ds = xr.open_dataset(path+filename)

        if rm_nc:
            os.remove(self.scratch_path+self.filename_merged)

        ds_sel = ds.sel(time=self._create_seltime_array(ds))
        del (ds)

        return ds_sel

    def _create_seltime_array(self, ds):
        time = self._create_time_array(ds)
        self.time_sel = time[(time > self.start_date) &
                             (time < self.end_date)]

        return self.time_sel

    @staticmethod
    def _create_time_array(ds):

        return np.array(pd.DataFrame(ds.time.values, columns=['Datetime'])['Datetime'].values.astype('datetime64[s]').tolist())

    def merge_ncfiles(self):

        if not os.path.exists(f'{self.scratch_path}{self.filename_merged}'):

            cdo = Cdo()

            print(
                f'Mergetime {self.path_var+self.filename_year1} {self.path_var+self.filename_year2}  {self.scratch_path}{self.filename_merged}')

            cdo.mergetime(input=f'{self.path_var+self.filename_year1} {self.path_var+self.filename_year2}',
                          output=f'{self.scratch_path}{self.filename_merged}')
