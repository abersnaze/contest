#!python3

import fileinput
import re
from collections import defaultdict, Counter
import sys
from enum import Enum
from itertools import islice

lines = map(lambda x: x.strip(), fileinput.input())

draws = list(map(int, next(lines).split(",")))
next(lines)


def boards():
    board = []
    for line in lines:
        if line == "":
            continue
        if len(board) == 5:
            yield board
            board = []
        board.append(list(map(int, re.split(" +", line))))
    yield board
    return


def blank():
    return [
        [False, False, False, False, False],
        [False, False, False, False, False],
        [False, False, False, False, False],
        [False, False, False, False, False],
        [False, False, False, False, False],
    ]


def bingo(marks):
    a = [
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
        True,
    ]
    for i in range(0, 5):
        a[0] &= marks[0][i]
        a[1] &= marks[1][i]
        a[2] &= marks[2][i]
        a[3] &= marks[3][i]
        a[4] &= marks[4][i]
        a[5] &= marks[i][0]
        a[6] &= marks[i][1]
        a[7] &= marks[i][2]
        a[8] &= marks[i][3]
        a[9] &= marks[i][4]
    return any(a)


min = len(draws)
answer = 0
for board in boards():
    marks = blank()
    for i, draw in enumerate(draws):
        for x in range(0, 5):
            for y in range(0, 5):
                if board[y][x] == draw:
                    marks[y][x] = True
        if bingo(marks):
            print(i, draw, board, marks)
            break
    if i < min:
        print("found better")
        s = 0
        for x in range(0, 5):
            for y in range(0, 5):
                if not marks[y][x]:
                    s += board[y][x]
        min = i
        answer = s * draw

print(answer)
