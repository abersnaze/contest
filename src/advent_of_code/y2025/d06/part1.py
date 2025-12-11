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
for column in zip(*lines):
    spaces = True
    for i, digit in enumerate(column):
        if digit != " ":
            if i != height-1:
                spaces = False
                numbers[i] *= 10
                numbers[i] += int(digit)
            else:
                spaces = False
                op += digit
    if spaces:
        fn = mul if op == "*" else add
        value = reduce(fn, numbers.values())
        print(op, numbers, value)
        sum += value
        
        op = ""
        numbers = defaultdict(lambda: 0)

print(sum)