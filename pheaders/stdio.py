import sys
import re

EOF = [-1]
stdout = [sys.stdout.buffer]
stdin = [sys.stdin.detach()]
stderr = [sys.stderr.buffer]

def fopen(fname, mode):
    mod = mode[0]
    if 'b' not in mod:
        mod += 'b'
    return open(fname, mod)

def fclose(stream):
    stream[0].close()

def fflush(stream):
    stream[0].flush()

def puts(string):
    stdout[0].write(str(string[0]).encode())
    stdout[0].write(b'\n')
    stdout[0].flush()

def printf(fmt, *args):
    fprintf(stdout, fmt, *args)

def fprintf(stream, fmt, *args):
    output = str(fmt[0]) % tuple(a[0] for a in args)
    stream[0].write(output.encode())
    stream[0].flush()

def scanf(fmt, *args):
    return fscanf(stdin, fmt, *args)

class _Reader:
    def __init__(self, fin):
        self.f = fin
        self.eof = False
        self.consumed = 0

    def read(self, pat, limit=None):
        chunks = []
        while True:
            if limit is None:
                rpat = pat + '+'
            else:
                rpat = pat + f'{{1,{limit}}}'
            raw_peek = self.f.peek()
            if len(raw_peek) == 0:
                self.eof = True
                break
            peeked = raw_peek.decode(errors='ignore')
            mat = re.match(rpat, peeked)
            if mat is None:
                break
            chunks.append(mat.group())
            matlen = len(mat.group().encode())
            self.f.read(matlen)
            self.consumed += matlen
            if mat.end() < len(peeked):
                break
            if limit is not None:
                limit -= len(peeked)
                if limit == 0:
                    break
        return ''.join(chunks)

    def word(self, seq):
        for x in seq:
            if not self.read(f'[{x.lower()}{x.upper()}]', 1):
                return False
        return True

    def get_float(self):
        sign = self.read('[+-]', 1)
        zero = self.read('0', 1)
        dpat = '[0-9]'
        base = 10
        esim = '[eE]'
        if zero:
            ex = self.read('[xX]', 1)
            if ex:
                dpat = '[0-9a-fA-F]'
                base = 16
                esim = '[pP]'
        pre = self.read(dpat)
        dot = self.read(re.escape('.'), 1)
        if not pre and not dot:
            # try for inf or nan
            if self.word('inf'):
                self.word('inity')
                return float(sign + 'inf')
            elif self.word('nan'):
                return float('nan')
        if dot:
            post = self.read(dpat)
        else:
            post = ''
        if not pre and not post:
            return None
        e = self.read(esim, 1)
        if e:
            expo = self.read('[0-9]')
            if not expo:
                return None
        else:
            expo = ''
        if base == 10:
            return float(sign + pre + dot + post + e + expo)
        else:
            return float.fromhex(sign + '0x' + pre + dot + post + e + expo)


def _signum(sign_string, num):
    return -num if sign_string == '-' else num

_scanf_fmt = re.compile(r"""
        (?P<capture>
            %
            (?P<noassign> \*)?
            (?P<width> [1-9][0-9]*)?
            (?P<modifier> hh|h|l|ll|j|z|t|L)?
            (?: (?P<percent> %)
              | (?P<char> c)
              | (?P<string> s)
              | (?P<set>
                    \[
                    (?P<invert> \^)?
                    (?P<bracket> \])?
                    (?P<chars> [^\]]*)
                    \]
                )
              | (?P<decimal> d)
              | (?P<integer> i)
              | (?P<unsigned> u)
              | (?P<octal> o)
              | (?P<hex> [xX])
              | (?P<count> n)
              | (?P<float> [aAeEfFgG])
              | (?P<pointer> p)
            )
        )
        | (?P<space> \s+)
        | (?P<literal> .)
    """, re.VERBOSE | re.DOTALL)

def fscanf(stream, fmt, *args):
    rdr = _Reader(stream[0])
    fstring = str(fmt[0])
    dest_it = iter(x[0] for x in args)
    nassign = 0
    lastend = 0
    for fmatch in _scanf_fmt.finditer(fstring):
        rhs = None
        if fmatch.start() != lastend:
            raise ValueError(f"scanf format string invalid at '{fstring[lastend:fmatch.start()]}'")
        if fmatch.group('space'):
            rdr.read(r'\s')
        elif fmatch.group('literal'):
            if not rdr.read(re.escape(fmatch.group('literal')), 1):
                break
        elif fmatch.group('percent'):
            if not rdr.read('%', 1):
                break
        elif fmatch.group('char'):
            wg = fmatch.group('width')
            width = 1 if wg is None else int(wg)
            got = rdr.read('.', width)
            if len(got) != width:
                break
            rhs = [ord(s) for s in got]
        elif fmatch.group('string'):
            rdr.read(r'\s')
            wg = fmatch.group('width')
            got = rdr.read(r'\S', None if wg is None else int(wg))
            rhs = [ord(s) for s in got]
            rhs.append(0)
        elif fmatch.group('set'):
            pat = '['
            if fmatch.group('invert'):
                pat += '^'
            if fmatch.group('bracket'):
                pat += r'\['
            pat += fmatch.group('chars')
            pat += ']'
            wg = fmatch.group('width')
            got = rdr.read(pat, None if wg is None else int(wg))
            rhs = [ord(s) for s in got]
            rhs.append(0)
        elif fmatch.group('decimal'):
            rdr.read(r'\s')
            sign = rdr.read('[+-]', 1)
            digits = rdr.read('[0-9]')
            if not digits:
                break
            rhs = _signum(sign, int(digits))
        elif fmatch.group('integer'):
            rdr.read(r'\s')
            sign = rdr.read('[+-]', 1)
            zero = rdr.read('0', 1)
            if zero:
                ex = rdr.read('[xX]', 1)
                if ex:
                    pat = '[0-9a-fA-F]'
                    base = 16
                else:
                    pat = '[0-7]'
                    base = 8
            else:
                pat = '[0-9]'
                base = 10
            digits = rdr.read(pat)
            if not digits:
                break
            rhs = _signum(sign, int(digits, base))
        elif fmatch.group('unsigned'):
            rdr.read(r'\s')
            digits = rdr.read('[0-9]')
            if not digits:
                break
            rhs = int(digits)
        elif fmatch.group('octal'):
            rdr.read(r'\s')
            digits = rdr.read('[0-7]')
            if not digits:
                break
            rhs = int(digits, 8)
        elif fmatch.group('hex'):
            rdr.read(r'\s')
            digits = rdr.read('[0-9a-fA-F]')
            if not digits:
                break
            rhs = int(digits, 16)
        elif fmatch.group('count'):
            rhs = rdr.consumed
        elif fmatch.group('float'):
            rdr.read(r'\s')
            rhs = rdr.get_float()
            if rhs is None:
                break
        else:
            # TODO pointer
            raise NotImplementedError(f"scanf matcher {fmatch}")
        lastend = fmatch.end()
        if rhs is not None and fmatch.group('noassign') is None:
            try:
                dest = next(dest_it)
            except StopIteration:
                raise ValueError("not enough destinations for scanf") from None
            if isinstance(rhs, list):
                for i in range(len(rhs)):
                    dest[i] = rhs[i]
            else:
                dest[0] = rhs
            nassign += 1
    else:
        if lastend != len(fstring):
            raise ValueError(f"scanf format string invalid at '{fstring[lastend:]}'")
    if nassign == 0 and rdr.eof:
        return EOF[0]
    else:
        return nassign
