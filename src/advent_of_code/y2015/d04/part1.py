#!/usr/bin/env python3

from hashlib import md5
from math import inf
from fileinput import input
from common.space import Space
from common.space import Dir


def ingest(files=None):
    return next(input(files)).strip()


def process(key):
    i = 0
    while True:
        data = key + str(i)
        code = md5(data.encode("utf-8")).digest().hex()
        if code[:5] == "00000":
            return i
        i += 1


def output(data):
    print(data)


if __name__ == "__main__":
    output(process(ingest()))
