#!python3

import fileinput
import re
from collections import defaultdict, Counter
import sys
from enum import Enum
from typing import List


def count_up(lines):
    total = 0
    bits = Counter()
    for line in lines:
        total += 1
        for i, bit in enumerate(line):
            if bit == "1":
                bits[i] += 1
        # print(bits)
    return total, bits


lines = list(map(lambda x: x.strip(), fileinput.input()))


def whittle(prefix: str, most: bool):
    matching = [l for l in lines if l.startswith(prefix)]
    print(prefix, len(matching))
    if len(matching) == 1:
        print("\t", matching[0])
        return int(matching[0], 2)
    total, bits = count_up(matching)

    i = len(prefix)
    count = bits[i]

    if count >= total / 2:
        if most:
            return whittle(prefix + "1", most)
        else:
            return whittle(prefix + "0", most)
    else:
        if most:
            return whittle(prefix + "0", most)
        else:
            return whittle(prefix + "1", most)


o2 = whittle("", True)
co2 = whittle("", False)

print(o2, "*", co2, "=", o2 * co2)
