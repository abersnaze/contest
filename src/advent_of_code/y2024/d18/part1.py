from collections import defaultdict
import heapq
from common.input import input, compile
from common.space import Space, adjacent4

pattern = compile("<int>,<int>")


def to_str(value):
    return "#" if value else "."


space = Space()
for i, line in enumerate(input()):
    x, y = pattern(line)
    for z in range(i, 30):
        space[(x, y, z)] = "#"

print(space.project(2, to_str=to_str))

start = (0, 0, 0)
end = (space.minmax(0)[1], space.minmax(1)[1])
print(start, end)


def manhattan(a, b):
    return sum(abs(x - y) for x, y in zip(a, b))


# a*
queue = []
heapq.heappush(queue, (0, 0, start))
visited = set()
while queue:
    x, y, t = heapq.heappop(queue)
    if (x, y) == end:
        print(t)
        break
    visited.add((x, y, t))
    for move in adjacent4((x, y)):
        neighbor = (*move, t + 1)
        if neighbor in visited or not space.inside(neighbor) or neighbor in space:
            continue
        queue.append(neighbor)
