#!python3

import fileinput
import re
from collections import defaultdict, Counter
from enum import Enum
from itertools import islice, product
import math
from functools import reduce

lines = map(lambda x: x.strip(), fileinput.input())


class Monkey:
    def __init__(self) -> None:
        self.items = []
        self.op = ""
        self.divisor = 0
        self.if_true = 0
        self.if_false = 0
        self.bidnus = 0

    def __str__(self) -> str:
        return f"{self.items} -> {self.op} % {self.divisor} ? {self.if_true} : {self.if_false}"

    def inspect(self):
        self.bidnus += 1
        new = eval(self.op, {}, {"old": self.items.pop(0)}) // 3
        return (self.if_true if new % self.divisor == 0 else self.if_false, new)


monkeys = defaultdict(Monkey)
num = 0
for line in lines:
    if not line:
        continue
    part = line.split(":")
    if part[0].startswith("Monkey"):
        _, num = part[0].split(" ")
    elif part[0].startswith("Starting items"):
        monkeys[num].items = list(
            map(int, map(lambda x: x.strip(), part[1].split(",")))
        )
    elif part[0].startswith("Operation"):
        monkeys[num].op = part[1].split("=")[1].strip()
    elif part[0].startswith("Test"):
        monkeys[num].divisor = int(part[1][14:])
    elif part[0].startswith("If true"):
        monkeys[num].if_true = part[1][17:]
    elif part[0].startswith("If false"):
        monkeys[num].if_false = part[1][17:]
    else:
        print(line)
        assert False

print("\n".join(map(lambda m: f"{m.items} - {m.bidnus}", monkeys.values())))

for round in range(20):
    for num, monkey in monkeys.items():
        while monkey.items:
            next_monkey, item = monkey.inspect()
            monkeys[next_monkey].items.append(item)

print("\n".join(map(lambda m: f"{m.items} - {m.bidnus}", monkeys.values())))

monkey_bidnus = sorted(map(lambda m: m.bidnus, monkeys.values()))[-2:]

print(monkey_bidnus[0] * monkey_bidnus[1])
