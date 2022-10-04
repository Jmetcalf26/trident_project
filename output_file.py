from helper_classes import *


def main():
    a = [1]
    if a > 2147483647:
        print('NOOOO')
    elif a < -2147483648:
        print('NOOOO')
    b = [1]
    c = [a[0] + b[0]]
    if c > 2147483647:
        print('NOOOO')
    elif c < -2147483648:
        print('NOOOO')
    d = [3]
    if d > 4294967295:
        print('NOOOO')
    e = [1.5]
    f = [1.5]
    g = [1.5]


if __name__ == '__main__':
    main()
