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


def would_loop(alt_guard):
    obstacle = alt_guard[0] + alt_guard[1]
    alt_space = space.copy()
    if not alt_space.inside(obstacle):
        return False
    alt_space[obstacle] = "0"
    alt_visited = set(visited)
    while alt_space.inside(alt_guard[0]):
        alt_space[alt_guard[0]] = "@"
        print(alt_space)
        alt_space[alt_guard[0]] = "+"
        if alt_guard in alt_visited:
            del alt_space[obstacle]
            return True
        alt_visited.add(alt_guard)
        if alt_space[alt_guard[0] + alt_guard[1]] in ("#", "0"):
            alt_guard = (alt_guard[0], alt_guard[1].turn("R"))
        else:
            alt_guard = (alt_guard[0] + alt_guard[1], alt_guard[1])
    del alt_space[obstacle]
    return False


loopers = set()

while space.inside(guard[0]):
    space[guard[0]] = "@"
    # print(space)
    space[guard[0]] = "x"
    if space[guard[0] + guard[1]] == "#":
        guard = (guard[0], guard[1].turn("R"))
        visited.add(guard)
    else:
        if would_loop(guard):
            loopers.add(guard[0] + guard[1])
        visited.add(guard)
        guard = (guard[0] + guard[1], guard[1])

for looper in loopers:
    space[looper] = "0"
print(space)
print(len(loopers))
