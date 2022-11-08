from helper_classes import *
from pheaders.stdio import *
from pheaders.stdlib import *
from pheaders.string import *


def booga():
    return 10


def main():
    seed = [None]
    printf([Pointer('Seed: ', 0, 1)])
    scanf([Pointer('%d', 0, 1)], [Pointer(seed, 0, 4)])
    srand([seed[0]])
    play([seed[0]])
    return 0


def play(seed):
    deck = [shuffle([seed[0]])]
    player = [Pointer([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 0, 4)]
    dealer = [Pointer([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 0, 4)]
    deckpos = [51]
    sleeptime = [2]
    pscore = [0]
    dscore = [0]
    cmd = [ord('h')]
    pbust = [0]
    dbust = [0]
    if True:
        i = [0]
        while i[0] < 2:
            deal([player[0]], [deck[0]], [Pointer(deckpos, 0, 4)])
            deal([dealer[0]], [deck[0]], [Pointer(deckpos, 0, 4)])
            i[0] += 1
    while cmd[0] == ord('h') and pscore[0] <= 21:
        printhands([player[0]], [dealer[0]], [1], [Pointer(pscore, 0, 4)],
            [Pointer(dscore, 0, 4)])
        if pscore[0] <= 21:
            printf([Pointer('Hit or stand? [h/s] ', 0, 1)])
            scanf([Pointer(' %c', 0, 1)], [Pointer(cmd, 0, 1)])
            if cmd[0] == ord('h'):
                deal
                player[0]
                deck[0]
                Pointer(deckpos, 0, 4)
        elif True:
            printf([Pointer('Player busts!\n', 0, 1)])
            pbust[0] = 1
            break
    while dscore[0] <= 21:
        printhands([player[0]], [dealer[0]], [0], [Pointer(pscore, 0, 4)],
            [Pointer(dscore, 0, 4)])
        sleep([sleeptime[0]])
        if pbust[0] or dscore[0] >= 17 and dscore[0] <= 21:
            printf([Pointer('Dealer stands.\n', 0, 1)])
            break
        elif dscore[0] > 21:
            printf([Pointer('Dealer busts!\n', 0, 1)])
            dbust[0] = 1
        elif True:
            printf([Pointer('Dealer hits.\n', 0, 1)])
            deal([dealer[0]], [deck[0]], [Pointer(deckpos, 0, 4)])
    printf([Pointer('\nFinal scores: Player %d, Dealer %d.\n', 0, 1)], [
        pscore[0]], [dscore[0]])
    if pscore[0] == dscore[0]:
        printf([Pointer('Push! Play again.\n', 0, 1)])
        play([seed[0]])
    elif pbust[0] or not dbust[0] and dscore[0] > pscore[0]:
        printf([Pointer('Dealer wins!\n', 0, 1)])
    elif True:
        printf([Pointer('Player wins!\n', 0, 1)])


def deal(hand, deck, deckpos):
    handpos = [0]
    while hand[0][handpos[0]] != ord('\x00'):
        handpos[0] += 1
    hand[0][handpos[0]] = deck[0][deckpos[0].value]
    deckpos[0].value -= 1


def printhands(player, dealer, hide, pscore, dscore):
    max = [0]
    dealmax = [0]
    while player[0][max[0]] != ord('\x00'):
        max[0] += 1
    while dealer[0][dealmax[0]] != ord('\x00'):
        dealmax[0] += 1
    if dealmax[0] > max[0]:
        max[0]
        dealmax[0]
    else:max[0]
    pscore[0].value = 0
    dscore[0].value = 0
    printf([Pointer('\n Player Dealer\n', 0, 1)])
    if True:
        i = [0]
        while i[0] < max[0]:
            printf([Pointer('| ', 0, 1)])
            if player[0][i[0]] != ord('\x00'):
                pscore[0].value = printcard([player[0][i[0]]], [pscore[0]])
            elif True:
                printf([Pointer('    ', 0, 1)])
            printf([Pointer(' | ', 0, 1)])
            if dealer[0][i[0]] != ord('\x00'):
                if i[0] == 1 and hide[0]:
                    printf([Pointer(' ** ', 0, 1)])
                elif True:
                    dscore[0].value = printcard([dealer[0][i[0]]], [dscore[0]])
            elif True:
                printf([Pointer('    ', 0, 1)])
            printf([Pointer(' |\n', 0, 1)])
            i[0] += 1


def shuffle(seed):
    deck = [Pointer([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], 0, 4)]
    suitnumber = [1]
    facevalue = [None]
    if True:
        i = [0]
        while i[0] < 52:
            if i[0] % 13 == 0 and i[0] != 0:
                suitnumber[0] += 1
                facevalue[0] = 2
            facevalue[0] = 2 + i[0] % 13
            deck[0][i[0]] = 100 * suitnumber[0] + facevalue[0]
            i[0] += 1
    if seed[0] != 0:
        if True:
            i = [51]
            while i[0] >= 0:
                j = [rand() % (i[0] + 1)]
                temp = [deck[0][i[0]]]
                deck[0][i[0]] = deck[0][j[0]]
                deck[0][j[0]] = temp[0]
                i[0] -= 1
    return deck[0]


def printcard(cardindex, score):
    suitnumber = [cardindex[0] / 100]
    facevalue = [cardindex[0] % 100]
    __switch_state_status0 = [0]
    __switch_var_value0 = [facevalue[0]]
    if (__switch_state_status0 == 1 or __switch_state_status0 == 0 and 
        __switch_var_value0 == 11):
        printf([Pointer(' J', 0, 1)])
        score[0].value += 10
        __switch_state_status0 = [2]
    if (__switch_state_status0 == 1 or __switch_state_status0 == 0 and 
        __switch_var_value0 == 12):
        printf([Pointer(' Q', 0, 1)])
        score[0].value += 10
        __switch_state_status0 = [2]
    if (__switch_state_status0 == 1 or __switch_state_status0 == 0 and 
        __switch_var_value0 == 13):
        printf([Pointer(' K', 0, 1)])
        score[0].value += 10
        __switch_state_status0 = [2]
    if (__switch_state_status0 == 1 or __switch_state_status0 == 0 and 
        __switch_var_value0 == 14):
        printf([Pointer(' A', 0, 1)])
        if score[0].value + 11 > 21 or score[0].value == 2:
            score[0].value += 1
            if score[0].value == 12:
                score[0].value = score[0].value - 10
        elif True:
            score[0].value += 11
        __switch_state_status0 = [2]
        break
        score[0].value += facevalue[0]
        __switch_state_status0 = [2]
    __switch_state_status1 = [0]
    __switch_var_value1 = [suitnumber[0]]
    if (__switch_state_status1 == 1 or __switch_state_status1 == 0 and 
        __switch_var_value1 == 1):
        printf([Pointer('♣ ', 0, 1)])
        __switch_state_status1 = [2]
    if (__switch_state_status1 == 1 or __switch_state_status1 == 0 and 
        __switch_var_value1 == 2):
        printf([Pointer('♦ ', 0, 1)])
        __switch_state_status1 = [2]
    if (__switch_state_status1 == 1 or __switch_state_status1 == 0 and 
        __switch_var_value1 == 3):
        printf([Pointer('♥ ', 0, 1)])
        __switch_state_status1 = [2]
    if (__switch_state_status1 == 1 or __switch_state_status1 == 0 and 
        __switch_var_value1 == 4):
        printf([Pointer('♠ ', 0, 1)])
        __switch_state_status1 = [2]
        break
        __switch_state_status1 = [2]
    return score[0].value


if __name__ == '__main__':
    main()
