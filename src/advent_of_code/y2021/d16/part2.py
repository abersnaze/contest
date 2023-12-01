#!python3

import fileinput
import re
from collections import defaultdict, Counter, deque
from enum import Enum
from itertools import islice, product
import math
from typing import List

lines = list(map(lambda x: x.strip(), fileinput.input()))


def bits(line):
    i = 0
    b = 8
    byts = bytes.fromhex(line)
    for i in range(len(byts)):
        for b in range(7, -1, -1):
            yield ((byts[i] >> b) & 1)


bs = bits(lines[0])
# bs = map(int, iter("110100101111111000101000"))
# bs = map(int, iter("00111000000000000110111101000101001010010001001000000000"))
# bs = map(int, iter("11101110000000001101010000001100100000100011000001100000"))


def num(n):
    v = 0
    for i in range(n):
        v = v << 1 | next(bs)
    return v


def process_packet():
    pver = num(3)
    ptype = num(3)

    if ptype == 4:
        return process_literal_packet(pver, ptype)
    else:
        return process_operator_packet(pver, ptype)


class Pkt:
    pver: int
    ptype: int
    size: int

    def __init__(self, pver, ptype, used) -> None:
        self.pver = pver
        self.ptype = ptype
        self.size = used

    def __str__(self) -> str:
        return self.str("")


class Lit(Pkt):
    n: int

    def __init__(self, pver, ptype, used, n) -> None:
        super().__init__(pver, ptype, used)
        self.n = n

    def ver_sum(self) -> int:
        return self.pver

    def str(self, indent) -> str:
        return f"{indent}L(v:{self.pver}, t:{self.ptype}, s:{self.size}, n:{self.n})"

    def eval(self) -> int:
        return self.n


class Op(Pkt):
    pver: int
    ptype: int
    sub: List[Pkt]

    def __init__(self, pver, ptype, used) -> None:
        super().__init__(pver, ptype, used)
        self.pver = pver
        self.ptype = ptype
        self.sub = []

    def ver_sum(self) -> int:
        return self.pver + sum(map(lambda x: x.ver_sum(), self.sub))

    def str(self, indent) -> str:
        s = f"{indent}O(v:{self.pver}, t:{self.ptype}, s:{self.size} [\n"
        for x in self.sub:
            s += x.str(indent + "  ") + "\n"
        s += f"{indent}])"
        return s

    def eval(self) -> int:
        if self.ptype == 0:
            return sum([s.eval() for s in self.sub])
        elif self.ptype == 1:
            return math.prod([s.eval() for s in self.sub])
        elif self.ptype == 2:
            return min([s.eval() for s in self.sub])
        elif self.ptype == 3:
            return max([s.eval() for s in self.sub])
        elif self.ptype == 5:
            return 1 if self.sub[0].eval() > self.sub[1].eval() else 0
        elif self.ptype == 6:
            return 1 if self.sub[0].eval() < self.sub[1].eval() else 0
        elif self.ptype == 7:
            return 1 if self.sub[0].eval() == self.sub[1].eval() else 0


def process_literal_packet(pver, type):
    used = 6
    n = 0
    while next(bs) == 1:
        n = n << 4 | num(4)
        used += 5
    n = n << 4 | num(4)
    used += 5
    return Lit(pver, type, used, n)


def process_operator_packet(pver, ptype):
    len_type = next(bs)
    used = 7

    if len_type == 0:
        max_used = num(15)
        used += 15
        max_used += used
        pkt = Op(pver, ptype, -1)
        while used < max_used:
            sub_pkt = process_packet()
            used += sub_pkt.size
            pkt.sub.append(sub_pkt)
        pkt.size = used
        return pkt
    else:
        max_pkt = num(11)
        used += 11
        pkt_used = 0
        pkt = Op(pver, ptype, -1)
        while pkt_used < max_pkt:
            sub_pkt = process_packet()
            used += sub_pkt.size
            pkt_used += 1
            pkt.sub.append(sub_pkt)
        pkt.size = used
        return pkt


pkt = process_packet()
print(str(pkt))
print(pkt.eval())
