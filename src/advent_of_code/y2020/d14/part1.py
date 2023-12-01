#!python3

import fileinput
import re
from collections import defaultdict

mask_patter = re.compile("mask = ([X01]{36})")
mem_patter = re.compile("mem\[(\d+)\] = (\d+)\n")

mem = defaultdict(lambda: 0)
mask = lambda value: value
for line in fileinput.input():
    match = mask_patter.match(line)
    if match:
        bits_clr = "".join(["0" if x == "0" else "1" for x in match.groups()[0]])
        bits_set = "".join(["1" if x == "1" else "0" for x in match.groups()[0]])
        print("mask", bits_clr, bits_set)
        mask_clr = int(bits_clr, 2)
        mask_set = int(bits_set, 2)
        mask = lambda value: value & mask_clr | mask_set
    else:
        match = mem_patter.match(line)
        if match:
            addr = int(match.groups()[0])
            value = int(match.groups()[1])
            print("mem", addr, value, mask(value))
            mem[addr] = mask(value)
        else:
            print("failed to match", line)

print(mem)
sum = 0
for value in mem.values():
    sum += value

print(sum)
