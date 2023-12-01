#!/usr/bin/env python3

from collections import defaultdict
from fileinput import input


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


def is_posible(game):
    for reveal in game:
        if reveal["red"] > 12:
            return False
        if reveal["green"] > 13:
            return False
        if reveal["blue"] > 14:
            return False
    return True


def process(data):
    return sum([id for id, game in data.items() if is_posible(game)])


def output(data):
    print(data)


if __name__ == "__main__":
    output(process(ingest()))
