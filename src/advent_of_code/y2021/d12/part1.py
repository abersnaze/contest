#!python3

import fileinput
import re
from collections import defaultdict, Counter
from enum import Enum
from itertools import islice, product

edges = defaultdict(list)

lines = map(lambda x: x.strip(), fileinput.input())
for line in lines:
    start, end = line.split("-")
    edges[start].append(end)
    edges[end].append(start)


finished = []
unfinished = [["start"]]
while unfinished:
    path = unfinished.pop()
    for dst in edges[path[-1]]:
        if dst == dst.lower() and dst in path:
            continue
        nxt = path.copy()
        nxt.append(dst)
        if dst == "end":
            finished.append(nxt)
        else:
            unfinished.append(nxt)

for path in finished:
    print(",".join(path))

print(len(finished))
