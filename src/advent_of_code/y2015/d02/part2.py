#!/usr/bin/env python3

from math import inf, prod
from fileinput import input
from common.space import Space


def ingest(files=None):
    return map(lambda x: tuple(map(int, x.strip().split("x"))), input(files))


def process(data):
    def wrap(w, l, h):
        bow = prod([w, l, h])
        ribbon = 2 * (w + l + h - max(w, l, h))
        return bow + ribbon

    return sum(map(lambda x: wrap(*x), data))


def output(data):
    print(data)


if __name__ == "__main__":
    output(process(ingest()))

