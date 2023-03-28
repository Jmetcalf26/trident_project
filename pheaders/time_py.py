import time as time_lib

def time(storage=None):
    if storage:
        storage.value = time_lib.time()
    return time_lib.time()
