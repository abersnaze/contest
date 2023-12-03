#!/usr/bin/env python3

from math import inf
from fileinput import input
from common.space import Space
from common.space import Dir


def ingest(files=None):
    def dirs(c):
        return {
            "^": Dir.N,
            "v": Dir.S,
            ">": Dir.E,
            "<": Dir.W,
        }[c]

    return map(dirs, next(input(files)).strip())


def process(data):
    s = Space(0)
    start = (0, 0)
    s[start] += 1
    robo = start
    santa = start
    for i, move in enumerate(data):
        if i % 2 == 0:
            santa += move
            s[santa] += 1
        else:
            robo += move
            s[robo] += 1
    return len(s)


def output(data):
    print(data)


if __name__ == "__main__":
    output(process(ingest()))
