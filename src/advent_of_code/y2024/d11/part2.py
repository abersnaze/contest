import functools
import math
from common.input import input

lines = input()
stones = list(map(int, next(lines).split(" ")))
times = int(next(lines))


@functools.cache
def stone_rule(stone, blink):
    if blink == 0:
        return 1
    if stone == 0:
        return stone_rule(1, blink - 1)
    digits = str(stone)
    num_digits = len(digits)
    if num_digits % 2 == 0:
        first = int(digits[: num_digits // 2])
        second = int(digits[num_digits // 2 :])
        return stone_rule(first, blink - 1) + stone_rule(second, blink - 1)
    return stone_rule(stone * 2024, blink - 1)


sum = 0
for stone in stones:
    out = stone_rule(stone, times)
    print("\t", stone, out)
    sum += out

print(sum)
