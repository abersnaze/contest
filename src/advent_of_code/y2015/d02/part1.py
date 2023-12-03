#!/usr/bin/env python3

from math import inf
from fileinput import input
from common.space import Space


def ingest(files=None):
    return map(lambda x: tuple(map(int, x.strip().split("x"))), input(files))


def process(data):
    def wrap(w, l, h):
        smallest = min(w * l, w * h, h * l)
        return 2 * l * w + 2 * w * h + 2 * h * l + smallest

    return sum(map(lambda x: wrap(*x), data))


def output(data):
    print(data)


if __name__ == "__main__":
    output(process(ingest()))
