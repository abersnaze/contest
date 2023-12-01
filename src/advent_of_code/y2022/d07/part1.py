#!python3

import fileinput
import re
from collections import defaultdict, Counter
from enum import Enum
from itertools import islice, product

lines = map(lambda x: x.strip(), fileinput.input())

cwd = []
drive = {}
for line in lines:
    if line.startswith("$ cd"):
        dir = line[5:]
        if dir == "..":
            cwd.pop()
        elif dir == "/":
            cwd = []
        else:
            cwd.append(dir)
    elif line.startswith("$ ls"):
        pass
    else:
        size, fname = line.split(" ")
        if size != "dir":
            c = drive
            for d in cwd:
                if d not in c:
                    c[d] = {}
                c = c[d]
            c[fname] = int(size)

print(drive)
total = 0


def walk(drive: dict, path):
    global total
    sum = 0
    for k, v in drive.items():
        if type(v) == dict:
            sum += walk(v, path + [k])
        else:
            sum += v
    if sum < 100_000:
        print(sum, path)
        total += sum
    return sum


walk(drive, [])
print(total)
