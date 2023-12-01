#!/usr/bin/env python3

from math import inf
from fileinput import input
from common.space import Space


names = {
    "one": "1",
    "two": "2",
    "three": "3",
    "four": "4",
    "five": "5",
    "six": "6",
    "seven": "7",
    "eight": "8",
    "nine": "9",
}


def first_digit(line):
    i = 0
    while i < len(line):
        for d in names:
            if line[i:].startswith(d):
                return names[d]
        if line[i].isdigit():
            return line[i]
        i += 1


def last_digit(line):
    i = len(line) - 1
    while i >= 0:
        for d in names:
            if line[i:].startswith(d):
                return names[d]
        if line[i].isdigit():
            return line[i]
        i -= 1


def ingest():
    values = []
    for line in input():
        line = line.strip()
        value = int(first_digit(line) + last_digit(line))
        print(line, "=>", value)
        values.append(value)
    return values


def process(data):
    return sum(data)


def output(data):
    print(data)


if __name__ == "__main__":
    output(process(ingest()))
