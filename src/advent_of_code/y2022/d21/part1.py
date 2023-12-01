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


def do(var, exp):
    global vals, exps
    suba, op, subb = exp
    if suba in vals and subb in vals:
        del exps[var]
        val = eval(" ".join(exp), vals)
        print("\tsovling", var, "=", exp, "=", val)
        vals[var] = val
        return val
    return None


while len(exps) > 0:
    for var, exp in list(exps.items()):
        do(var, exp)
