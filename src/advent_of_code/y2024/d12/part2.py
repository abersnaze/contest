from collections import defaultdict
import math
from common.input import input
from common.space import Dir4, Space, adjacent4

garden = Space.read(input)
print(garden)

total = 0
for plant in garden.values():
    points = set(garden.index(plant))
    while points:
        start = points.pop()
        # find all the connected points
        blob = {start}
        neighbors = set(adjacent4(start)) & points
        while neighbors:
            point = neighbors.pop()
            blob.add(point)
            points.remove(point)
            neighbors |= set(adjacent4(point)) & points

        # find the area and perimeter of the blob
        area = len(blob)
        fences = defaultdict(list)
        for point in blob:
            for neighbor in adjacent4(point):
                if neighbor not in blob:
                    if neighbor[0] == point[0]:
                        fences[
                            (
                                Dir4.N if neighbor[1] < point[1] else Dir4.S,
                                (neighbor[1] + point[1]) / 2,
                            )
                        ].append(point[0])
                    elif neighbor[1] == point[1]:
                        fences[
                            (
                                Dir4.E if neighbor[0] > point[0] else Dir4.W,
                                (neighbor[0] + point[0]) / 2,
                            )
                        ].append(point[1])

        # find contiguous fence segments
        sides = 0
        for dir, segments in fences.items():
            sides += 1
            segments.sort()
            start = segments[0]
            for segment in segments[1:]:
                if segment != start + 1:
                    sides += 1
                start = segment
            pass

        cost = area * sides
        print(plant, area, sides, cost)
        total += cost

print(total)
