#!/usr/bin/env python3

from collections import Counter, defaultdict
from fileinput import input
from functools import cmp_to_key
from itertools import count, product
import json
from math import ceil, floor, inf, prod, sqrt
import re
from common.space import Space, adjacent4


def ingest(files=None):
    foos = []
    for line in input(files):
        line = line.strip()
        constraints, pattern = line.split()
        foos.append((constraints, tuple(map(int, pattern.split(",")))))
    return foos


def process(foos):
    opts = defaultdict(list)
    for constraints, pattern in foos:
        key = f"{constraints}, {pattern}"
        print(key)
    print(json.dumps(opts, indent=2))
    return sum([len(x) for x in opts.values()])


def premute(constraints, start_at=0):
    if start_at >= len(constraints):
        yield constraints
        return
    if constraints[start_at] == "?":
        yield from premute(constraints.replace("?", "#", 1), start_at + 1)
        yield from premute(constraints.replace("?", "_", 1), start_at + 1)
        return
    if constraints[start_at] == ".":
        yield from premute(constraints.replace(".", "_", 1), start_at + 1)
    if constraints[start_at] == "#":
        yield from premute(constraints, start_at + 1)


def _premute(offset, constraints, pattern):
    if len(pattern) == 0:
        yield constraints
        return
    count = pattern[0]
    regex = "(?=([\?#]{" + str(count) + "}))"
    matches = list(re.finditer(regex, constraints[offset:]))
    for match in matches:
        s = match.start(1) + offset
        e = match.end(1) + offset
        head = constraints[:s] + ("#" * count)
        processed_by = constraints[s - 1]
        followed_by = constraints[e]
        tail = constraints[e + 1 :]
        if processed_by not in {".", "?", "_"}:
            continue
        if followed_by in {".", "?", "_"}:
            next_cons = head + "." + tail
        else:
            continue
        assert len(next_cons) == len(constraints)
        yield from premute(e, next_cons, pattern[1:])


if __name__ == "__main__":
    print(process(ingest()))
