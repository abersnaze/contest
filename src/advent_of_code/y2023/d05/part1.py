#!/usr/bin/env python3

from bisect import bisect
from collections import defaultdict
from fileinput import input

from common.space import Dir, Space, adjencent8


def ingest(files=None):
    lines = input(files)
    seeds = list(map(int, next(lines).split(":")[1].strip().split(" ")))

    maps = dict()
    ranges = dict()
    curr_map = None
    for line in map(lambda l: l.strip(), lines):
        if line == "":
            continue
        if line.endswith(":"):
            curr_map = []
            from_type, to_type = line[:-5].split("-to-")
            maps[from_type] = to_type
            ranges[from_type] = curr_map
        else:
            curr_map.append(list(map(int, line.split(" "))))

    return seeds, maps, ranges


def process(seeds, maps, ranges):
    locations = []
    for seed in seeds:
        loc = search_maps("seed", "location", seed, maps, ranges)
        locations.append(loc)
    return min(locations)


def search_maps(curr_type, to_type, curr_value, maps, ranges):
    if curr_type == to_type:
        return curr_value
    next_type = maps[curr_type]
    for range in ranges[curr_type]:
        if range[1] < curr_value and curr_value < (range[1] + range[2]):
            # found the range
            next_value = curr_value - range[1] + range[0]
            return search_maps(next_type, to_type, next_value, maps, ranges)
    # not mapped
    return search_maps(next_type, to_type, curr_value, maps, ranges)


def output(data):
    print(data)


if __name__ == "__main__":
    output(process(*ingest()))
