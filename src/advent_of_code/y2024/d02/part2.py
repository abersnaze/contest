from common.input import input

reports = []

for line in input():
    reports.append(list(map(int, line.split())))


def is_safe(report):
    is_increasing = report[0] < report[1]
    for i in range(1, len(report)):
        if is_increasing:
            if report[i - 1] > report[i]:
                return False
        else:
            if report[i - 1] < report[i]:
                return False
        diff = abs(report[i] - report[i - 1])
        if diff not in (1, 2, 3):
            return False
    return True


sum = 0
for report in reports:
    if is_safe(report):
        sum += 1
    else:
        for i in range(len(report)):
            if is_safe(report[:i] + report[i + 1 :]):
                sum += 1
                break

print("sum", sum)
# assert sum == 366
