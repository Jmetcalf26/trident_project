from helper_classes import *
from pheaders.stdio import *


def booga():
    return 10


def main():
    a = [0]
    b = [1]
    c = [a[0] + b[0]]
    h = ['%d%d\n']
    printf([h[0]], [a[0]], [c[0]])


if __name__ == '__main__':
    main()
