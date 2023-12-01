#!python3

import fileinput
import re
from collections import defaultdict
import sys


class Rule:
    pass


class Terminal(Rule):
    def __init__(self, chr):
        self.chr = chr

    def __repr__(self):
        return self.chr

    def resolve(self, rules):
        return True


class Or(Rule):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __repr__(self):
        return "(" + str(self.a) + "|" + str(self.b) + ")"

    def resolve(self, rules):
        if type(self.a) == str:
            self.a = rules[self.a]
        self.a.resolve(rules)
        if type(self.b) == str:
            self.b = rules[self.b]
        self.b.resolve(rules)


class And(Rule):
    def __init__(self, a, b):
        self.a = a
        self.b = b

    def __repr__(self):
        return str(self.a) + str(self.b)

    def resolve(self, rules):
        if type(self.a) == str:
            self.a = rules[self.a]
        self.a.resolve(rules)
        if type(self.b) == str:
            self.b = rules[self.b]
        self.b.resolve(rules)


class Ref(Rule):
    def __init__(self, a):
        self.a = a

    def __repr__(self):
        return str(self.a)

    def resolve(self, rules):
        if type(self.a) == str:
            self.a = rules[self.a]
        self.a.resolve(rules)


def link(parts):
    if len(parts) == 1:
        return Ref(parts[0])
    rule = And(parts.pop(-2), parts.pop())
    while parts:
        rule = And(parts.pop(), rule)
    return rule


rule_mode = True
rules = {}
inputs = []
for line in map(lambda x: x.strip(), fileinput.input()):
    if rule_mode:
        if not line:
            rule_mode = False
            continue
        id, stuff = line.split(":")
        parts = stuff.split()
        if len(parts) == 1 and parts[0].startswith('"'):
            rule = Terminal(parts[0][1])
        elif "|" in parts:
            idx = parts.index("|")
            rule = Or(link(parts[:idx]), link(parts[idx + 1 :]))
        else:
            rule = link(parts)
        rules[id] = rule
        print("rule", id, ":", rule)
    else:
        inputs.append(line)
        print("foo", line)

for rule in rules.values():
    rule.resolve(rules)

pattern = "^" + str(rules["0"]) + "$"
print(pattern)
f = re.compile(pattern)

total = 0
for input in inputs:
    if f.match(input):
        print("\t", input)
        total += 1
    else:
        print(input)

print(total)
