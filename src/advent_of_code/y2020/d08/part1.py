#!python3

import fileinput
import re

insts = list(fileinput.input())

opcode = {
    "acc": lambda acc, inst_ptr, value: (acc + value, inst_ptr + 1),
    "jmp": lambda acc, inst_ptr, value: (acc, inst_ptr + value),
    "nop": lambda acc, inst_ptr, value: (acc, inst_ptr + 1),
}

prev_inst_ptr = set()
p = re.compile("(\w\w\w) ([+-]\d+)\n")

acc = 0
inst_ptr = 0

while inst_ptr not in prev_inst_ptr:
    prev_inst_ptr.add(inst_ptr)
    inst = insts[inst_ptr]
    op, value_str = p.match(inst).groups()
    code = opcode[op]
    acc, inst_ptr = code(acc, inst_ptr, int(value_str))

print()
print(acc)
