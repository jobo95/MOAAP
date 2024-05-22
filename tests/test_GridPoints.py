import pytest
from src.GridPoints import *



def test_point_in_domain():
    p=RegularGridPoint(50,50)
    dom = Domain(north = 60, 
                 south=40, 
                 east=60,
                 west = 40)
    assert p in dom
    
    
def test_domain_contains():
    domain = Domain(north=10, south=-10, east=10, west=-10)
    in_point = RegularGridPoint(5, 5)
    out_point = RegularGridPoint(15, 15)
    assert in_point in domain
    assert out_point not in domain