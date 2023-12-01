#!python3

import fileinput
import re
from collections import defaultdict, Counter
from itertools import islice, product, repeat
import math
from functools import reduce

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
non_zero = []
for line in lines:
    # Valve RN has flow rate=0; tunnels lead to valves AC, CN
    part = line.split(" ")
    id = part[1]
    rate = part[4]
    other = part[9:]
    id, rate, others = (
        id,
        int(rate[5:-1]),
        list(map(lambda x: x.replace(",", ""), other)),
    )
    valve = Valve(id, rate, others)
    if valve.rate != 0:
        non_zero.append(id)
    valves[id] = valve
    print(valve)
print("##################")

adjacent = {}
for start in set(non_zero) | {"AA"}:
    dist = defaultdict(lambda: 100000000)
    dist[start] = 0
    queue = set(map(valves.get, valves[start].edges))
    while queue:
        valve = queue.pop()
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
    def __init__(self, moves, time, total):
        self.moves = moves
        self.time = time
        self.total = total

    def __lt__(self, o):
        return self.total < o.total

    def __repr__(self):
        return str(self.time) + ", " + str(self.total) + ", " + ",".join(self.moves)


best_of_best = 0


def best_moves(valve_set):
    move_sets = []
    move_sets.append(MoveSet(["AA"], 26, 0))
    local_best = 0
    best_move = None
    while move_sets:
        move_set = move_sets.pop()
        if move_set.total > local_best:
            local_best = move_set.total
            best_move = move_set
            # print(move_set.moves, move_set.total, move_set.time)
        for dest, cost in adjacent[move_set.moves[-1]].items():
            if dest not in valve_set:
                continue
            if move_set.time - cost < 0:
                continue
            if dest in move_set.moves:
                continue
            remaining = move_set.time - cost
            total = move_set.total + valves[dest].rate * (remaining - 1)
            move_sets.append(MoveSet(move_set.moves + [dest], remaining - 1, total))
    print(str(best_of_best) + "\t" + str(best_move))
    return local_best


combined_best = 0
bits = len(non_zero)
for split in range(1 << (bits - 1)):
    elp_non_zero = set()
    you_non_zero = set()
    for i in range(bits):
        if split & 1:
            elp_non_zero.add(non_zero[i])
        else:
            you_non_zero.add(non_zero[i])
        split >>= 1

    elp_best = best_moves(you_non_zero)
    you_best = best_moves(elp_non_zero)
    combined_best = elp_best + you_best
    if best_of_best < combined_best:
        best_of_best = combined_best
        print(you_best, elp_best, combined_best, you_non_zero, elp_non_zero)

print(best_of_best)
