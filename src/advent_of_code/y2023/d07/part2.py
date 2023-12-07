#!/usr/bin/env python3

from collections import Counter, defaultdict
from fileinput import input
from functools import cmp_to_key
from math import ceil, floor, prod, sqrt
import math

points = {
    "A": 14,
    "K": 13,
    "Q": 12,
    "J": 1,
    "T": 10,
    "9": 9,
    "8": 8,
    "7": 7,
    "6": 6,
    "5": 5,
    "4": 4,
    "3": 3,
    "2": 2,
}


def ingest(files=None):
    hands = []
    for i, line in enumerate(input(files)):
        cards, bid = line.strip().split()
        cards = tuple(map(lambda c: points.get(c), cards))
        hand = Counter(cards)
        hands.append((cards, int(bid), classify_with_jokers(hand)))
    return hands


def compare(a, b):
    cards_a, bid_a, rank_a = a
    cards_b, bid_b, rank_b = b
    if rank_a > rank_b:
        return 1
    elif rank_a < rank_b:
        return -1

    if cards_a > cards_b:
        return 1
    elif cards_a < cards_b:
        return -1
    return 0


def classify_with_jokers(hand: Counter):
    max_rank = classify(hand)
    if 1 in hand:
        _hand = hand.copy()
        jokers = _hand[1]
        del _hand[1]
        for card in _hand:
            _hand[card] += jokers
            max_rank = max(max_rank, classify(_hand))
            _hand[card] -= jokers
    return max_rank


def classify(hand: Counter):
    # Five of a kind, where all five cards have the same label: AAAAA
    groups = hand.most_common(2)
    if groups[0][1] == 5:
        return 7

    # Four of a kind, where four cards have the same label and one card has a different label: AA8AA
    if groups[0][1] == 4:
        return 6

    # Full house, where three cards have the same label, and the remaining two cards share a different label: 23332
    if groups[0][1] == 3 and groups[1][1] == 2:
        return 5

    # Three of a kind, where three cards have the same label, and the remaining two cards are each different from any other card in the hand: TTT98
    if groups[0][1] == 3:
        return 4

    # Two pair, where two cards share one label, two other cards share a second label, and the remaining card has a third label: 23432
    if groups[0][1] == 2 and groups[1][1] == 2:
        return 3

    # One pair, where two cards share one label, and the other three cards have a different label from the pair and each other: A23A4
    if groups[0][1] == 2:
        return 2

    # High card, where all cards' labels are distinct: 23456
    return 1


def process(hands):
    ranked = sorted(hands, key=cmp_to_key(compare), reverse=False)
    scores = [((i + 1), bid) for i, (hand, bid, cls) in enumerate(ranked)]
    return sum(map(math.prod, scores))


def output(data):
    print(data)


if __name__ == "__main__":
    output(process(ingest()))
