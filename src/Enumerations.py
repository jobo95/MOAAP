from enum import Enum, IntEnum
from src.GridPoints import Domain
from src.Experiments_infos import *


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
    
class Experiments(Enum):
    ICON_CNRM_CONTROL = ICON_CNRM_CONTROL
    ICON_NORESM_CONTROL = ICON_NorESM_CONTROL
    ICON_CNRM_SSP = ICON_CNRM_SSP
    ICON_NORESM_SSP = ICON_NorESM_SSP #ICON_CNRM_EXP = ICON_CNRM_CONTROL
    ERA5 = ERA5

    def __getitem__(self, index):
        return self._value_[index]

class Domains(Enum):
    NORTH_ATLANTIC = Domain(north=60, south=40, east=0, west=-60)
    NORTH_PACIFIC = Domain(north=60, south=40, east=-160, west=160)
