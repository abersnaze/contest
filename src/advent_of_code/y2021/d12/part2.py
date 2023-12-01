#!python3

import fileinput
import re
from collections import defaultdict, Counter
from enum import Enum
from itertools import islice, product

edges = defaultdict(list)
# the caves that we can visit twice
dbls = set()

lines = map(lambda x: x.strip(), fileinput.input())
for line in lines:
    start, end = line.split("-")
    edges[start].append(end)
    edges[end].append(start)
    if start.lower() == start:
        dbls.add(start)
    if end.lower() == end:
        dbls.add(end)
dbls.remove("start")
dbls.remove("end")


def visit(allowd_twice):
    finished = []
    unfinished = [["start"]]
    while unfinished:
        path = unfinished.pop()
        for dst in edges[path[-1]]:
            if dst == allowd_twice:
                if path.count(dst) >= 2:
                    continue
            elif dst == dst.lower() and dst in path:
                continue
            nxt = path.copy()
            nxt.append(dst)
            if dst == "end":
                finished.append(tuple(nxt))
            else:
                unfinished.append(nxt)
    return finished


allyall = set()
for dbl in dbls:
    for path in visit(dbl):
        allyall.add(path)

for path in allyall:
    print(",".join(path))

print(len(allyall))
