import math
from common.input import input

lights = 0
buttons = {}
for line in input():
    bits = line.split(" ")
    goal = list(map(lambda p: p[0], filter(lambda p: p[1] == "#", enumerate(bits[0][1:-1]))))
    for idx, button in enumerate(bits[1:-1]):
        buttons[idx] = list(map(int, button[1:-1].split(',')))
     = map(int, bits[-1][1:-1].split(','))

    print(goal, buttons, joltage)
 