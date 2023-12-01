#!python3

import fileinput
import math
import re
import sys
from collections import Counter, defaultdict


class Tile:
    def __init__(self, pixels, edge_n, edge_w, edge_s, edge_e, dx, dy, swap):
        self.pixels = pixels
        self.edge_n = edge_n
        self.edge_w = edge_w
        self.edge_s = edge_s
        self.edge_e = edge_e
        self.dx = dx
        self.dy = dy
        self.swap = swap

    def rotate(self):
        return Tile(
            self.pixels,
            self.edge_w[::-1],
            self.edge_s,
            self.edge_e[::-1],
            self.edge_n,
            self.dy,
            -self.dx,
            not self.swap,
        )

    def flip_v(self):
        return Tile(
            self.pixels,
            self.edge_s,
            self.edge_w[::-1],
            self.edge_n,
            self.edge_e[::-1],
            self.dx,
            -self.dy,
            self.swap,
        )

    def flip_h(self):
        return Tile(
            self.pixels,
            self.edge_n[::-1],
            self.edge_e,
            self.edge_s[::-1],
            self.edge_w,
            -self.dx,
            self.dy,
            self.swap,
        )

    def get(self, x, y):
        m = x * self.dx if not self.swap else y * self.dy
        n = y * self.dy if not self.swap else x * self.dx
        return self.pixels[n][m]

    def __repr__(self):
        l = len(self.pixels)
        out = ""
        out += "\n\t" + self.edge_n + "-n"
        ys = list(range(0, l)) if self.dy > 0 else list(reversed(range(0, l)))
        xs = list(range(0, l)) if self.dx > 0 else list(reversed(range(0, l)))
        if not self.swap:
            for y in ys:
                out += "\n\t"
                for x in xs:
                    out += self.pixels[y][x]
        else:
            for x in xs:
                out += "\n\t"
                for y in ys:
                    out += self.pixels[y][x]
        out += "\n\t" + self.edge_s + "-s"
        out += "\n\t" + self.edge_e + "-e"
        out += "\n\t" + self.edge_w + "-w"
        return out


header = re.compile("Tile (\d+):")
id = None
pixels = []
tiles_by_id = {}
id_by_edge = defaultdict(list)
for line in map(lambda x: x.strip(), fileinput.input()):
    if not line:
        edge_n = ""
        edge_w = ""
        edge_s = ""
        edge_e = ""
        l = len(pixels)
        for i in range(l):
            edge_n += pixels[0][i]
            edge_w += pixels[i][0]
            edge_s += pixels[-1][i]
            edge_e += pixels[i][-1]
        tile = Tile(pixels, edge_n, edge_w, edge_s, edge_e, 1, 1, False)

        edge_rn = edge_n[::-1]
        edge_rw = edge_w[::-1]
        edge_rs = edge_s[::-1]
        edge_re = edge_e[::-1]

        id_by_edge[edge_n].append(id)
        id_by_edge[edge_rn].append(id)
        id_by_edge[edge_w].append(id)
        id_by_edge[edge_rw].append(id)
        id_by_edge[edge_s].append(id)
        id_by_edge[edge_rs].append(id)
        id_by_edge[edge_e].append(id)
        id_by_edge[edge_re].append(id)

        # print("title:", id)
        # print(tile)
        tiles_by_id[id] = tile
        pixels = []
        continue
    h = header.match(line)
    if h:
        id = h.group(1)
    else:
        pixels.append(line)
# print("id_by_edge", id_by_edge)

# find edge or rev(edge) that don't have a match (aka image edges)
print("######################################")
edge_tiles = Counter(
    list(
        map(
            lambda ids: ids[0],
            list(filter(lambda ids: len(ids) == 1, id_by_edge.values())),
        )
    )
)
edge_tiles = sorted(edge_tiles, key=edge_tiles.__getitem__, reverse=True)
print("edge_tiles", edge_tiles)


class Mosaic:
    def __init__(self, size):
        self.tiles = []
        self.size = size
        for i in range(0, L):
            self.tiles.append([None] * L)

    def __repr__(self):
        l = 10
        L = self.size * l
        out = "\n\t"
        for y in range(L):
            i = y
            ty = int(i / l)
            py = i % l
            tout = ""
            for x in range(L):
                j = x
                tx = int(j / l)
                px = j % l
                t = self.tiles[ty][tx]
                out += t.get(px, py) if t else "_"
            out += "\n\t"
        else:
            out += "\n"
        return out

    def __getitem__(self, i):
        return self.tiles[i]


L = int(math.sqrt(len(tiles_by_id)))
print("size:", L)

mosaic = Mosaic(L)
unused = [edge_tiles[0]] + edge_tiles[4:] + edge_tiles[1:4]
unused = unused + list(set(tiles_by_id.keys()).difference(unused))

# print(mosaic)


def slices(xs):
    for i in range(len(xs)):
        yield xs[i], xs[:i] + xs[i + 1 :]


def permut_tile(tile: Tile):
    yield tile
    yield tile.flip_h()
    yield tile.flip_v()
    x = tile.rotate()
    yield x
    x = x.rotate()
    yield x
    x = x.rotate()
    yield x


match_id = 0


def match(tile, x, y):
    global mosaic, L, match_id
    match_id += 1
    if 0 < x and mosaic[y][x - 1]:
        print(mosaic[y][x - 1])
        print("\t<", tile.edge_w, "==", mosaic[y][x - 1].edge_e)
        if tile.edge_w != mosaic[y][x - 1].edge_e:
            return False
    if x < L - 1 and mosaic[y][x + 1]:
        print("\t>", tile.edge_e, "==", mosaic[y][x + 1].edge_w)
        if tile.edge_e == mosaic[y][x + 1].edge_w:
            return False
    if 0 < y and mosaic[y - 1][x]:
        print("\t^", tile.edge_n, "==", mosaic[y - 1][x].edge_s)
        if tile.edge_n == mosaic[y - 1][x].edge_s:
            return False
    if y < L - 1 and mosaic[y + 1][x]:
        print("\tv", tile.edge_s, "==", mosaic[y + 1][x].edge_n)
        if tile.edge_s == mosaic[y + 1][x].edge_n:
            return False
    print(match_id, "does", tile, "fit at", (x, y), "in", mosaic)
    return True


def fill_mosaic(x, y, unused):
    global tiles_by_id, id_by_edge, L
    if len(unused) == 0:
        return True
    print(x, y, unused)
    next_x = x + 1
    next_y = y
    if next_x >= L:
        next_x = 0
        next_y += 1

    id = unused.pop()
    next_unused = unused
    # for id, next_unused in slices(unused):
    for permut in permut_tile(tiles_by_id[id]):
        print("testing", id, "at", (x, y), permut.dx, permut.dy, permut.swap)
        print(permut)
        if match(permut, x, y):
            mosaic[y][x] = tile
            if fill_mosaic(next_x, next_y, next_unused):
                return True
            mosaic[y][x] = None
        print("next permut of", id)
    unused.append(id)
    return False


unused = reversed(
    ["1951", "2311", "3079", "2729", "1427", "2473", "2971", "1489", "1171"]
)
fill_mosaic(0, 0, list(unused))
