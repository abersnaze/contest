import regex as re
from common.input import input

lines = input()
invalid = []

def is_valid(i):
    s = str(i)
    l = len(s)
    if l % 2 == 1:
        return True
    start, end = s[:l//2], s[l//2:]
    if start == end:
        return False

for line in lines:
    smol, larg = line.split("-")
    for i in range(int(smol), int(larg), 1):
        if is_valid(i) is False:
            invalid.append(i)

print(invalid)
print(sum(invalid))