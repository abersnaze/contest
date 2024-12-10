from collections import defaultdict
from common.input import input
from common.space import Space

space = Space.read(input)
print(space)

antinodes = set()
seen_nodes = defaultdict(set)
for p, freq in space.items():
    for q in seen_nodes[freq]:
        print(freq, p, q)
        delta = p - q
        anti = p + delta
        if space.inside(anti):
            antinodes.add(anti)
        anti = q - delta
        if space.inside(anti):
            antinodes.add(anti)
    seen_nodes[freq].add(p)

for anti in antinodes:
    space[anti] = "#"
print(space)

print(len(antinodes))
