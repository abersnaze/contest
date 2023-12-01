#!python3

import sys
import re

content = sys.stdin.readlines()

loc = (0, 0)
delta = (3, 1)

tree_count = 0
while loc[1] < len(content):
    row = content[loc[1]]
    terrain = row[loc[0] % (len(row) - 1)]
    if terrain == "#":
        tree_count += 1
    print(loc, terrain, tree_count)
    loc = loc[0] + delta[0], loc[1] + delta[1]

print(tree_count)
