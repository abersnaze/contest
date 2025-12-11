import regex as re
from common.input import input
from collections import Counter

lines = input()
invalid = []


def is_valid(i):
    s = str(i)
    freqs = set(Counter(s).values())
    if len(freqs) > 1:
        reps = min(freqs)
        if reps == 1:
            return True
        for freq in freqs:
            # if not all the digits appear an even number of times
            if freq % reps != 0:
                return True
    else:
        reps = freqs.pop()
        if reps == 1:
            return True
    # the string is invalide if its reps of a chunk
    chunk = s[0 : (len(s) // reps)]
    rep_chunks = chunk * reps
    valid = rep_chunks != s
    return valid

print(is_valid(10011001))
print(is_valid(6464664646))

# for line in lines:
#     smol, larg = line.split("-")
#     for i in range(int(smol), int(larg) + 1, 1):
#         if is_valid(i) is False:
#             invalid.append(i)

print(invalid)
print(sum(invalid))
