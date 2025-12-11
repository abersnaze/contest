from collections import defaultdict
from functools import reduce
from operator import mul, add
import regex as re
from fileinput import input

lines = list(input())
height = len(lines)

sum = 0
op = ""
numbers = defaultdict(lambda: 0)
i = 0
for column in zip(*lines):
    if "".join(column).strip() == "":
        fn = mul if op == "*" else add
        value = reduce(fn, numbers.values())
        print(op, list(numbers.values()), value)
        sum += value
        op = ""
        i = 0
        numbers = defaultdict(lambda: 0)
    else:
        numbers[i] = int("".join(column[:-1]).strip())
        i+=1
        if column[-1] != " ":
            op = column[-1]

print(sum)