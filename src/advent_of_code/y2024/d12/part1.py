import math
from common.input import input
from common.space import Space, adjacent4

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
        perimeter = area * 4
        for point in blob:
            perimeter -= len(set(adjacent4(point)) & blob)

        cost = area * perimeter
        print(plant, area, perimeter, cost)
        total += cost

print(total)
