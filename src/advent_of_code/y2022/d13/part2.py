#!python3

import fileinput
import re
from collections import defaultdict, Counter
from enum import Enum
from itertools import islice, product
import math
from functools import reduce, cmp_to_key

divider_a = [[2]]
divider_b = [[6]]
packets = [divider_a, divider_b]
lines = map(lambda x: x.strip(), fileinput.input())
for line in lines:
    if line == "":
        p = []
        continue
    packets.append(eval(line))


def correct(left, right, depth=""):
    if left is None:
        print(depth, left, right, "correct")
        return True
    if right is None:
        print(depth, left, right, "incorrect")
        return False
    if type(left) == int and type(right) == int:
        if left < right:
            print(depth, left, right, "correct")
            return True
        if left > right:
            print(depth, left, right, "incorrect")
            return False
        return None
    print(depth, left, right, "before")
    if type(left) == int:
        left = [left]
    if type(right) == int:
        right = [right]
    if len(left) > len(right):
        print(depth, left, right, "extends right")
        right = right + [None for i in range(len(left) - len(right))]
    if len(left) < len(right):
        print(depth, left, right, "extends left")
        left = left + [None for i in range(len(right) - len(left))]
    print(depth, left, right, "after")
    for subpacket in zip(left, right):
        c = correct(*subpacket, depth=depth + "\t")
        if c is not None:
            return c
    return None


def compare_packets(a, b):
    return -1 if correct(a, b) else 1


packets.sort(key=cmp_to_key(compare_packets))

print("\n".join(map(str, packets)))

loc_a = packets.index(divider_a) + 1
loc_b = packets.index(divider_b) + 1

print(loc_a, "*", loc_b, "=", loc_a * loc_b)
