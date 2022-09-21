from pointer import *
from pheaders.stdio import *


def booga():
    return 10


def main():
    n = [3]
    a = [[0] * n[0]]
    b = [booga()]
    puts([a[0][2]])
    s = ['string\n']
    puts([s[0]])
    return b[0]


if __name__ == '__main__':
    main()
