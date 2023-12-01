#!python3

import sys
import re

content = sys.stdin.readlines()

pps = []
pp = []
for line in content:
    if line == "\n":
        pps.append(dict([x.split(":") for x in pp]))
        pp = []
    else:
        pp.extend(line.strip().split(" "))
if len(pp) > 0:
    pps.append(dict([x.split(":") for x in pp]))


def year(min, max):
    return lambda x: len(x) == 4 and int(x) >= min and int(x) <= max


hair_color = re.compile("#[a-f0-9][a-f0-9][a-f0-9][a-f0-9][a-f0-9][a-f0-9]$")

eye_color = set(["amb", "blu", "brn", "gry", "grn", "hzl", "oth"])


def check_height(x):
    if x.endswith("cm"):
        v = int(x[:-2])
        return 150 <= v and v <= 193
    if x.endswith("in"):
        v = int(x[:-2])
        return 59 <= v and v <= 76
    return False


required = set(
    [
        "byr",  # (Birth Year)
        "iyr",  # (Issue Year)
        "eyr",  # (Expiration Year)
        "hgt",  # (Height)
        "hcl",  # (Hair Color)
        "ecl",  # (Eye Color)
        "pid",  # (Passport ID)
        # "cid",# (Country ID)
    ]
)
validator = {
    "byr": year(1920, 2002),  # (Birth Year)
    "iyr": year(2010, 2020),  # (Issue Year)
    "eyr": year(2020, 2030),  # (Expiration Year)
    "hgt": check_height,  # (Height)
    "hcl": lambda x: hair_color.match(x) is not None,  # (Hair Color)
    "ecl": lambda x: x in eye_color,  # (Eye Color)
    "pid": lambda x: len(x) == 9 and int(x) >= 0,  # (Passport ID)
    # "cid",# (Country ID)
}
count = 0
for pp in pps:
    if not set(pp.keys()).issuperset(required):
        print("missing keys")
        continue

    print(pp)
    all_good = True
    for k, v in pp.items():
        good = validator[k](v) if k in validator else True
        all_good = all_good and good

    if all_good:
        count += 1

print(count)
