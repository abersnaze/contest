#!python3

import fileinput
from functools import reduce
import re
from collections import defaultdict, Counter, deque
from enum import Enum
from itertools import islice, product
import math
from typing import List, Tuple


def sf_explode(sf):
    for i in range(len(sf) - 1):
        if sf[i][0] == 5 and sf[i + 1][0] == 5:
            if i == 0:
                prefix = []
            else:
                prefix = sf[: i - 1] + [(sf[i - 1][0], sf[i][1] + sf[i - 1][1])]
            if i + 2 == len(sf):
                sufix = []
            else:
                sufix = [(sf[i + 2][0], sf[i + 1][1] + sf[i + 2][1])] + sf[i + 3 :]
            return prefix + [(4, 0)] + sufix
    return sf


def sf_split(sf):
    for i in range(len(sf)):
        if sf[i][1] >= 10:
            return (
                sf[:i]
                + [(sf[i][0] + 1, sf[i][1] // 2), (sf[i][0] + 1, (sf[i][1] + 1) // 2)]
                + sf[i + 1 :]
            )
    return sf


def sf_reduce(sf):
    prev = None
    curr = sf
    while prev != curr:
        prev, curr = curr, sf_explode(curr)
        if prev == curr:
            prev, curr = curr, sf_split(curr)
    return curr


def sf_add(a, b):
    return sf_reduce([(d + 1, v) for d, v in a + b])


def sf_magnitude(sf):
    while len(sf) > 1:
        for i in range(len(sf) - 1):
            if sf[i][0] == sf[i + 1][0]:
                m = (sf[i][0] - 1, sf[i][1] * 3 + sf[i + 1][1] * 2)
                sf = sf[:i] + [m] + sf[i + 2 :]
                break
    return sf[0][1]


def sf_test(op, input, output: str):
    input = parse(input) if type(input) == str else input
    act = op(input)
    exp = parse(output) if type(output) == str else output
    assert act == exp, str(act) + " != " + str(exp)


def parse(line: str) -> List[Tuple[int, int]]:
    sf = []
    nest = 0
    for token in line:
        if token == "[":
            nest += 1
        elif token == "]":
            nest -= 1
        elif token == ",":
            pass
        else:
            sf.append((nest, int(token)))
    return sf


sf_test(sf_explode, "[[[[[9,8],1],2],3],4]", "[[[[0,9],2],3],4]")
sf_test(sf_explode, "[7,[6,[5,[4,[3,2]]]]]", "[7,[6,[5,[7,0]]]]")
sf_test(sf_explode, "[[6,[5,[4,[3,2]]]],1]", "[[6,[5,[7,0]]],3]")
sf_test(
    sf_explode,
    "[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]",
    "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]",
)
sf_test(
    sf_explode, "[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]", "[[3,[2,[8,0]]],[9,[5,[7,0]]]]"
)
sf_test(sf_split, [(0, 10)], "[5,5]")
sf_test(sf_split, [(0, 11)], "[5,6]")
sf_test(sf_split, [(0, 10)], "[5,5]")
sf_test(
    sf_reduce,
    "[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]",
    "[[[[0,7],4],[[7,8],[6,0]]],[8,1]]",
)
sf_test(sf_magnitude, "[[1,2],[[3,4],5]]", 143)

lines = list(map(lambda x: x.strip(), fileinput.input()))

largest = 0
largest_a = None
largest_b = None
for a, b in product(lines, lines):
    if a == b:
        continue
    mag = sf_magnitude(sf_add(parse(a), parse(b)))
    if mag > largest:
        largest = mag
        largest_a = a
        largest_b = b


print(largest_a, " + ", largest_b)
print(largest)
