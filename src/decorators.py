import time
from functools import wraps

# from line_profiler import LineProfiler


def measure_time_func(func):
    """
    Decorator that measures and prints the execution time of a function
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        print(f"Function {func.__name__} took {total_time:.4f} seconds")
        return result

    return wrapper


# def measure_time_func_lines(func):
#    """
#    Decorator that measures and prints the execution time of  each line in a function
#    """
#
#    @wraps(func)
#    def wrapper(*args, **kwargs):
#        profiler = LineProfiler()
#        profiler.add_function(func)
#        profiler.enable_by_count()
#
#        result = func(*args, **kwargs)
#
#        profiler.disable_by_count()
#        profiler.print_stats()
#
#        return result
#
#    return wrapper
#
