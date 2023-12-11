#!/usr/bin/env python3

from fileinput import input
from functools import reduce
from itertools import cycle
import re


def ingest(files=None):
    lines = input(files)
    turns = cycle(iter(next(lines).strip()))
    _ = next(lines)
    edges = {}
    for i, line in enumerate(lines):
        # regex to parse AAA = (BBB, CCC)
        start, left, right = re.match(
            r"(\w+) = \((\w+), (\w+)\)", line.strip()
        ).groups()
        edges[start] = [left, right]
        pass
    return turns, edges


def process(turns, edges):
    curr = [k for k in edges.keys() if k[-1] == "A"]
    count = 0
    z_index = [0 for _ in curr]
    while not all([z != 0 for z in z_index]):
        turn = next(turns)
        curr = [move(turn, edges, c) for c in curr]
        count += 1
        for i, c in enumerate(curr):
            if c[-1] == "Z":
                z_index[i] = count

    f = reduce(lcm, z_index)
    return f


def lcm(a, b):
    return abs(a * b) // gcd(a, b)


def gcd(a, b):
    while b:
        a, b = b, a % b
    return a


def move(turn, edges, curr):
    return edges[curr][0 if turn == "L" else 1]


def output(data):
    print(data)


if __name__ == "__main__":
    output(process(*ingest()))
