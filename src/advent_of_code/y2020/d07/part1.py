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
    for inside in insides:
        wraper[inside[1]].append(outside)

print(json.dumps(wraper, indent="  "))

unchecked = set(["shiny gold"])
checked = set()
valid = set()

while unchecked:
    color = unchecked.pop()
    outsides = wraper[color]
    for outside in outsides:
        print(color, "in", outside)
        if outside not in checked:
            print("\tadding to queue to check")
            unchecked.add(outside)
            if outside not in valid:
                print("\tadding valid", outside)
                valid.add(outside)

print(valid)
print(len(valid))
