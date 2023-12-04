#!/usr/bin/env python3

from collections import defaultdict
from fileinput import input

from common.space import Dir, Space, adjencent8


def ingest(files=None):
    cards = {}
    for line in input(files):
        id, win_nums, pick_nums = parse(line.strip().replace("  ", " "))
        cards[id] = (win_nums, pick_nums)
    return (cards,)


def parse(line):
    # Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53

    card, numbers = line.strip().split(":")
    id = int(card[5:])
    win_nums, pick_nums = numbers.split("|")
    win_nums = list(map(int, win_nums.strip().split(" ")))
    pick_nums = list(map(int, pick_nums.strip().split(" ")))

    return id, win_nums, pick_nums


def process(cards):
    scores = []
    for card, nums in cards.items():
        win_nums, pick_nums = nums
        score = score_card(win_nums, pick_nums)
        print(card, score)
        scores.append(score)
    return sum(scores)


def score_card(win_nums, pick_nums):
    score = 0
    for pick in pick_nums:
        if pick in win_nums:
            if score == 0:
                score = 1
            else:
                score *= 2
    return score


def output(data):
    print(data)


if __name__ == "__main__":
    output(process(*ingest()))
