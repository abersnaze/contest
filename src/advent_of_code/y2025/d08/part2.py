import math
from common.input import input

boxes = []
for line in input():
    if line.startswith("n="):
        cloest = int(line[2:])
    elif line.startswith("c="):
        largest = int(line[2:])
    else:
        boxes.append(tuple(map(int, line.split(","))))

dists = {}
for idx_a, a in enumerate(boxes):
    for b in boxes[idx_a + 1 :]:
        if a == b:
            continue
        dist = math.dist(a, b)
        dists[(a, b)] = dist

sorted_dists = sorted(dists.items(), key=lambda p: p[1])


class Circuit:
    def __init__(self, a):
        self.seed = a
        self.boxes = {a}
        self.connections = dict()

    def add(self, a, b, dist):
        if a in self.boxes and b in self.boxes:
            return
        self.boxes.add(a)
        self.boxes.add(b)
        self.connections[(a, b)] = dist

    def join(self, other: "Circuit", a, b, dist):
        self.add(a, b, dist)
        self.boxes |= other.boxes
        self.connections |= other.connections

    def __repr__(self):
        return "~".join(map(str, self.boxes))


circuits = {box: Circuit(box) for box in boxes}

for (a, b), dist in sorted_dists:
    ca = circuits[a]
    cb = circuits[b]
    if ca == cb:
        continue
    ca.join(cb, a, b, dist)
    for sib_b in cb.boxes:
        circuits[sib_b] = ca
    if len(set(map(lambda c: c.seed, circuits.values()))) == 1:
        break

print(a, b)
print(a[0], "*", b[0], "=", a[0] * b[0])
