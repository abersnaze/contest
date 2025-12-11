import regex as re
from common.input import input
from common.space import Space, adjacent8

s = Space.read(input())
o = s.copy()

print(s)

sum = 0
for roll in s.keys():
    count = 0
    for adjacent in adjacent8(roll):
        if adjacent in s:
            count += 1
    if count < 4:
        o[roll] = 'x'
        sum += 1

print(o)
print(sum)