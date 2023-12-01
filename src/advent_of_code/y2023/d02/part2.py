#!/usr/bin/env python3

from collections import defaultdict
from fileinput import input
from math import prod


def ingest(files=None):
    games = {}
    for line in input(files):
        id, reveals = parse(line)
        games[id] = reveals
    return games


def parse(line):
    game, cube_sets = line.strip().split(":")
    id = int(game[5:])
    reveals = []
    for cube_set in cube_sets.strip().split(";"):
        reveal = defaultdict(lambda: 0)
        for cubes in cube_set.split(","):
            count_count, cube_color = cubes.strip().split(" ")
            reveal[cube_color.strip()] += int(count_count.strip())
        reveals.append(reveal)
    return id, reveals


def power(game):
    min = defaultdict(lambda: 0)
    for reveal in game:
        for color, count in reveal.items():
            if count > min[color]:
                min[color] = count
    print(dict(min))
    return prod(min.values())


def process(data):
    return sum([power(game) for id, game in data.items()])


def output(data):
    print(data)


if __name__ == "__main__":
    output(process(ingest()))
