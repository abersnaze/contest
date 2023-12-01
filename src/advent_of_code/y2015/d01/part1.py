#!/usr/bin/env python3

from math import inf
from fileinput import input
from common.space import Space


def ingest(files=None):
    return next(input(files)).strip()


def process(data):
    floor = 0
    for i, c in enumerate(data):
        if c == "(":
            floor += 1
        elif c == ")":
            floor -= 1
    return floor


def output(data):
    print(data)


if __name__ == "__main__":
    output(process(ingest()))
