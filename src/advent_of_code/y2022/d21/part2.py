#!python3

import fileinput
import re
from collections import defaultdict, Counter
from itertools import islice, product, repeat
from functools import reduce

exps = {}
vals = {}
lines = list(map(lambda x: x.strip(), fileinput.input()))
for line in lines:
    var, exp = line.split(": ")
    if re.match("[0-9]", exp):
        vals[var] = int(exp)
    else:
        exps[var] = tuple(exp.split(" "))

del vals["humn"]
expa, _, expb = exps.pop("root")


def resolve(a, op, b):
    if type(a) == str:
        a = vals[a] if a in vals else resolve(*exps[a]) if a in exps else a
    if type(b) == str:
        b = vals[b] if b in vals else resolve(*exps[b]) if b in exps else b
    return (a, op, b)


def simplify(a, op, b, humn=None):
    if type(a) == tuple:
        a = simplify(*a, humn)
    if type(b) == tuple:
        b = simplify(*b, humn)
    if a == "humn" and humn is not None:
        a = humn
    if b == "humn" and humn is not None:
        b = humn
    if type(a) == int and type(b) == int:
        return int(eval(f"{a} {op} {b}"))
    if humn is not None:
        raise ValueError()
    return (a, op, b)


expa = resolve(*exps[expa])
expb = resolve(*exps[expb])


def dump(r):
    if type(r) == tuple:
        return f"({dump(r[0])} {r[1]} {dump(r[2])})"
    return str(r)


print(dump(expa))
print(simplify(*expb))


def undo(a, op, b, eq):
    if type(a) == tuple:
        a = simplify(*a)
        if type(b) == tuple:
            b = simplify(*b)
        if op == "+":
            # ()+b = eq -> eq-b
            return undo(*a, eq - b)
        elif op == "-":
            # ()-b = eq -> () = eq+b
            return undo(*a, eq + b)
        elif op == "*":
            # ()*b = eq -> () = eq/b
            return undo(*a, eq / b)
        else:
            # ()/b = eq -> () = eq*b
            return undo(*a, eq * b)
    if type(b) == tuple:
        if type(a) == tuple:
            a = simplify(*a)
        if op == "+":
            # b+() = eq -> eq-b
            return undo(*b, eq - a)
        elif op == "-":
            # b-() = eq -> () = -eq+b
            return undo(*b, -eq + a)
        elif op == "*":
            # b*() = eq -> () = eq/b
            return undo(*b, eq / a)
        else:
            # b/() = eq -> () = b*eq
            return undo(*b, eq * a)
    return (a, op, b, "=", eq)


print(undo(*expa, simplify(*expb)))
