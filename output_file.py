def booga(a):
    b = [-a[0]]
    while b[0] > 0:
        a[0] = a[0] + 1
        a[0] = a[0] - 1
    if b[0] == 0:
        a[0] = a[0] + 3
    else:
        a[0] = a[0] + 2
    return a[0] ^ 1


def main():
    a = [1]
    return booga(a[0])


if __name__ == '__main__':
    main()
