# 119/126
# 8:44/25:10
from math import isfinite
from functools import cache
from fileinput import input

lines = input()
data = [
    (l, tuple(int(x) for x in r.split(",")))
    for l, r in [line.split() for line in lines]
]
index = lambda s, c: s.index(c) if c in s else float("inf")


@cache
def count(springs, damaged):
    if len(damaged) == 0:
        return springs.count("#") == 0
    if len(springs) == 0:
        return False
    if isfinite(skip := min(index(springs, "#"), index(springs, "?"))) and skip > 0:
        return count(springs[skip:], damaged)
    valid = (
        len(springs) >= damaged[0]
        and all(c != "." for c in springs[: damaged[0]])
        and (damaged[0] == len(springs) or springs[damaged[0]] in ".?")
    )
    return (count(springs[damaged[0] + 1 :], damaged[1:]) if valid else 0) + (
        count(springs[1:], damaged) if springs[0] == "?" else 0
    )


print("a", sum(count(springs, damaged) for springs, damaged in data))
# print('b', sum(count('?'.join([springs] * 5), damaged * 5) for springs, damaged in data))
