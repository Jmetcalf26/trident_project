from helper_classes import *
from pheaders.stdio import *


def booga():
    return 10


def main():
    a = [1]
    b = [Pointer(a, 0, 4)]
    c = [4 - 2]
    d = [Pointer_alias(Pointer(c, 0, 4), 1)]
    printf(['%c\n'], [d[0].value])
    e = [d[0].value]
    printf(['%d %d %d\n'], [a[0]], [c[0]], [e[0]])


if __name__ == '__main__':
    main()
