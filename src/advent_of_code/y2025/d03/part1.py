import regex as re
from common.input import input

lines = input()

sum = 0
for line in lines:
    first_digit = max(line[:-1])
    second_digit = max(line[line.index(first_digit) + 1:])
    jolts = int(first_digit + second_digit)
    print(line, "->", jolts)
    sum += jolts
    
print(sum)
