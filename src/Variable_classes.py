import functools
import math
import numbers


@functools.total_ordering
class Variable(numbers.Integral):
    """ 
    Custom class that rounds input to nearest integer and creates singelton object for each unique value.
    """
    ####TODO descriptor for fobridding value setting#####
    _instances = {}
    

    def __new__(cls, value):
        
        #value =cls._find_closest_value_in_bins(value, cls.bins)
        value =cls._round_to_int(value)
        # Wenn eine Instanz für den Wert bereits existiert, wird diese zurückgegeben
        if value in cls._instances:
            return cls._instances[value]
        # Ansonsten wird eine neue Instanz erzeugt und gespeichert
        instance = super().__new__(cls)
        cls._instances[value] = instance
        return instance
    
    def __init__(self, value) -> None:
        #self.value = self._find_closest_value_in_bins(value, self.bins)
        self.value =self._round_to_int(value)
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}(value={self.value})"
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(value={self.value})"
    
    def __hash__(self) -> int:
        return hash(self.value)
    
    def __getnewargs__(self):
        return (self.value,)
    
    @classmethod
    def _round_to_int(cls,value):
        return float(round(value))
    #@classmethod
    #def _find_closest_value_in_bins(cls, value:float, bins:set)-> int:
    #    return min(bins, key=lambda num: abs(num - value))
    

    def __int__(self):
        return self.value

    def __float__(self):
        return float(self.value)

    def __index__(self):
        return self.value

    def __ceil__(self):
        return self.__class__(math.ceil(self.value))

    def __floor__(self):
        return self.__class__(math.floor(self.value))

    def __round__(self, ndigits=None):
        return self.__class__(round(self.value, ndigits))

    def __trunc__(self):
        return self.__class__(math.trunc(self.value))

    def __pos__(self):
        return self.__class__(+self.value)

    def __neg__(self):
        return self.__class__(-self.value)

    def __abs__(self):
        return self.__class__(abs(self.value))

    # Arithmetische Operationen
    def __add__(self, other):
        if isinstance(other, Variable):
            other = other.value
        return self.__class__(self.value + other)

    def __sub__(self, other):
        if isinstance(other, Variable):
            other = other.value
        return self.__class__(self.value - other)

    def __mul__(self, other):
        if isinstance(other, Variable):
            other = other.value
        return self.__class__(self.value * other)

    def __floordiv__(self, other):
        if isinstance(other, Variable):
            other = other.value
        return self.__class__(self.value // other)

    def __truediv__(self, other):
        if isinstance(other, Variable):
            other = other.value
        return float(self.value) / other  # Echte Division, gibt float zurück

    def __mod__(self, other):
        if isinstance(other, Variable):
            other = other.value
        return self.__class__(self.value % other)

    def __pow__(self, other, modulo=None):
        if isinstance(other, Variable):
            other = other.value
        return self.__class__(pow(self.value, other, modulo))

    # Vergleichsoperationen
    def __eq__(self, other):
        if isinstance(other, Variable):
            other = other.value
        return self.value == other

    def __lt__(self, other):
        if isinstance(other, Variable):
            other = other.value
        return self.value < other

    def __le__(self, other):
        if isinstance(other, Variable):
            other = other.value
        return self.value <= other

    # Bitweise Operationen
    def __and__(self, other):
        if isinstance(other, Variable):
            other = other.value
        return self.__class__(self.value & other)

    def __or__(self, other):
        if isinstance(other, Variable):
            other = other.value
        return self.__class__(self.value | other)

    def __xor__(self, other):
        if isinstance(other, Variable):
            other = other.value
        return self.__class__(self.value ^ other)

    def __lshift__(self, other):
        if isinstance(other, Variable):
            other = other.value
        return self.__class__(self.value << other)

    def __rshift__(self, other):
        if isinstance(other, Variable):
            other = other.value
        return self.__class__(self.value >> other)

    def __invert__(self):
        return self.__class__(~self.value)

    # Reverse Operationen
    def __radd__(self, other):
        return self + other

    def __rsub__(self, other):
        return -self + other

    def __rmul__(self, other):
        return self * other

    def __rtruediv__(self, other):
        return float(other) / self.value

    def __rfloordiv__(self, other):
        return self.__class__(other // self.value)

    def __rmod__(self, other):
        return self.__class__(other % self.value)

    def __rpow__(self, other, modulo=None):
        return self.__class__(pow(other, self.value, modulo))

    def __rlshift__(self, other):
        return self.__class__(other << self.value)

    def __rrshift__(self, other):
        return self.__class__(other >> self.value)

    def __rand__(self, other):
        return self.__class__(other & self.value)

    def __ror__(self, other):
        return self.__class__(other | self.value)

    def __rxor__(self, other):
        return self.__class__(other ^ self.value)        
        
#class Variable2(int):
#    ####TODO descriptor for fobridding value setting#####
#    _instances = {}
#    
#
#    def __new__(cls, value):
#        
#        #value =cls._find_closest_value_in_bins(value, cls.bins)
#        value =cls._round_to_int(value)
#        # Wenn eine Instanz für den Wert bereits existiert, wird diese zurückgegeben
#        if value in cls._instances:
#            return cls._instances[value]
#        # Ansonsten wird eine neue Instanz erzeugt und gespeichert
#        instance = super().__new__(cls, value)
#        cls._instances[value] = instance
#        return instance
#    
#    
#    def __str__(self) -> str:
#        return f"{self.__class__.__name__}({super().__str__()})"
#    
#    def __repr__(self) -> str:
#        return f"{self.__class__.__name__}({super().__repr__()})"
#    
#    @classmethod
#    def _round_to_int(cls,value):
#        return float(round(value))
 
        

class IWV(Variable):
    pass

class IVT(Variable):
    pass

class IVTv(Variable):
    pass
class T2M(Variable):
    pass

