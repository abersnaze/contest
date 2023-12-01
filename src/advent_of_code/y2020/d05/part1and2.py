#!python3

import sys
import re

content = sys.stdin.readlines()

tickets = [
    int(
        x.strip()
        .replace("F", "0")
        .replace("B", "1")
        .replace("R", "1")
        .replace("L", "0"),
        2,
    )
    for x in content
]

# part 1
print(max(tickets))

# part 2
tickets.sort()
expected = 6
for ticket in tickets:
    if ticket != expected:
        print(ticket, expected)
    expected = ticket + 1
