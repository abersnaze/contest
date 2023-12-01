#!/usr/bin/env python3

from fileinput import input


def ingest(files=None):
    values = []
    for line in input(files):
        digits = [c for c in line if c.isdigit()]
        values.append(int(digits[0] + digits[-1]))
    return values


def process(data):
    return sum(data)


def output(data):
    print(data)


if __name__ == "__main__":
    output(process(ingest()))
