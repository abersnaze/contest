#!pypy

import fileinput
import re
from collections import defaultdict, Counter
from itertools import islice, product, repeat, chain
from functools import reduce


LIMIT = 25
lines = list(map(lambda x: x.strip(), fileinput.input()))
kinds = ["ore", "clay", "obsidian", "geode"]
blueprint_num = 1
all_blueprints = defaultdict(list)
for line in lines:
    blueprint = line[line.index(":") + 7 : -1]
    for recipe in blueprint.split(". Each "):
        if " and " in recipe:
            (
                kind,
                _,
                _,
                amount1,
                thing1,
                _,
                amount2,
                thing2,
            ) = recipe.split(" ")
            cost = [0, 0, 0]
            cost[kinds.index(thing1)] = int(amount1)
            cost[kinds.index(thing2)] = int(amount2)
            result = [0, 0, 0, 0]
            result[kinds.index(kind)] = 1
            all_blueprints[blueprint_num].append((cost, result))
        else:
            kind, _, _, amount1, thing1 = recipe.split(" ")
            cost = [0, 0, 0]
            cost[kinds.index(thing1)] = int(amount1)
            result = [0, 0, 0, 0]
            result[kinds.index(kind)] = 1
            all_blueprints[blueprint_num].append((cost, result))
    blueprint_num += 1


def mul(foos, x):
    return (foo * x for foo in foos)


def add(foos, bars):
    return (foo + bar for foo, bar in zip(foos, bars))


def sub(foos, bars):
    return (foo - bar for foo, bar in zip(foos, bars))


def use_blueprint(time, robots, inventory, geode_total, cost, result):
    longest = 0
    for robot, inv, amount in zip(robots, inventory, cost):
        if inv >= amount:
            continue
        if robot == 0:
            # no amount of time will get what we need
            return
        # divide round up
        duration = (amount - inv + robot - 1) // robot
        if duration > longest:
            longest = duration
    if longest + time < LIMIT - 1:
        time += longest + 1
        geode_total += result[3] * (LIMIT - time)
        inventory = tuple(sub(add(inventory, mul(robots, longest + 1)), cost))
        robots = tuple(add(robots, result))
        # state at the end of the time step
        yield (time, robots, inventory, geode_total)


def optimal(blueprints):
    queue = [(0, (1, 0, 0), (0, 0, 0), 0)]
    best_at = [0 for t in range(LIMIT)]
    while queue:
        state = queue.pop()
        geodes = state[3]
        if geodes < best_at[state[0]]:
            continue
        if geodes > best_at[state[0]]:
            for t in range(state[0], LIMIT):
                best_at[t] == geodes
        best_at[state[0]] = state[3]
        for choice in blueprints:
            queue.extend(use_blueprint(*state, *choice))
        queue.sort(key=lambda s: s[0], reverse=True)
    return best_at[LIMIT - 1]


for num, blueprints in all_blueprints.items():
    best = optimal(blueprints)
    print(num, best)
