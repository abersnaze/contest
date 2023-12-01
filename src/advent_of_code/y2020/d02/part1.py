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
    ls = [l for l in pw if l == ltr]
    count_ltr = len(ls)
    if count_ltr < int(low):
        print(pw, f'expected at least {low} "{ltr}"s found {count_ltr}')
    elif int(high) < count_ltr:
        print(pw, f'expected at most {high} "{ltr}"s found {count_ltr}')
    else:
        valid += 1

print(valid)
