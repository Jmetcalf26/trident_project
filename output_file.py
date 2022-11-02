from helper_classes import *
from pheaders.stdio import *


def booga():
    return 10


def main():
    a = [Pointer('booga', 0, 1)]
    printf([Pointer('%s\n', 0, 1)], [a[0]])
    x = [None]
    scanf([Pointer('%d', 0, 1)], [Pointer(x, 0, 4)])


if __name__ == '__main__':
    main()
