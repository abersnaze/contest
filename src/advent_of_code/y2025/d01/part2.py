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
        step = 1
    else:
        step = -1

    for _ in range(clicks):
        position += step
        position %= 100
        if position == 0:
            zeros += 1
            print("\tZERO")
    
    print("\t", position)

print(zeros)