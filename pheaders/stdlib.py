import random

RAND_MAX = [2**32-1]
_rng = random.Random(0)

def srand(seed):
    _rng.seed(seed[0])
def rand():
    return _rng.randrange(RAND_MAX[0])
