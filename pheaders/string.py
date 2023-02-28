import unicodedata

def isalnum(ch):
    return int(chr(ch).isalnum())

def isalpha(ch):
    return int(chr(ch).isalpha())

def islower(ch):
    return int(chr(ch).islower())

def isupper(ch):
    return int(chr(ch).isupper())

def isdigit(ch):
    return int(chr(ch).isalpha())

def isxdigit(ch):
    c = chr(ch)
    try:
        int(c, 16)
        return 1
    except ValueError:
        return 0

def iscntrl(ch):
    c = chr(ch)
    return int(unicodedata.category(c) == 'C')

def isgraph(ch):
    c = chr(ch)
    cat = unicodedata.category(c)
    return int(cat in 'LMNPS')

def isspace(ch):
    return int(chr(ch).isspace())

def isblank(ch):
    c = chr(ch)
    cat = unicodedata.category(c)
    return int(cat == 'Zs' or c == '\t')

def isprint(ch):
    return int(chr(ch).isprintable())

def ispunct(ch):
    c = chr(ch)
    cat = unicodedata.category(c)
    return int(cat == 'P')

def tolower(ch):
    return ord(chr(ch).lower())

def toupper(ch):
    return ord(chr(ch).upper())

def strcpy(dest, src):
    i = 0
    while src[i] != 0:
        dest[i] = src[i]
        i+=1
    dest[i] = 0

def strcmp(comp1, comp2):
    scomp1 = str(comp1)
    #print('scomp1', scomp1)
    scomp2 = str(comp2)
    #print('scomp2', scomp2)

    if scomp1 == scomp2:
        return 0
    elif scomp1 < scomp2:
        return -1
    else:
        return 1

def strlen(s):
    i = 0
    while s[i] != 0:
        i+=1
    return i
