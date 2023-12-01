#!python3

import fileinput


def parse_line(line):
    return line[0], int(line.strip()[1:])


content = list(map(parse_line, fileinput.input()))

# content = [('F', 10), ('N', 3), ('F', 7), ('R', 90), ('F', 11)]


def rotate(facing, dir, amount):
    if dir == "R":
        return rotate(facing, "L", 360 - amount)
    r = int(amount / 90)
    if r == 0 or r == 4:
        return facing
    if r == 1:
        return (-facing[1], facing[0])
    if r == 2:
        return (-facing[0], -facing[1])
    if r == 3:
        return (facing[1], -facing[0])


facing = (10, 1)
curr = (0, 0)

# test rotate
# print(rotate(facing, 'L', 0), (10, 1))
# print(rotate(facing, 'L', 90), 'N')
# print(rotate(facing, 'L', 180), 'W')
# print(rotate(facing, 'L', 270), 'S')
# print(rotate(facing, 'L', 360), (10, 1))
# print(rotate(facing, 'R', 0), (10, 1))
# print(rotate(facing, 'R', 90), 'S')
# print(rotate(facing, 'R', 180), 'W')
# print(rotate(facing, 'R', 270), 'N')
# print(rotate(facing, 'R', 360), (10, 1))

for cmd, amount in content:
    # print(curr, facing, '--->', cmd, amount)
    if cmd == "L" or cmd == "R":
        facing = rotate(facing, cmd, amount)
    if cmd == "F":
        # print('∆', facing[0]*amount, facing[1]*amount)
        curr = curr[0] + facing[0] * amount, curr[1] + facing[1] * amount
    if cmd == "E":
        facing = (facing[0] + amount, facing[1])
    if cmd == "W":
        facing = (facing[0] - amount, facing[1])
    if cmd == "N":
        facing = (facing[0], facing[1] + amount)
    if cmd == "S":
        facing = (facing[0], facing[1] - amount)

print(curr, abs(curr[0]) + abs(curr[1]))
