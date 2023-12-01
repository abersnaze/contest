#!python3

import fileinput
import sys


time, buses = map(lambda x: x.strip(), fileinput.input())

time = int(time)
buses = list(map(int, filter(lambda x: x != "x", buses.split(","))))

print(time, buses, max(buses))

for t in range(time, time + max(buses)):
    for b in buses:
        if t % b == 0:
            print("bus", b, "leaving at time", t, "∆t", t - time)
            print(b * (t - time))
            sys.exit(0)
