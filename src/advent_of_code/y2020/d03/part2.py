#!python3

import sys
import re

content = sys.stdin.readlines()


def decent(delta):
    loc = (0, 0)

    tree_count = 0
    while loc[1] < len(content):
        row = content[loc[1]]
        terrain = row[loc[0] % (len(row) - 1)]
        if terrain == "#":
            tree_count += 1
        loc = loc[0] + delta[0], loc[1] + delta[1]
    return tree_count


# Right 1, down 1.
a = decent((1, 1))
# Right 3, down 1. (This is the slope you already checked.)
b = decent((3, 1))
# Right 5, down 1.
c = decent((5, 1))
# Right 7, down 1.
d = decent((7, 1))
# Right 1, down 2.
e = decent((1, 2))

print(a, b, c, d, e)
print(a * b * c * d * e)
