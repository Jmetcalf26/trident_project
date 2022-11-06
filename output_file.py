from helper_classes import *
from pheaders.stdio import *


def booga():
    return 10


def main():
    sames = [2]
    x = [None]
    y = [None]
    z = [None]
    while sames[0] > 1:
        printf([Pointer('Enter three distinct numbers: ', 0, 1)])
        scanf([Pointer('%lg %lg %lg', 0, 1)], [Pointer(x, 0, 8)], [Pointer(
            y, 0, 8)], [Pointer(z, 0, 8)])
        sames[0] = dupes([x[0]], [y[0]], [z[0]])
        if dupes([x[0]], [y[0]], [z[0]]) <= 1:
            return 0
        printf([Pointer('There were %d duplicates. Try again.\n', 0, 1)], [
            sames[0]])
    return 0


def dupes(x, y, z):
    sames = [1]
    if (x[0] == y[0] or y[0] == z[0]) or x[0] == z[0]:
        sames[0] += 1
        if x[0] == y[0] and z[0] == y[0]:
            sames[0] += 1
    return sames[0]


if __name__ == '__main__':
    main()
