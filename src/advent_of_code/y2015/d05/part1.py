#!/usr/bin/env python3

from hashlib import md5
from math import inf
from fileinput import input
from common.space import Space
from common.space import Dir


def ingest(files=None):
    return map(lambda l: l.strip(), input(files))


def is_nice(line):
    # It contains at least three vowels (aeiou only), like aei, xazegov, or aeiouaeiouaeiou.
    vowels = set("aeiou")
    if sum([1 for c in line if c in vowels]) < 3:
        return False

    # It contains at least one letter that appears twice in a row, like xx, abcdde (dd), or aabbccdd (aa, bb, cc, or dd).
    has_double = False
    for i in range(len(line) - 1):
        if line[i] == line[i + 1]:
            has_double = True
    if not has_double:
        return False

    # It does not contain the strings ab, cd, pq, or xy, even if they are part of one of the other requirements.
    not_alloweds = set(["ab", "cd", "pq", "xy"])
    for not_allowed in not_alloweds:
        if not_allowed in line:
            return False

    return True


def process(lines):
    count = sum([1 for line in lines if is_nice(line)])
    return count


def output(data):
    print(data)


if __name__ == "__main__":
    output(process(ingest()))
