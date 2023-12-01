#!python3

import fileinput


def parse_line(line):
    return line[0], int(line.strip()[1:])


content = list(map(parse_line, fileinput.input()))

# content = [('F', 10), ('N', 3), ('F', 7), ('R', 90), ('F', 11)]


def rotate(facing, dir, amount):
    news = ["E", "N", "W", "S"]
    if dir == "R":
        return rotate(facing, "L", 360 - amount)
    x = news.index(facing)
    r = int(amount / 90)
    y = (x + r) % 4
    # print('\t', x, '+', '∆'+str(r), '=', y)
    return news[y]


facing = "E"
curr = (0, 0)

# test rotate
# print(rotate(facing, 'L', 0), 'E')
# print(rotate(facing, 'L', 90), 'N')
# print(rotate(facing, 'L', 180), 'W')
# print(rotate(facing, 'L', 270), 'S')
# print(rotate(facing, 'L', 360), 'E')
# print(rotate(facing, 'R', 0), 'E')
# print(rotate(facing, 'R', 90), 'S')
# print(rotate(facing, 'R', 180), 'W')
# print(rotate(facing, 'R', 270), 'N')
# print(rotate(facing, 'R', 360), 'E')

for cmd, amount in content:
    if cmd == "L" or cmd == "R":
        facing = rotate(facing, cmd, amount)
    if cmd == "F":
        cmd = facing
    if cmd == "E":
        curr = (curr[0] + amount, curr[1])
    if cmd == "W":
        curr = (curr[0] - amount, curr[1])
    if cmd == "N":
        curr = (curr[0], curr[1] + amount)
    if cmd == "S":
        curr = (curr[0], curr[1] - amount)

print(curr, abs(curr[0]) + abs(curr[1]))
