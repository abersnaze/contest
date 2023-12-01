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
    def __init__(self, id, rate, edges) -> None:
        self.id = id
        self.rate = rate
        self.edges = edges

    def next(self):
        return set(map(valves.get, valves[self.id].edges))

    def __repr__(self) -> str:
        return f"{self.id}:{self.rate} -> {','.join(self.edges)}"


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
    def __init__(self, moves, time, total) -> None:
        self.moves = moves
        self.time = time
        self.total = total

    def goto(self, dest, cost, rate):
        remaining = self.time - cost
        total = self.total + rate * remaining
        return MoveSet(self.moves + [dest], remaining, total)

    def __lt__(self, o):
        return self.total < o.total


move_sets: PriorityQueue[MoveSet] = PriorityQueue()
move_sets.put(MoveSet(["AA"], 30, 0))

while not move_sets.empty():
    move_set = move_sets.get()
    print(move_set.moves, move_set.total, move_set.time)
    for dest, cost in adjacent[move_set.moves[-1]].items():
        if move_set.time - cost < 0:
            continue
        if dest in move_set.moves:
            continue
        print("\t", dest, cost)
        move_sets.put(move_set.goto(dest, cost, valves[dest].rate))
