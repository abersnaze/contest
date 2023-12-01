#!python3

import sys
import re

content = sys.stdin.readlines()

pps = []
pp = []
for line in content:
    if line == "\n":
        pps.append(pp)
        pp = []
    else:
        pp.extend(line.strip().split(" "))
if len(pp) > 0:
    pps.append(pp)

required = set(
    [
        "byr",  # (Birth Year)
        "iyr",  # (Issue Year)
        "eyr",  # (Expiration Year)
        "hgt",  # (Height)
        "hcl",  # (Hair Color)
        "ecl",  # (Eye Color)
        "pid",  # (Passport ID)
        # "cid",# (Country ID)
    ]
)
count = 0
for pp in pps:
    keys = set([x.split(":")[0] for x in pp])
    if keys.issuperset(required):
        print("pass", keys)
        count += 1
    else:
        print("fail", keys)

print(count)
