from typing import Set, Tuple
from common.input import input
from common.space import Space, adjacent4

space = Space.read(input, int)
tails = dict()

print(space)


def score(head, value) -> Set[Tuple]:
    if head in tails:
        return tails[head]
    if value == 9:
        tails[head] = {(head,)}
        return tails[head]

    nxt_value = value + 1
    agg = set()
    for step in adjacent4(head):
        if space[step] == nxt_value:
            for distinct in score(step, nxt_value):
                agg.add((head,) + distinct)

    if head not in tails:
        tails[head] = set()
    tails[head].update(agg)
    return agg


sum = 0
for head in space.index(0):
    ts = score(head, 0)
    print(head, len(ts))
    sum += len(ts)

print(sum)
