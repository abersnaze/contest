import regex as re
from common.input import input

lines = input()

position = 50
zeros = 0
print("\t", position)
for line in lines:
    dir, clicks = line[0], int(line[1:])
    print(dir, clicks)

    if dir == "R":
        position += clicks
    else:
        position -= clicks
    position %= 100
    
    if position == 0:
        zeros += 1
    print("\t", position)

print(zeros)