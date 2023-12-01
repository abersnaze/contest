#!python3

import fileinput
import re
from collections import defaultdict, Counter
from enum import Enum
from itertools import islice, product

line = next(fileinput.input())


def find_start(s):
    for i in range(0, len(s) - 14):
        if len(set(s[i : i + 14])) == 14:
            return i + 14


print(find_start("mjqjpqmgbljsphdztnvjfqwrcgsmlb"), 19)
print(find_start("bvwbjplbgvbhsrlpgdmjqwftvncz"), 23)
print(find_start("nppdvjthqldpwncqszvftbrmjlhg"), 23)
print(find_start("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"), 29)
print(find_start("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"), 26)

print(find_start(line))
