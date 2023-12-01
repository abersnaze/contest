#!python3

import fileinput
import re

insts = list(fileinput.input())

opcode = {
    "acc": lambda acc, inst_ptr, value: (acc + value, inst_ptr + 1),
    "jmp": lambda acc, inst_ptr, value: (acc, inst_ptr + value),
    "nop": lambda acc, inst_ptr, value: (acc, inst_ptr + 1),
}

p = re.compile("(\w\w\w) ([+-]\d+)\n")


def run(swap):
    insts_copy = list(insts)
    swap_inst = insts_copy[swap]
    if swap_inst.startswith("acc"):
        print("skip")
        return None
    else:
        if swap_inst.startswith("jmp"):
            insts_copy[swap] = swap_inst.replace("jmp", "nop")
        if swap_inst.startswith("nop"):
            insts_copy[swap] = swap_inst.replace("nop", "jmp")

    prev_inst_ptr = set()
    acc = 0
    inst_ptr = 0

    while inst_ptr not in prev_inst_ptr:
        prev_inst_ptr.add(inst_ptr)
        if inst_ptr >= len(insts_copy):
            print("terminate", acc)
            return acc
        inst = insts_copy[inst_ptr]
        op, value_str = p.match(inst).groups()
        code = opcode[op]
        acc, inst_ptr = code(acc, inst_ptr, int(value_str))
    print("swap", swap, "infinite loop at", inst_ptr, acc)

    return None


for i in range(len(insts)):
    print(i)
    out = run(i)
    if out is not None:
        print("swapped instruction", i, "resulted in", out)
        print(out)
        break
