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
print(maze.project(2, to_str=to_str))
seats = maze.copy()

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

print(maze.project(2, to_str=to_str))
end = min(ends, key=lambda end: maze[end])
end_score = maze[end]
print(end, end_score)

seats[end] = "O"
all_points = {end[0:2]}
pathes = [(end, end_score)]
count = 0
while pathes:
    pos, score = pathes.pop(0)
    pass
    px, py, dir = pos
    for move in Dir4:
        if move == -dir:
            continue
        if move == dir:
            cost = 1
            prev_pos = (*((px, py) - move), dir)
        else:
            cost = 1000
            prev_pos = (px, py, move)
        prev_score = score - cost
        if prev_score == "#" or prev_score != maze[prev_pos]:
            continue
        pathes.append((prev_pos, prev_score))
        seats[prev_pos] = "O"
        all_points.add(prev_pos[0:2])
    count += 1
    if count % 10 == 0:
        print(seats.project(2, to_str=to_str))
print(seats.project(2, to_str=to_str))

print(len(all_points))
