#!python3

import fileinput
import re
from collections import defaultdict, Counter
from itertools import islice, product, repeat
from functools import reduce
from math import inf
from enum import Enum

fm_sdigit = {"2": 2, "1": 1, "0": 0, "-": -1, "=": -2}
to_sdigit = {n: s for s, n in fm_sdigit.items()}


def fm_snafu(s):
    n = 0
    place = 1
    for digit in reversed(s):
        n += fm_sdigit[digit] * place
        place *= 5
    return n


def to_snafu(n):
    b5 = []
    while n > 0:
        digit = n % 5
        n = n // 5
        if digit > 2:
            n += 1
            digit -= 5
        b5.append(digit)
    return "".join(map(to_sdigit.get, reversed(b5)))


lines = list(map(lambda x: x.rstrip(), fileinput.input()))
total = 0
for line in lines:
    n = fm_snafu(line)
    print(line, "\t", n)
    total += n

print(total)
print(to_snafu(total))
