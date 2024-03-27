from enum import Enum, IntEnum


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
    WINTER = (12,1,2)
    SPRING = (3,4,5)
    SUMMER = (6,7,8)
    AUTUMN = (9,10,11)
    #ALL = (1,2,3,4,5,6,7,8,9,10,11,12)
                        
                        
    def __getitem__(self, index):
        return self._value_[index]
