#!python3

import sys
import re
from collections import defaultdict
import json

content = sys.stdin.readlines()

wraper = defaultdict(list)

p = re.compile("(.*) bags contain (.*).")
q = re.compile("(\d+) (.*) bags?")
for rule in content:
    outside, conts = p.match(rule.strip()).groups()
    insides = (
        [q.match(x.strip()).groups() for x in conts.split(",")]
        if conts != "no other bags"
        else []
    )
    print(f"'{outside}'", "->", insides)
    wraper[outside] = insides

print(json.dumps(wraper, indent="  "))

unchecked = defaultdict(lambda: 0)
unchecked["shiny gold"] += 1
total = defaultdict(lambda: 0)

while unchecked:
    outside, out_count = unchecked.popitem()
    print(out_count, outside)
    total[outside] += out_count
    for in_count, inside in wraper[outside]:
        print("\t", int(in_count) * out_count, inside)
        unchecked[inside] += int(in_count) * out_count

print(json.dumps(total, indent="  "))

print(sum(total.values()) - 1)
