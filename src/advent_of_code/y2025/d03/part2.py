import regex as re
from common.input import input

lines = input()

def max_digit(bank, i):
    digit = max(bank[:-(i - 1)] if i > 1 else bank)
    if i == 1:
        return digit
    return digit + max_digit(bank[bank.index(digit) + 1:], i-1)

sum = 0
for line in lines:
    jolts = int(max_digit(line, 12))
    print(line, "->", jolts)
    sum += jolts
    
print(sum)
