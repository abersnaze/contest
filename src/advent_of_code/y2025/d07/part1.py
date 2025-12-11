from collections import defaultdict
from common.space import Space
from common.input import input

lines = list(input())

start = lines[0].index('S')
front = defaultdict(lambda: 0)
front[start] = 1

def dump():
    for x in range(min(*front.keys(), 0), max(*front.keys(), start) + 1):
        ltr = '|' if x in front else '.'
        print(ltr, end="")
    print()

times = 0
for y, line in enumerate(lines[1:]):
    dump()
    if '^' in line:
        propagate = defaultdict(lambda: 0)
        for x, ltr in enumerate(line):
            if ltr == '^':
                if x in front:
                    times += 1
                propagate[x-1] += front[x]
                propagate[x+1] += front[x]
            if ltr == '.' and x in front:
                propagate[x] += front[x]
        
        front = propagate

print(times)
