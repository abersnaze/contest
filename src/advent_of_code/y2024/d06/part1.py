from common.input import input
from common.space import Dir4, Space

space = Space()
guard = None
for y, line in enumerate(input()):
    for x, char in enumerate(line):
        if char == "#":
            space[(x, y)] = char
        if char == "^":
            guard = ((x, y), Dir4.N)

visited = set()

while space.inside(guard[0]):
    visited.add(guard[0])
    space[guard[0]] = "@"
    # print(space)
    space[guard[0]] = "x"
    if space[guard[0] + guard[1]] == "#":
        guard = (guard[0], guard[1].turn("R"))
    else:
        guard = (guard[0] + guard[1], guard[1])

print(len(visited))
