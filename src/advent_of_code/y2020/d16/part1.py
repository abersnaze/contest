#!python3

import fileinput
import re
from collections import defaultdict

rule_pattern = re.compile("(.*): (.*)-(.*) or (.*)-(.*)")

rules = defaultdict(list)
your_ticket = None
othr_tickets = []
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
        ns = list(range(int(a), int(b) + 1))
        ns.extend(range(int(c), int(d) + 1))
        for n in ns:
            rules[n].append(name)
        print(name, a, b, c, d)
    else:
        ticket = list(map(int, line.split(",")))
        print(your, ticket)
        if your:
            your_ticket = ticket
        else:
            othr_tickets.append(ticket)

print(rules)

sum = 0
for othr_ticket in othr_tickets:
    for value in othr_ticket:
        if value not in rules:
            print(value, "not in rules")
            sum += value

print(sum)
