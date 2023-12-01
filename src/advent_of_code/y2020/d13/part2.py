#!python3

import fileinput
import sys
from functools import reduce


time, buses = map(lambda x: x.strip(), fileinput.input())

buses = list(
    map(
        lambda x: (x[0], int(x[1])),
        filter(lambda x: x[1] != "x", enumerate(buses.split(","))),
    )
)

buses.sort(key=lambda x: -x[1])

print(buses)


def foo(t, step, bs):
    if len(bs) == 0:
        return t
    while True:
        if (t + bs[0][0]) % bs[0][1] == 0:
            return foo(t, step * bs[0][1], bs[1:])
        t += step


print(foo(0, 1, buses))
