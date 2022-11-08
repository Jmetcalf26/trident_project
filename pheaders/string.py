import unicodedata

def isalnum(ch):
    return int(chr(ch[0]).isalnum())

def isalpha(ch):
    return int(chr(ch[0]).isalpha())

def islower(ch):
    return int(chr(ch[0]).islower())

def isupper(ch):
    return int(chr(ch[0]).isupper())

def isdigit(ch):
    return int(chr(ch[0]).isalpha())

def isxdigit(ch):
    c = chr(ch[0])
    try:
        int(c, 16)
        return 1
    except ValueError:
        return 0

def iscntrl(ch):
    c = chr(ch[0])
    return int(unicodedata.category(c) == 'C')

def isgraph(ch):
    c = chr(ch[0])
    cat = unicodedata.category(c)
    return int(cat[0] in 'LMNPS')

def isspace(ch):
    return int(chr(ch[0]).isspace())

def isblank(ch):
    c = chr(ch[0])
    cat = unicodedata.category(c)
    return int(cat[0] == 'Zs' or c == '\t')

def isprint(ch):
    return int(chr(ch[0]).isprintable())

def ispunct(ch):
    c = chr(ch[0])
    cat = unicodedata.category(c)
    return int(cat[0] == 'P')

def tolower(ch):
    return ord(chr(ch[0]).lower()[0])

def toupper(ch):
    return ord(chr(ch[0]).upper()[0])

def strcpy(dest, src):
    i = 0
    while src[0][i] != 0:
        dest[0][i] = src[0][i]
        i+=1
    dest[0][i] = 0

def strcmp(comp1, comp2):
    scomp1 = str(comp1[0])
    scomp2 = str(comp2[0])

    if scomp1 == scomp2:
        return 0
    elif scomp1 < scomp2:
        return -1
    else:
        return 1
