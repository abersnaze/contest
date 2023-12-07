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

    for range in ranges.values():
        range.sort(key=lambda r: r[1])

    return seeds, maps, ranges


def process(seeds, maps, ranges):
    seed_spans = []
    for i, seed in enumerate(seeds):
        if i % 2 != 0:
            continue
        seed_spans.append((seed, seeds[i + 1]))

    loc_spans = search_maps("seed", "location", seed_spans, maps, ranges)
    print(loc_spans)
    return min(map(lambda s: s[0], loc_spans))


def search_maps(curr_type, to_type, curr_spans, maps, ranges):
    print(curr_type, curr_spans)

    if curr_type == to_type:
        return curr_spans
    next_type = maps[curr_type]
    next_spans = []
    for span in curr_spans:
        curr_start, curr_length = span
        curr_end = curr_start + curr_length
        while curr_length > 0:
            for dst_start, src_start, leng in ranges[curr_type]:
                src_end = src_start + leng
                if src_start < curr_start and curr_start < src_end:
                    # start overlaps
                    next_span = (
                        (curr_start - src_start) + dst_start,
                        min(curr_length, leng),
                    )
                    next_spans.append(next_span)
                    curr_start += next_span[1]
                    curr_length -= next_span[1]
                    break
                if src_start < curr_end and curr_end < src_end:
                    # end overlaps
                    next_span = (dst_start, min(curr_length, leng))
                    next_spans.append(next_span)
                    curr_start += next_span[1]
                    curr_length -= next_span[1]
                    break
            else:
                next_spans.append(span)
                break

    return search_maps(next_type, to_type, next_spans, maps, ranges)


def output(data):
    print(data)


if __name__ == "__main__":
    output(process(*ingest()))
