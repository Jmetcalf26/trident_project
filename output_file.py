def bmain(x):
    x[0] = x[0] + 2
    return 3


def cmain():
    return 2


def main():
    return bmain([cmain()])


if __name__ == '__main__':
    exit(main())
