def booga(a):
    i = [0]
    b = [-a[0]]
    if True:
        i[0] = 0
        while i[0] < a[0]:
            a[0] = a[0] + 1
            a[0] = a[0] - 1
            i[0] += 1
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
