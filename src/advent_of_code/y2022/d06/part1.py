#!python3

import fileinput
import re
from collections import defaultdict, Counter
from enum import Enum
from itertools import islice, product

line = next(fileinput.input())


def find_start(s):
    for i in range(0, len(s) - 4):
        if len(set(s[i : i + 4])) == 4:
            return i + 4


print(find_start("bvwbjplbgvbhsrlpgdmjqwftvncz"), 5)
print(find_start("nppdvjthqldpwncqszvftbrmjlhg"), 6)
print(find_start("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"), 10)
print(find_start("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"), 11)

print(find_start(line))
