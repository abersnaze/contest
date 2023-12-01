#!python3

import fileinput
import re
from collections import defaultdict, Counter
from enum import Enum
from itertools import islice, product
import math
from functools import reduce

packets = []
lines = map(lambda x: x.strip(), fileinput.input())
p = []
for line in lines:
    if line == "":
        packets.append(tuple(p))
        p = []
        continue
    p.append(eval(line))


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


total = 0
for i, packet in enumerate(packets):
    print("##########", i)
    if correct(*packet):
        total += i + 1
        print(i, "is correct")

print(total)
