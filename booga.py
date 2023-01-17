from helper_classes import *
from pheaders.stdio import *
from pheaders.stdlib import *


def main():
    x = [Pointer([0, 1, 2], 0, 4)]
    a = [Deref(x[0], 0).get_pointer()]
    printf([Pointer('%d\n', 0, 1)], [a[0]])
    b = [Deref(x[0], 1).get_pointer()]
    printf([Pointer('%d\n', 0, 1)], [b[0]])
    c = [Deref(x[0], 2).get_pointer()]
    printf([Pointer('%d\n', 0, 1)], [c[0]])
    m = [Pointer([a[0], b[0], c[0]], 0, 8)]
    printf([Pointer('%d\n', 0, 1)], [m[0]])
    p = [Deref(m[0], 2)]
    printf([Pointer('%d\n', 0, 1)], [p[0]])
    n = [p[0].get_value()]
    printf([Pointer('%d\n', 0, 1)], [n[0]])
    q = [Deref(m[0], 2).get_value()]
    printf([Pointer('%d\n', 0, 1)], [q[0]])
    o = [a[0].get_value()]
    printf([Pointer('%d\n', 0, 1)], [o[0]])


if __name__ == '__main__':
    main()
