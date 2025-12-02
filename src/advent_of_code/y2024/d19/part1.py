import regex as re
from common.input import input

lines = input()

avail_patterns = next(lines).split(", ")
_ = next(lines)

foo = "^(" + "|".join(avail_patterns) + ")+$"
pattern = re.compile(foo)

total = 0
for line in lines:
    print(line)
    new_var = pattern.fullmatch(line)
    if new_var:
        print("\tYES")
        total += 1
    else:
        print("\tNO")

print(total)
