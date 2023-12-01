#!python3

import fileinput
import re
from collections import defaultdict


mask_patter = re.compile("mask = ([X01]{36})")
mem_patter = re.compile("mem\[(\d+)\] = (\d+)\n")
mem = defaultdict(lambda: 0)
mask = None
for line in fileinput.input():
    match = mask_patter.match(line)
    if match:
        bits_set = "".join(["1" if x == "1" else "0" for x in match.groups()[0]])
        bits_float = "".join(["1" if x == "X" else "0" for x in match.groups()[0]])
        print("mask", bits_set, bits_float.replace("0", "-"))
        mask = (int(bits_set, 2), int(bits_float, 2))
    else:
        match = mem_patter.match(line)
        if match:
            mask_set, mask_float = mask
            # force the bits that need to be set
            # clear the bits that float
            # to get the smallest address set
            addr = (int(match.groups()[0]) | mask_set) & ~mask_float
            value = int(match.groups()[1])

            addrs = [addr]
            bit = 1
            for i in range(36):
                # if float bit is set
                if bit & mask_float:
                    # set addrs to product of bitwise or of all the
                    # addresses and [float bit 0 & float bit 1]
                    addrs = [b | a for a in addrs for b in [0, bit]]
                bit <<= 1
            for a in addrs:

                mem[a] = value

print(len(mem.values()))
print(sum(mem.values()))
