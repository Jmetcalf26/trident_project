import random
from helper_classes import *
RAND_MAX = 2**32-1
_rng = random.Random(0)
NULL = variable(0, size=8)

def srand(seed):
    _rng.seed(seed)
def rand():
    return _rng.randrange(RAND_MAX)

def malloc(size):
    return Pointer([0] * size, 0, 1)

def free(ptr):
    pass

def calloc(nmemb, size):
    return Pointer([0] * nmemb, 0, size)

def realloc(ptr, size):
    if ptr is None:
        return malloc(size)

def memset(string, c, n):
    for i in range(c):
        string[i] = c[i]

