#!/usr/bin/env python3

from fileinput import input
import re


def ingest(files=None):
    lines = input(files)
    turns = next(lines).strip()
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
    curr = "AAA"
    count = 0
    while curr != "ZZZ":
        for turn in turns:
            next = edges[curr][0 if turn == "L" else 1]
            count += 1
            curr = next
    return count


def output(data):
    print(data)


if __name__ == "__main__":
    output(process(*ingest()))
