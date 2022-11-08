from helper_classes import *


def main():
    length = [None]
    best = [0]
    curr_word = [Pointer([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 0, 1)]
    best_word = [Pointer([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 0, 1)]
    while strcmp([curr_word[0]], [Pointer('DONE', 0, 1)]):
        scanf([Pointer('%s', 0, 1)], [curr_word[0]])
        curr = [replacements([curr_word[0]])]
        printf([Pointer('%s\n', 0, 1)], [curr_word[0]])
        if curr[0] > best[0]:
            strcpy([best_word[0]], [curr_word[0]])
            best[0] = curr[0]
    printf([Pointer('%d conversions for "%s"\n', 0, 1)], [best[0]], [
        best_word[0]])
    return 0


def replacements(word):
    replacements = [0]
    if True:
        i = [0]
        while word[0][i[0]] != 0:
            if word[0][i[0]] == ord('a'):
                word[0][i[0]] = ord('@')
                replacements[0] += 1
            elif word[0][i[0]] == ord('e'):
                word[0][i[0]] = ord('3')
                replacements[0] += 1
            elif word[0][i[0]] == ord('i'):
                word[0][i[0]] = ord('!')
                replacements[0] += 1
            elif word[0][i[0]] == ord('t'):
                word[0][i[0]] = ord('+')
                replacements[0] += 1
            i[0] += 1
    return replacements[0]


if __name__ == '__main__':
    main()
