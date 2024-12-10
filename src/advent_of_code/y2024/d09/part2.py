from common.input import input

disk_map = list(
    map(
        lambda x: (str(x[0] // 2) if x[0] % 2 == 0 else ".", x[1]),
        enumerate(map(int, next(input()))),
    )
)

for file_idx in range(len(disk_map) - 1, 0, -1):
    file_id, file_size = disk_map[file_idx]
    if file_id == ".":
        continue

    for free_idx in range(0, len(disk_map)):
        if disk_map[free_idx][0] != "." or file_idx < free_idx:
            continue
        free_space = disk_map[free_idx][1]
        if disk_map[free_idx][0] == "." and free_space >= file_size:
            disk_map[file_idx] = (".", file_size)
            disk_map[free_idx] = (file_id, file_size)
            if free_space > file_size:
                disk_map.insert(free_idx + 1, (".", free_space - file_size))
            break

disk_layout = []
for id, blocks in disk_map:
    for _ in range(blocks):
        disk_layout.append(id)

print("".join(map(str, disk_layout)))

checksum = sum(
    map(lambda p: p[0] * int(p[1]) if p[1] != "." else 0, enumerate(disk_layout))
)

print(checksum)
