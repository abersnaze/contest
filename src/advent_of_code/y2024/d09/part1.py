from common.input import input

disk_map = list(enumerate(map(int, next(input()))))


def chunks(disk_map):
    for idx2, blocks in disk_map:
        id = "." if idx2 % 2 != 0 else idx2 // 2
        for _ in range(blocks):
            yield id


disk_layout = list(chunks(disk_map))

compacted = []
while len(disk_layout) > 0:
    block = disk_layout.pop(0)
    if block == ".":
        fill = disk_layout.pop()
        while fill == "." and len(disk_layout) > 0:
            fill = disk_layout.pop()
        if fill == ".":
            break
        compacted.append(fill)
    else:
        compacted.append(block)

print("".join(map(str, compacted)))

checksum = sum(map(lambda p: p[0] * int(p[1]), enumerate(compacted)))

print(checksum)
