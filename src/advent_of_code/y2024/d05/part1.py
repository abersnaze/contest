from common.input import input

rules = []
updates = []
section = 0
for line in input():
    if section == 0:
        if line == "":
            section += 1
        else:
            rules.append(tuple(map(int, line.split("|"))))
    else:
        updates.append(list(map(int, line.split(","))))

print(rules)
print(updates)


def passes_rules(update):
    for a, b in rules:
        try:
            idx_a = update.index(a)
            idx_b = update.index(b)
        except ValueError:
            continue
        if idx_a > idx_b:
            return False
    return True


sum = 0
for update in updates:
    if passes_rules(update):
        sum += update[len(update) // 2]

print(sum)
