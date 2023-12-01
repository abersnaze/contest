#!python3

import fileinput
import re
from collections import defaultdict, Counter
import sys


class Tile:
    def __init__(
        self,
        id,
        edge_n,
    ):
        self.edgesN = edges

    def rotate(self):
        return Tile(
            [
                self.edges[1][::-1],
                self.edges[2],
                self.edges[3][::-1],
                self.edges[0],
            ]
        )

    def flip_v(self):
        return Tile(
            [
                self.edges[2],
                self.edges[1][::-1],
                self.edges[0],
                self.edges[3][::-1],
            ]
        )

    def flip_h(self):
        return Tile(
            [
                self.edges[0][::-1],
                self.edges[3],
                self.edges[2][::-1],
                self.edges[1],
            ]
        )

    def __repr__(self):
        l = len(self.edges[0])
        lines = ["".join(self.edges[0])]
        for i in range(1, l - 1):
            lines.append(self.edges[1][i] + (" " * (l - 2)) + self.edges[3][i])
        lines.append("".join(self.edges[2]))
        return f"Tile {str(self.id)}\n" + "\n".join(lines)


header = re.compile("Tile (\d+):")
id = None
pixels = []
tiles = []
foo = defaultdict(list)
for line in map(lambda x: x.strip(), fileinput.input()):
    if not line:
        edges = ["", "", "", ""]
        l = len(pixels)
        for i in range(l):
            edges[0] += pixels[0][i]
            edges[1] += pixels[i][0]
            edges[2] += pixels[l - 1][i]
            edges[3] += pixels[i][l - 1]
        # tile = Tile(id, edges)
        foo[edges[0]].append(id)
        foo[edges[1]].append(id)
        foo[edges[2]].append(id)
        foo[edges[3]].append(id)
        foo[edges[0][::-1]].append(id)
        foo[edges[1][::-1]].append(id)
        foo[edges[2][::-1]].append(id)
        foo[edges[3][::-1]].append(id)

        # print(tile.flip_v(), "\n")
        # print("\n".join(pixels), "\n")
        # tiles.append(tile)
        pixels = []
        continue
    h = header.match(line)
    if h:
        id = h.group(1)
    else:
        pixels.append(line)

edge_tiles = Counter(
    list(map(lambda ids: ids[0], filter(lambda ids: len(ids) == 1, foo.values())))
)
print(edge_tiles)

total = 1
for key, value in edge_tiles.items():
    print(key, value)
    if value == 4:
        total *= int(key)
print(total)
