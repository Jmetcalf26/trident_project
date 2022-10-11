import sys

def puts(string):
    print(string[0])

stdout = [sys.stdout]
stdin = [sys.stdin]
stderr = [sys.stderr]

def _cformat(fmt, args):
    return fmt[0] % tuple(a[0] for a in args)

def printf(fmt, *args):
    fprintf(stdout, fmt, *args)

def fprintf(stream, fmt, *args):
    print(_cformat(fmt, args), end='', file=stream[0])

def scanf(fmt, *args):
    fscanf(stdin, fmt, *args)

def fscanf(stream, fmt, *args):
    inp = input()
    args = tuple(map(int, inp.split(' ')))
