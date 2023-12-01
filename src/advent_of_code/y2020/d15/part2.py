#!python3

import fileinput
import sys


def run(starts: list, count, end):
    order = dict(map(lambda entry: (entry[1], (entry[0] + 1,)), enumerate(starts)))
    last = starts[-1]
    print(order, last, "\n")
    for t in range(len(starts) + 1, count + 1):
        if t % 1000000 == 0:
            print(t)
        hist = order.get(last, "X")
        # sys.stdout.write(f"turn: {t} last: {last} order: {hist}")
        if len(hist) == 2:
            next = hist[0] - hist[1]
        else:
            next = 0
        # print(f" next: {next}")
        order[next] = (t, order.get(next, (t,))[0])
        last = next

    print(last, "=", end)


for case in fileinput.input():
    starts, count, end = case.split(":")
    starts = list(map(int, starts.split(",")))
    run(starts, int(count), int(end.strip()))
