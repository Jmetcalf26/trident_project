import random
from helper_classes import *

RAND_MAX = [2**32-1]
_rng = random.Random(0)

def srand(seed):
    _rng.seed(seed[0])
def rand():
    return _rng.randrange(RAND_MAX[0])

def malloc(size):
    return Pointer([0] * size[0], 0, 1)

def free(ptr):
    pass

def calloc(nmemb, size):
    return Pointer([0] * nmemb[0], 0, size[0])

def realloc(ptr, size):
    if ptr[0] is None:
        return malloc(size)
