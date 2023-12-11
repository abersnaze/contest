#!/usr/bin/env python3

from collections import Counter, defaultdict
from fileinput import input
from functools import cmp_to_key
from math import ceil, floor, prod, sqrt


def ingest(files=None):
    sensors = []
    for i, line in enumerate(input(files)):
        sensors.append(list(map(int, line.strip().split())))
    return sensors


def predict(values):
    last = values[-1]
    uniq = set(values)
    if len(uniq) == 1:
        return last
    # difference between each value and the next
    return predict([values[i + 1] - values[i] for i in range(len(values) - 1)]) + last


def process(sensors):
    nexts = []
    for values in sensors:
        nexts.append(predict(values))
    return sum(nexts)


if __name__ == "__main__":
    print(process(ingest()))
