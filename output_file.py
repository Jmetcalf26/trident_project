from pointer import *


def main():
    a = [1]
    b = [Pointer(a, 0) + 3]
    c = [b[0].get()]
    return 0


if __name__ == '__main__':
    main()
