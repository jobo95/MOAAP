from enum import Enum, IntEnum

from src.Experiments_infos import (
    ERA5,
    ICON_CNRM_CONTROL,
    ICON_CNRM_SSP,
    ICON_ERA5,
    ICON_NorESM_CONTROL,
    ICON_NorESM_SSP,
)
from src.GridPoints import Domain


class Month(IntEnum):
    JANUARY = 1
    FEBRUARY = 2
    MARCH = 3
    APRIL = 4
    MAY = 5
    JUNE = 6
    JULY = 7
    AUGUST = 8
    SEPTEMBER = 9
    OCTOBER = 10
    NOVEMBER = 11
    DECEMBER = 12


class Season(Enum):
    DJF = (12, 1, 2)
    MAM = (3, 4, 5)
    JJA = (6, 7, 8)
    SON = (9, 10, 11)
    # ALL = (1,2,3,4,5,6,7,8,9,10,11,12)

    def __getitem__(self, index):
        return self._value_[index]


class GPH700_4Cluster(Enum):
    NAO_PLUS = "NAO+"
    NAO_MINUS = "NAO-"
    ATL_MINUS = "ATL-"
    SCAN = "SCAN"


class GPH700_5Cluster_DJF(Enum):
    NAO_PLUS = "NAO+"
    NAO_MINUS = "NAO-"
    ATL_MINUS = "ATL-"
    SCAN = "SCAN"
    DIP = "DIP"


class GPH700_5Cluster_MAM(Enum):
    NAO_PLUS = "SP-NAO+"
    NAO_MINUS = "SP-NAO-"
    ATL_MINUS = "SP-ATL+"
    SCAN = "SP-SCAN"
    DIP = "SP-DIP"


class Experiments(Enum):
    ICON_CNRM_CONTROL = ICON_CNRM_CONTROL
    ICON_NORESM_CONTROL = ICON_NorESM_CONTROL
    ICON_CNRM_SSP = ICON_CNRM_SSP
    ICON_NORESM_SSP = ICON_NorESM_SSP  # ICON_CNRM_EXP = ICON_CNRM_CONTROL
    ERA5 = ERA5
    ICON_ERA5 = ICON_ERA5

    def __getitem__(self, index):
        return self._value_[index]


class Domains(Enum):
    NORTH_ATLANTIC = Domain(north=70, south=50, east=0, west=-60)
    NORTH_PACIFIC = Domain(north=70, south=40, east=-160, west=140)
    CENTRAL_ARCTIC = Domain(north=90, south=85, east=180, west=-180)
    FRAM_STRAIT = Domain(north=81, south=77, east=10, west=-10)
    GREENLAND_SEA = Domain(north=80, south=75, east=10, west=-20)
