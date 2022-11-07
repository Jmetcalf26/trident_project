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
