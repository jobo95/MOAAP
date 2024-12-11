from itertools import chain

import numpy as np
from numpy import ndarray
from sklearn.neighbors import KDTree

from src.GridPoints import RotatedGridPoint
from src.Objectcontainer import ObjectContainer
from timeit import default_timer as timer


def compute_history(object_container: ObjectContainer, threshold: float = 3) -> ObjectContainer:
    """Computes the splitting/merging history of all objects and adds it to the object_container. First, algorithm determines for start/end time of each reference object which other objects live  at the same time.
       Then the closest distance between all those objects and the reference object is calculated (in the rotated coordinate system) and all objects with distance less than threshold are filtered. From these filtered objects all objects that are smaller (total IVT)
       than the reference object are distributed and from these the object with the closest distance is finally choosen.
       !!! Assumes that grid points are evenly spaced!!!

    Args:
        object_container (ObjectContainer)
        threshold (float, optional): Distance threshold [°]. Defaults to 2.

    Returns:
        ObjectContainer: modified object container with history added
    """

    print("    compute history")
    object_container = create_empty_history(object_container)

    for type_ in ("start", "end"):
        if type_ == "start":
            all_objs = object_container.seltimesteps(slice(0, 1))

        if type_ == "end":
            all_objs = object_container.seltimesteps(slice(-1, None))

        start=0
        end = 0
        for i, obj in enumerate(all_objs):
            if i % 500 == 0:
                end = timer()
                print ("ellapsed time: ",end-start)
                start = timer()
                print (str(100*i/len(all_objs)/2.)+"%")
            objs_closest = {}

            time = obj.times
            if i % 50 == 0:
                objs_at_time_presel = object_container[i - 500 : i + 500]
            objs_at_time = objs_at_time_presel.sel_by_time(time.values[0])
       #     # objs_at_time =object_container.sel_by_time(time.values[0])
       #     # print (len(objs_at_time))
       
            for obj2 in objs_at_time:

                obj2 = obj2.sel(times=time)
                distance = calc_min_distance_between_objs(obj.gridpoints.values, obj2.gridpoints.values)
                if distance < threshold and distance != 0:
                    objs_closest[distance] = obj2

            if not objs_closest:
                continue
            objs_closest = {key: value for key, value in objs_closest.items() if value.total_IVT > obj.total_IVT}

            if not objs_closest:
                continue
            largest_closest_obj = objs_closest[min(objs_closest.keys())]

            obj_index = object_container.get_index_by_id(int(obj.id_))
            largest_closest_obj_index = object_container.get_index_by_id(int(largest_closest_obj.id_))

            object_container = edit_obj_history(
                object_container,
                obj_index,
                largest_closest_obj_index,
                time,
                type_=type_,
            )

    return object_container


def calc_min_distance_between_objs(p1: ndarray[list[RotatedGridPoint]], p2: ndarray[list[RotatedGridPoint]]) -> float:
    """Calculate the minimal distance between to Gridobject point clouds.

    Returns:
        float: Minimal distance
    """

    p1 = list(chain.from_iterable(p1))
    p2 = list(chain.from_iterable(p2))

    p1_lat = [x.lat for x in p1]
    p1_lon = [x.lon for x in p1]

    p2_lat = [x.lat for x in p2]
    p2_lon = [x.lon for x in p2]

    p1 = np.column_stack([p1_lat, p1_lon])
    p2 = np.column_stack([p2_lat, p2_lon])

    tree = KDTree(p1)
    (distances, _) = tree.query(p2, k=1)

    return distances.min()


def edit_obj_history(
    obj_container: ObjectContainer,
    obj_index: int,
    obj_close_index: int,
    time: np.datetime64,
    type_: str,
) -> ObjectContainer:
    """
    Modifiy the history of the reference and the closest object.

    Args:
        obj_container (ObjectContainer)
        obj_index (int): Index of reference object (not id!)
        obj_close_index (int): Index of closest object
        time (np.datetime64): time step
        type_ (str): start or end

    Returns:
        ObjectContainer: Modified object container
    """

    obj = obj_container[obj_index]
    obj_close = obj_container[obj_close_index]

    obj_id = int(obj.id_.values)
    obj_close_id = int(obj_close.id_.values)

    hist = obj.history
    hist_close = obj_close.history

    # print (f"{obj_id=}, {obj_close_id=}")

    if type_ == "start":

        hist.loc[{"times": time}] = obj_close_id
        hist_close.loc[{"times": time}] = -obj_id

    elif type_ == "end":

        hist.loc[{"times": time}] = -obj_close_id
        hist_close.loc[{"times": time}] = obj_id

    obj["history"] = hist
    obj_close["history"] = hist_close

    obj_container[obj_index] = obj
    obj_container[obj_close_index] = obj_close

    return obj_container


def create_empty_history(obj_container: ObjectContainer) -> ObjectContainer:
    """Create empty history with zeros for all objects

    Args:
        obj_container (ObjectContainer)

    Returns:
        ObjectContainer
    """
    for i in range(len(obj_container)):
        
        history = ("times", np.zeros(len(obj_container[i].times)).astype("int"))

        obj_container[i] = obj_container[i].assign(history=history)

    return obj_container
