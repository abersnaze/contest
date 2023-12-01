#!python3

import fileinput
import re
from collections import defaultdict, Counter
from enum import Enum
from itertools import islice, product, repeat
import math
from functools import reduce


def dist(ax, ay, bx, by):
    if ax < bx:
        ax, bx = bx, ax
    if ay < by:
        ay, by = by, ay
    return (ax - bx) + (ay - by)


lines = list(map(lambda x: x.strip(), fileinput.input()))
valves = {}
for line in lines:
    # Valve RN has flow rate=0; tunnels lead to valves AC, CN
    _, valve, _, _, rate, _, _, _, _, *other = line.split(" ")
    valve, rate, others = (
        valve,
        int(rate[5:-1]),
        list(map(lambda x: x.replace(",", ""), other)),
    )
    print(valve, rate, others)
    valves[valve] = (rate, others)
print("##################")


def availble_moves(curr_loc, remaining, visited: set, open_valves: tuple):
    if remaining == 0:
        return
    if curr_loc in visited:
        return
    rate, others = valves[curr_loc]
    if curr_loc not in open_valves:
        yield (curr_loc, remaining - 1, rate * (remaining - 1))
    for other in others:
        yield from availble_moves(other, remaining, visited | {curr_loc}, open_valves)


def best_availble_moves(curr_loc, remaining, open_valves, total):
    move_by_dest = defaultdict(lambda: (30, 0))
    for valve, time, amount in availble_moves(curr_loc, remaining, set(), open_valves):
        _, prev_amount = move_by_dest[valve]
        if prev_amount <= amount + total:
            move_by_dest[valve] = (time, amount + total)
    return {
        tuple([*open_valves, loc]): (time, amount)
        for loc, (time, amount) in move_by_dest.items()
    }


best = best_availble_moves("AA", 30, tuple(), 0)
done = False
round = 0
while not done:
    print("round", round)
    open, (time, total) = max(best.items(), key=lambda x: x[1][1])
    print("\t", open, time, total)
    round += 1
    next_best = defaultdict(lambda: (30, 0))
    for open_valves, (time, amount) in best.items():
        for loc in open_valves:
            # print(loc, time, amount, open_valves)
            next_moves = best_availble_moves(loc, time, open_valves, amount)
            for next_open, (next_time, next_total) in next_moves.items():
                _, prev_total = next_best[next_open]
                # print("\t", next_open, next_time, next_total, prev_total)
                if prev_total <= next_total:
                    next_best[next_open] = (next_time, next_total)

    done = best == next_best
    best = next_best
