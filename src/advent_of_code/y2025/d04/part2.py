import regex as re
from common.input import input
from common.space import Space, adjacent8

s = Space.read(input())
o = s.copy()

print(s)

sum = 0
round = 1
while round > 0:
    round = 0
    for roll in s.keys():
        count = 0
        for adjacent in adjacent8(roll):
            if adjacent in s:
                count += 1
        if count < 4:
            del o[roll]
            sum += 1
            round += 1
    print(o)
    s = o
    o = s.copy()

print(sum)