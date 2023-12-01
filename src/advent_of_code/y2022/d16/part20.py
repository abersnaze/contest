#!python3

import fileinput
from queue import PriorityQueue
import re
from collections import defaultdict, Counter
from enum import Enum
from itertools import islice, product, repeat
import math
from functools import reduce
from typing import Dict

valves = {}


class Valve:
    def __init__(self, id, rate, edges):
        self.id = id
        self.rate = rate
        self.edges = edges

    def next(self):
        return set(map(valves.get, valves[self.id].edges))

    def __repr__(self):
        return self.id + ":" + str(self.rate) + " -> " + ",".join(self.edges)


lines = list(map(lambda x: x.strip(), fileinput.input()))
non_zero = set()
for line in lines:
    # Valve RN has flow rate=0; tunnels lead to valves AC, CN
    _, id, _, _, rate, _, _, _, _, *other = line.split(" ")
    id, rate, others = (
        id,
        int(rate[5:-1]),
        list(map(lambda x: x.replace(",", ""), other)),
    )
    valve = Valve(id, rate, others)
    if valve.rate != 0:
        non_zero.add(id)
    valves[id] = valve
    print(valve)
print("##################")

adjacent = {}
for start in set([*non_zero, "AA"]):
    dist = defaultdict(lambda: math.inf)
    dist[start] = 0
    queue = set(map(valves.get, valves[start].edges))
    while queue:
        valve: Valve = queue.pop()
        d = min(map(lambda i: dist[i], valve.edges)) + 1
        if d < dist[valve.id]:
            dist[valve.id] = d
            queue = queue.union(valve.next())
    adjacent[start] = {
        id: cost for id, cost in dist.items() if id in non_zero and cost != 0
    }
    print(start, "->", adjacent[start])
print("##################")


class MoveSet:
    def __init__(self, you_moves, elp_moves, you_time, you_total, elp_time, elp_total):
        self.you_moves = you_moves
        self.elp_moves = elp_moves
        self.you_time = you_time
        self.you_total = you_total
        self.elp_time = elp_time
        self.elp_total = elp_total

    def you_goto(self, dest, cost, rate):
        remaining = self.you_time - cost - 1
        total = self.you_total + rate * remaining
        return MoveSet(
            self.you_moves + [dest],
            self.elp_moves,
            remaining,
            total,
            self.elp_time,
            self.elp_total,
        )

    def elp_goto(self, dest, cost, rate):
        remaining = self.elp_time - cost - 1
        total = self.elp_total + rate * remaining
        return MoveSet(
            self.you_moves,
            self.elp_moves + [dest],
            self.you_time,
            self.you_total,
            remaining,
            total,
        )

    def score(self):
        return self.elp_total + self.you_total

    def __lt__(self, o):
        return self.score() > o.score()


move_sets: PriorityQueue[MoveSet] = PriorityQueue()
move_sets.put(MoveSet(["AA"], ["AA"], 26, 0, 26, 0))

best = 0
i = 0
while not move_sets.empty():
    move_set = move_sets.get()
    if best < move_set.score():
        best = move_set.score()
        print(
            move_set.elp_moves,
            move_set.you_moves,
            move_set.you_total + move_set.elp_total,
        )
    i += 1
    if i % 1000000 == 0:
        print(move_sets.qsize())
    # print(move_set.elp_moves, move_set.you_moves, move_set.you_total + move_set.elp_total)
    for dest, cost in adjacent[move_set.you_moves[-1]].items():
        if move_set.you_time - cost < 0:
            continue
        if dest in move_set.you_moves or dest in move_set.elp_moves:
            continue
        # print("\t", dest, cost)
        move_sets.put(move_set.you_goto(dest, cost, valves[dest].rate))
    for dest, cost in adjacent[move_set.elp_moves[-1]].items():
        if move_set.elp_time - cost < 0:
            continue
        if dest in move_set.you_moves or dest in move_set.elp_moves:
            continue
        # print("\t", dest, cost)
        move_sets.put(move_set.elp_goto(dest, cost, valves[dest].rate))
print(best)
