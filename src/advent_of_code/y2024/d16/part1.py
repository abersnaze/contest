from collections import defaultdict
import math
from common.input import input
from common.space import Dir4, Point, Space


def to_str(value):
    min_score = math.inf
    min_dir = None
    for dir, score in value.items():
        if type(score) == str:
            return score
        if score < min_score:
            min_score = score
            min_dir = dir
    if min_score == math.inf:
        return "."
    return str(min_dir)


start = None
ends = None
maze = Space(default=math.inf)
for y, line in enumerate(input()):
    if line == "":
        break
    for x, char in enumerate(line):
        if char == "#":
            for dir in Dir4:
                maze[(x, y, dir)] = "#"
        if char == "S":
            start = (x, y, Dir4.E)
        if char == "E":
            ends = {(x, y, dir) for dir in Dir4}
maze_projection = maze.project(2, to_str=to_str)
print(maze_projection)

queue = [start]
maze[start] = 0

count = 0
while queue:
    pos = queue.pop(0)
    score = maze[pos]
    px, py, dir = pos
    for move in Dir4:
        if move == -dir:
            continue
        if move == dir:
            cost = 1
            new_pos = (*((px, py) + move), move)
        else:
            cost = 1000
            new_pos = (px, py, move)
        if maze[new_pos] == "#":
            continue
        new_score = score + cost
        if maze[new_pos] <= new_score:
            continue
        maze[new_pos] = new_score
        queue.append(new_pos)

    count += 1
    if count % 1000 == 0:
        print(maze.project(2, to_str=to_str))
        print(count)
        pass

for end in ends:
    print(end, maze[end])
