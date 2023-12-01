#!python3

import fileinput
import re
from collections import defaultdict
import json

rule_pattern = re.compile("(.*): (.*)-(.*) or (.*)-(.*)")

rules = defaultdict(list)
your_ticket = None
othr_tickets = []
all_names = set()
for line in map(lambda x: x.strip(), fileinput.input()):
    if line == "":
        continue
    r = rule_pattern.match(line)
    if line == "your ticket:":
        your = True
        continue
    if line == "nearby tickets:":
        your = False
        continue
    if r:
        name, a, b, c, d = r.groups()
        all_names.add(name)
        ns = list(range(int(a), int(b) + 1))
        ns.extend(range(int(c), int(d) + 1))
        for n in ns:
            rules[n].append(name)
        # print(name, a, b, c, d)
    else:
        ticket = list(map(int, line.split(",")))
        # print(your, ticket)
        if your:
            your_ticket = ticket
        else:
            othr_tickets.append(ticket)

# print(json.dumps(rules, indent=2))

valid_tickets = []
for othr_ticket in othr_tickets:
    valid = True
    for value in othr_ticket:
        if value not in rules:
            valid = False
    if valid:
        valid_tickets.append(othr_ticket)

print(len(valid_tickets))

fields = {}
while len(fields) < len(your_ticket):
    for idx in range(0, len(your_ticket)):
        valid_names = all_names - set(fields.keys())
        for valid_ticket in valid_tickets:
            value = valid_ticket[idx]
            rule_names = rules[value]
            valid_names = valid_names.intersection(rule_names)
        if len(valid_names) == 1:
            name = next(iter(valid_names))
            # print(idx, name)
            fields[name] = idx


product = 1
for name, idx in fields.items():
    if name.startswith("depart"):
        print(name, idx)
        product *= your_ticket[idx]
print(product)
