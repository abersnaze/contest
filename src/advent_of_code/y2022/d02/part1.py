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


class Us(Enum):
    X = 1  # Rock
    Y = 2  # Paper
    Z = 3  # Scissors


win = {(2, 1), (3, 2), (1, 3)}

lines = map(lambda x: x.strip(), fileinput.input())

my_scores = []
for line in lines:
    t, u = line.split(" ")
    t = Them[t]
    u = Us[u]
    if (u.value, t.value) in win:
        my_scores.append(u.value + 6)
    elif (t.value, u.value) in win:
        my_scores.append(u.value)
    else:
        my_scores.append(u.value + 3)

print(my_scores)
print(sum(my_scores))
