from abc import ABC
import numpy as np
class Variable(ABC):
    _instances = {}
    

    def __new__(cls, value):
        
        value =cls._find_closest_value_in_bins(value, cls.bins)
        # Wenn eine Instanz für den Wert bereits existiert, wird diese zurückgegeben
        if value in cls._instances:
            return cls._instances[value]
        # Ansonsten wird eine neue Instanz erzeugt und gespeichert
        instance = super().__new__(cls)
        cls._instances[value] = instance
        return instance
    
    def __init__(self, value) -> None:
        self.value = self._find_closest_value_in_bins(value, self.bins)
    
    def __str__(self) -> str:
        return f"{self.__class__.__name__}(value={self.value})"
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(value={self.value})"
    
    def __hash__(self) -> int:
        return hash(self.value)
    
    def __getnewargs__(self):
        return self.value
    @classmethod
    def _find_closest_value_in_bins(cls, value:float, bins:set)-> int:
        return min(bins, key=lambda num: abs(num - value))
    


class IWV(Variable):
    max_ = 500
    min_= 0
    bins = set(np.arange(min_, max_ + 1, 5))

    