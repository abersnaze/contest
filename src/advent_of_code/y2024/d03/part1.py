from common.input import input
import re

insts = []
for line in input():
    insts.extend(re.finditer(r"mul\((\d{1,3}),(\d{1,3})\)", line))


sum = 0
for inst in insts:
    a, b = int(inst.group(1)), int(inst.group(2))
    print(a, b, "=", a * b)
    sum += a * b

print("sum", sum)
# sum = 196826776
