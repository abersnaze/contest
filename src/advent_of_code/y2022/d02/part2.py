#!python3

import fileinput
import re
from collections import defaultdict, Counter
from enum import Enum
from itertools import islice, product


class Them(Enum):
    A = 1  # Rock
    B = 2  # Paper
    C = 3  # Scissors


class Counter(Enum):
    X = {Them.A: 3, Them.B: 1, Them.C: 2}  # Lose
    Y = {Them.A: 1 + 3, Them.B: 2 + 3, Them.C: 3 + 3}  # Draw
    Z = {Them.A: 2 + 6, Them.B: 3 + 6, Them.C: 1 + 6}  # Win


lines = map(lambda x: x.strip(), fileinput.input())

my_scores = []
for line in lines:
    t, u = line.split(" ")
    t = Them[t]
    u = Counter[u]
    my_scores.append(u.value[t])

print(my_scores)
print(sum(my_scores))
