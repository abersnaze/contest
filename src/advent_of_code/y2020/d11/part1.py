#!python3

import fileinput


def parse_line(line):
    return list(line.strip())


content = list(map(parse_line, fileinput.input()))


def occupied(x, y):
    global content
    if x < 0 or y < 0:
        return 0
    try:
        return 1 if content[y][x] == "#" else 0
    except IndexError:
        return 0


def available(x, y):
    global content
    return content[y][x] == "L"


def crowd(x, y):
    a = occupied(x + 1, y + 1)
    b = occupied(x - 0, y + 1)
    c = occupied(x - 1, y + 1)
    d = occupied(x - 1, y - 0)
    e = occupied(x - 1, y - 1)
    f = occupied(x + 0, y - 1)
    g = occupied(x + 1, y - 1)
    h = occupied(x + 1, y + 0)
    return a + b + c + d + e + f + g + h


step = 0
total = 0


def write():
    global content
    # global total
    # global step
    # print("step", step, "total", total)
    print("\n".join(["".join(row) for row in content]))
    print("---------------------")


changes = 1
while changes > 0:
    write()
    step += 1
    changes = 0
    nxt_content = []
    for y in range(len(content)):
        nxt_row = []
        for x in range(len(content[y])):
            if available(x, y):
                if crowd(x, y) == 0:
                    changes += 1
                    total += 1
                    nxt_row.append("#")
                else:
                    nxt_row.append("L")
            else:
                if occupied(x, y):
                    if crowd(x, y) > 3:
                        changes += 1
                        total -= 1
                        nxt_row.append("L")
                    else:
                        nxt_row.append("#")
                else:
                    nxt_row.append(".")
        nxt_content.append(nxt_row)
    content = nxt_content

write()
print(total)
