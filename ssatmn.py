def booga(a):
    return a ^ 1


def main():
    a = 1print(a)
    a = booga(a)print(a)
    return booga(booga(a) * 10)


if __name__ == '__main__':
    main()
