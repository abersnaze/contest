#!python3

import fileinput
import re
from collections import defaultdict, Counter
from itertools import islice, product, repeat
from functools import reduce

nums = list(map(lambda x: int(x.strip()) * 811589153, fileinput.input()))
idxs = list(range(len(nums)))


def slide(frm, amount, size=len(nums)):
    to = frm + amount
    wraps = to // size
    while wraps != 0:
        to = (to % size) + wraps
        wraps = to // size
    return to


def dump(header, xs):
    off = xs.index(0)
    print(header, end="\t")
    for i in range(len(xs)):
        print(xs[(i + off) % len(xs)], end=", ")
    print()


# rounds = [
# [2, 1, -3, 3, -2, 0, 4],
# [1, -3, 2, 3, -2, 0, 4],
# [1, 2, 3, -2, -3, 0, 4],
# [1, 2, -2, -3, 0, 3, 4],
# [1, 2, -3, 0, 3, 4, -2],
# [1, 2, -3, 0, 3, 4, -2],
# [1, 2, -3, 4, 0, 3, -2],
# ]
# dump("a", nums)
# dump("e", nums)
for i in range(len(nums)):
    if i == 2:
        print("i", i)
    frm = idxs.index(i)
    to = slide(frm, nums[frm])
    nums.insert(to, nums.pop(frm))
    idxs.insert(to, idxs.pop(frm))
    # dump("a", nums)
    # dump("e", rounds[i])


def xlate(frm):
    return frm % len(nums)


offset = nums.index(0)
x = nums[xlate(1000 + offset)]
# assert x == 4
y = nums[xlate(2000 + offset)]
# assert y == -3
z = nums[xlate(3000 + offset)]
# assert z == 2

print(x, y, z)
print(x + y + z)
