from common.input import input
import re

insts = []
for line in input():
    batch = []
    batch.extend(re.finditer(r"(mul)\((\d{1,3}),(\d{1,3})\)", line))
    batch.extend(re.finditer(r"(do)\(\)", line))
    batch.extend(re.finditer(r"(don't)\(\)", line))
    batch.sort(key=lambda x: x.start())
    insts.extend(batch)


sum = 0
enable = True
for inst in insts:
    cmd = inst.group(1)
    if cmd == "do":
        enable = True
        continue
    if cmd == "don't":
        enable = False
        continue
    if not enable:
        continue
    a, b = int(inst.group(2)), int(inst.group(3))
    print(a, b, "=", a * b)
    sum += a * b

print("sum", sum)
# sum = 106780429
