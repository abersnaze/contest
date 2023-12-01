#!python3

import fileinput


def parse_line(line):
    return list(line.strip())


content = list(map(parse_line, fileinput.input()))


def get(x, y):
    if x < 0 or y < 0:
        return " "
    global content
    try:
        return content[y][x]
    except IndexError:
        return " "


def occupied(x, y):
    return 1 if get(x, y) == "#" else 0


def available(x, y):
    return get(x, y) == "L"


def gaze(x0, dx, y0, dy):
    x1 = x0 + dx
    y1 = y0 + dy

    loc = get(x1, y1)
    if loc == ".":
        return gaze(x1, dx, y1, dy)
    if loc == "#":
        return 1
    if loc == "L":
        return 0
    return 0


def crowd(x, y):
    a = gaze(x, +1, y, +1)
    b = gaze(x, -0, y, +1)
    c = gaze(x, -1, y, +1)
    d = gaze(x, -1, y, -0)
    e = gaze(x, -1, y, -1)
    f = gaze(x, +0, y, -1)
    g = gaze(x, +1, y, -1)
    h = gaze(x, +1, y, +0)
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
                    if crowd(x, y) > 4:
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
