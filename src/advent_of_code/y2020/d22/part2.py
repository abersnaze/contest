#!python3

import fileinput
import re
from collections import defaultdict
import sys

pattern = re.compile("Player \d+:")
game = {}
count = 0
for line in map(lambda x: x.strip(), fileinput.input()):
    res = pattern.match(line)
    if res:
        deck = []
        game[res.group(0)] = deck
    elif line:
        deck.append(int(line))
        count += 1

print(game)


def winner(g):
    global count
    leader = max([(p[0], len(p[1])) for p in g.items()], key=lambda x: x[1])
    print("leader", leader, count)
    if leader[1] == count:
        cards = list(
            map(lambda x: (x[0] + 1) * x[1], enumerate(reversed(g[leader[0]])))
        )
        print("winning cards", cards)
        return (leader, sum(cards))
    return None


def do_round(g):
    high_card = -1
    high_player = None
    cards = []
    print(g)
    for player, deck in g.items():
        card = deck.pop(0)
        cards.append(card)
        if card > high_card:
            high_card = card
            high_player = player
    print("cards played", cards)
    print("round winner is", high_player, "with", high_card)
    g[high_player].extend(sorted(cards, reverse=True))


prev = set()
w = winner(game)
while not w:
    # no repeats
    state = tuple(map(tuple, game.values()))
    if state in prev:
        print("repeat", game)
        break
    prev.add(state)

    do_round(game)
    w = winner(game)

print(w)
