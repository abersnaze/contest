from common.input import input
from common.space import Dir4, Space

lines = input()
space = Space()
for y, line in enumerate(lines):
    if line == "":
        break
    for x, char in enumerate(line):
        if char == "#":
            space[(2 * x + 0, y)] = "#"
            space[(2 * x + 1, y)] = "#"
        if char == "O":
            space[(2 * x + 0, y)] = "["
            space[(2 * x + 1, y)] = "]"
        if char == "@":
            space[(2 * x + 0, y)] = "@"
            space[(2 * x + 1, y)] = "."

print(space)

moves = []
for line in lines:
    for c in line:
        if c == "^":
            moves.append(Dir4.N)
        elif c == "v":
            moves.append(Dir4.S)
        elif c == "<":
            moves.append(Dir4.W)
        elif c == ">":
            moves.append(Dir4.E)

# print(moves)
robot = next(iter(space.index("@")))


def can_move(frm, move):
    thing = space[frm]
    if thing == ".":
        return True
    if thing == "#":
        return False
    dest = frm + move
    if thing == "@":
        return can_move(dest, move)
    if thing == "[":
        return can_move(dest, move) and (
            move in (Dir4.E, Dir4.W) or can_move(dest + Dir4.E, move)
        )
    if thing == "]":
        return can_move(dest, move) and (
            move in (Dir4.E, Dir4.W) or can_move(dest + Dir4.W, move)
        )


def push(frm, move, sticky=False):  # sticky to break the left-right infinit loop
    thing = space[frm]
    if thing not in ("[", "]", "@"):
        return
    dest = frm + move
    push(dest, move)
    if thing == "[" and move in (Dir4.N, Dir4.S) and not sticky:
        push(frm + Dir4.E, move, sticky=True)
    if thing == "]" and move in (Dir4.N, Dir4.S) and not sticky:
        push(frm + Dir4.W, move, sticky=True)

    del space[frm]
    space[dest] = thing
    return dest


def score(space):
    total = 0
    for bx, by in space.index("["):
        total += bx + by * 100
    return total


for move in moves:
    print(move)
    if can_move(robot, move):
        robot = push(robot, move)

    # print(space)
    pass


print(score(space))
