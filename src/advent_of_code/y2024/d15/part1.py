from common.input import input
from common.space import Dir4, Space

lines = input()
space = Space.read(lines)

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


def step(frm, move):
    thing = space[frm]
    if thing == "#":
        return None
    dest = frm + move
    if dest in space:
        if step(dest, move) is None:
            return None
    del space[frm]
    space[dest] = thing
    return dest


def score(space):
    total = 0
    for bx, by in space.index("O"):
        total += bx + by * 100
    return total


for move in moves:
    r = step(robot, move)
    if r is not None:
        robot = r

    # print(move)
    # print(space)
    pass


print(score(space))
