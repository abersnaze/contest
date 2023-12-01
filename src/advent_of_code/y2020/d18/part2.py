#!python3

import fileinput
import re
from collections import defaultdict
import sys


class N:
    def __init__(self, v):
        self.v = v

    def __mul__(self, other):
        return N(self.v + other.v)

    def __sub__(self, other):
        return N(self.v * other.v)

    def __repr__(self):
        return str(self.v)


def compute(chs: str):
    chs.replace("0", "N(0)")
    chs = chs.replace("1", "N(1)")
    chs = chs.replace("2", "N(2)")
    chs = chs.replace("3", "N(3)")
    chs = chs.replace("4", "N(4)")
    chs = chs.replace("5", "N(5)")
    chs = chs.replace("6", "N(6)")
    chs = chs.replace("7", "N(7)")
    chs = chs.replace("8", "N(8)")
    chs = chs.replace("9", "N(9)")
    chs = chs.replace("*", "-")
    chs = chs.replace("+", "*")
    return eval(chs, {}, {"N": N})


total = 0
for line in map(lambda x: x.strip().replace(" ", ""), fileinput.input()):
    x = compute(line)
    total += x.v
    print("eq = ", x)

print("total =", total)
