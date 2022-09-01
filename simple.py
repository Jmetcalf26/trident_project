def booga(a):
    b = [-a[0]]
    if b[0] > 0:
        a[0] = a[0] + 1
    else:
        a[0] = a[0] + 2

    return a[0]+1
def main():
    a = [1]
    return booga(a)

if __name__ == "__main__":
     main()
