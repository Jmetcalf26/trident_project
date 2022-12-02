

from helper_classes import *
from pheaders.stdio import *
from pheaders.string import *


def main():
    berthing = [Pointer([0, 0], 0, 4)]
    name = [Pointer([0, 0, 0, 0, 0, 0, 0, 0], 0, 1)]
    printf([Pointer('Enter your wing and deck: ', 0, 1)])
    scanf([Pointer(' %d %d', 0, 1)], [berthing[0]], [berthing[0] + 1])
    printf([Pointer('Enter your name: ', 0, 1)])
    scanf([Pointer('%s', 0, 1)], [name[0]])
    printf([Pointer('%s lives in %d wing and on %d deck\n', 0, 1)],
            [name[0]], [berthing[0][0]], [berthing[0][1]])
    return 0


if __name__ == '__main__':
    main()



