#!python3

import fileinput
import re
from collections import defaultdict


def parse_line(line):
    return int(line)


content = list(map(parse_line, fileinput.input()))

SIZE = content.pop(0)
pre_list = content[:SIZE]
pre_ocr = defaultdict(lambda: 0)
for p in pre_list:
    pre_ocr[p] += 1
post_list = content[SIZE:]


def state():
    # print(list(map(lambda p: p[0], filter(lambda p: p[1]>0, pre_ocr.items()))))
    print(pre_list, post_list)
    pass


state()
idx = SIZE
while post_list:
    nxt = post_list.pop(0)

    valid = False
    for a in pre_list:
        b = nxt - a
        if pre_ocr[b] > 0 and a != b or pre_ocr[b] > 1:
            print(f"{nxt} = {a} + {b}")
            valid = True
            break

    if not valid:
        print(f"[{idx}] = {nxt} is invalid")
        break

    state()
    idx += 1
    lst = pre_list.pop(0)
    pre_ocr[lst] -= 1
    pre_ocr[nxt] += 1
    pre_list.append(nxt)
