#!/usr/bin/env python3

from collections import defaultdict
from fileinput import input
from math import prod

from common.space import Dir, Space, adjencent8


def ingest(files=None):
    s = Space(".")
    syms = {}
    for y, line in enumerate(input(files)):
        for x, c in enumerate(line.strip()):
            if c.isdigit():
                s[x, y] = int(c)
            elif c != ".":
                syms[(x, y)] = c
    return s, syms


def process(s, syms):
    parts = defaultdict(set)
    for sym in syms.keys():
        print("Checking", syms[sym], "at", sym)
        for p in adjencent8(sym):
            if p in s:
                parts[sym].add(read_part(s, p))
        s[sym] = 0
    total = 0
    for key in parts.keys():
        if syms[key] == "*" and len(parts[key]) == 2:
            total += prod(parts[key])
    return total


def read_part(s, p):
    digits = 0
    # find the first
    curr = p
    while curr in s:
        curr += Dir.W
    curr += Dir.E

    # curr is now the first digit
    while curr in s:
        digits = digits * 10 + s[curr]
        curr += Dir.E

    return digits


def output(data):
    print(data)


if __name__ == "__main__":
    output(process(*ingest()))
