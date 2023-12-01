#!python3

import fileinput
import re
from collections import defaultdict


def run(order: list, count, end):
    spoken = set(order[1:])
    while len(order) < count:
        last = order[0]
        if last in spoken:
            next = order.index(last, 1)
        else:
            next = 0
        spoken.add(last)
        # print(next, order, spoken)
        order.insert(0, next)
        if len(order) % 10000 == 0:
            print(len(order))

    print(order[0], "=", end)


for case in fileinput.input():
    starts, count, end = case.split(":")
    starts = list(map(int, starts.split(",")))
    starts.reverse()
    run(starts, int(count), int(end.strip()))
