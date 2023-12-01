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
dirs = []


def walk(drive: dict, path):
    global dirs
    sum = 0
    for k, v in drive.items():
        if type(v) == dict:
            sum += walk(v, path + [k])
        else:
            sum += v
    dirs.append(sum)
    return sum


total = walk(drive, [])
free = 70000000 - total
more = 30000000 - free
dirs.sort()
print(dirs)

print(next(filter(lambda d: d > more, dirs)))
