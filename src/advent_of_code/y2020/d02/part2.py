#!python3

import sys
import re

content = sys.stdin.readlines()

# you may also want to remove whitespace characters like `\n` at the end of each line
p = re.compile("(\d+)-(\d+) (\w): (\w+)")
content = [p.match(x).groups() for x in content]
# tuple low, high, letter, password

valid = 0
for low, high, ltr, pw in content:
    low = int(low)
    high = int(high)
    one = pw[low - 1] == ltr
    two = pw[high - 1] == ltr

    if one ^ two:
        valid += 1
    else:
        print(pw, f"expected {low} xor {high} to be {ltr}", one, two)

print(valid)
