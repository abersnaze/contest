from collections import Counter
from common.input import input

equations = []
for line in input():
    value, terms = line.split(": ", 1)
    terms = list(map(int, terms.split(" ")))
    equations.append((int(value), terms))


def is_valid(value, terms):
    possible = {terms[0]}
    for term in terms[1:]:
        next = set()
        for p in possible:
            next.add(p + term)
            next.add(p * term)
            next.add(int(str(p) + str(term)))
        possible = next
    return value in possible


calibration = 0
for value, terms in equations:
    if is_valid(value, terms):
        calibration += value

print(calibration)
