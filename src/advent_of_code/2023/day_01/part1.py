#!/usr/bin/env python3

from math import inf
from fileinput import input
from common.space import Space


def ingest():
    values = []
    for line in input():
        digits = [c for c in line if c.isdigit()]
        values.append(int(digits[0] + digits[-1]))
    return values


def process(data):
    return sum(data)


def output(data):
    print(data)


if __name__ == "__main__":
    output(process(ingest()))
