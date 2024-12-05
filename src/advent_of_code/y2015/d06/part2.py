#!/usr/bin/env python3

from hashlib import md5
from math import inf
from fileinput import input
from common.space import Space
from common.space import Dir


def ingest(files=None):
    return map(lambda l: l.strip(), input(files))


def is_nice(line):
    # It contains a pair of any two letters that appears at least twice in the string without overlapping,
    # like xyxy (xy) or aabcdefgaa (aa), but not like aaa (aa, but it overlaps).
    has_double_double = False
    for i in range(len(line) - 1):
        double = line[i] + line[i + 1]
        if double in line[i + 2 :]:
            has_double_double = True
            break
    if not has_double_double:
        return False

    # It contains at least one letter which repeats with exactly one letter between them, like xyx, abcdefeghi (efe), or even aaa.
    has_split_double = False
    for i in range(len(line) - 2):
        if line[i] == line[i + 2]:
            has_split_double = True
            break
    if not has_split_double:
        return False

    return True


def process(lines):
    count = sum([1 for line in lines if is_nice(line)])
    return count


def output(data):
    print(data)


if __name__ == "__main__":
    output(process(ingest()))
