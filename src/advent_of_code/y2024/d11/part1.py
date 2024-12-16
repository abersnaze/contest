import math
from common.input import input

lines = input()
stones = list(map(int, next(lines).split(" ")))
times = int(next(lines))


def stone_rule(s):
    if s == 0:
        yield 1
        return
    digits = str(s)
    num_digits = len(digits)
    if num_digits % 2 == 0:
        yield int(digits[: num_digits // 2])
        yield int(digits[num_digits // 2 :])
        return
    yield s * 2024


def blink(stones):
    new_stones = []
    for stone in stones:
        new_stones.extend(stone_rule(stone))
    return new_stones


for i in range(times):
    print(i, len(stones))
    stones = blink(stones)

# print(" ".join(map(str, stones)))

print(len(stones))
