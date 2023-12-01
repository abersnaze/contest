#!python3

import fileinput
import re
from collections import Counter, defaultdict, deque
from enum import Enum, unique
from functools import reduce
from itertools import islice, product
from typing import Dict, List, Set, Tuple
import math

lines = list(map(lambda x: x.strip(), fileinput.input()))


class Scanner:
    beacons: Dict[str, Tuple[int, int, int]]
    # edges as list of distances between to beacon ids
    graph: List[Tuple[float, Tuple[str, str]]]

    def __init__(self) -> None:
        self.beacons = {}
        self.graph = []

    def __repr__(self) -> str:
        return str(self)

    def __str__(self) -> str:
        return str(len(self.beacons))


scanners = defaultdict(Scanner)
id = iter(range(10000000))
for line in lines:
    if not line:
        continue
    header = re.match(r"--- scanner (\d+) ---", line)
    if header:
        scanner_key = f"s{header.group(1)}"
    else:
        scanner = scanners[scanner_key]
        bid1 = f"{scanner_key}.b{next(id)}"
        bcord1 = tuple(map(int, line.split(",")))
        # fully connected edges
        for bid2, bcord2 in scanner.beacons.items():
            scanner.graph.append((math.dist(bcord1, bcord2), (bid1, bid2)))
        scanner.graph.sort(key=lambda edge: edge[0])
        scanners[scanner_key].beacons[bid1] = bcord1

scanner_pairs = list(
    map(
        tuple,
        filter(lambda id: id[0] < id[1], product(scanners.keys(), scanners.keys())),
    )
)


def find_alignment(potental, matches):
    if len(potental) == 0:
        return matches

    edge_a, edge_b = potental.pop()

    if edge_a[0] in matches:
        if edge_b[0] == matches[edge_a[0]]:
            if edge_a[1] in matches:
                if edge_b[1] != matches[edge_a[1]]:
                    # edge_a[1] conflicting matches
                    return None
            else:
                matches[edge_a[1]] = edge_b[1]
        elif edge_b[1] == matches[edge_a[0]]:
            if edge_a[1] in matches:
                if edge_b[0] != matches[edge_a[1]]:
                    # edge_a[1] conflicting matches
                    return None
            else:
                matches[edge_a[1]] = edge_b[0]
        else:
            # edge_a[0] conflicting matches
            return None
        return find_alignment(potental, matches)
    elif edge_a[1] in matches:
        # edge_a[0] is not in matches yet so match it
        if edge_b[0] == matches[edge_a[1]]:
            matches[edge_a[0]] = edge_b[1]
        elif edge_b[1] == matches[edge_a[1]]:
            matches[edge_a[0]] = edge_b[0]
        else:
            # edge_a[1] conflicting matches
            return None
        return find_alignment(potental, matches)
    else:
        # no matches yet
        matches[edge_a[0]] = edge_b[0]
        matches[edge_a[1]] = edge_b[1]
        out = find_alignment(potental, matches)
        if out:
            return out
        # try the other way around
        matches[edge_a[0]] = edge_b[1]
        matches[edge_a[1]] = edge_b[0]
        return find_alignment(potental, matches)


transforms = {}
beacons = {}
for said, sbid in scanner_pairs:
    # get two different scanners
    if said == sbid:
        continue
    sa = scanners[said]
    sb = scanners[sbid]

    # find all the edges that are the same distance
    by_dist = defaultdict(list)
    for ea in sa.graph:
        by_dist[ea[0]].append(ea[1])
    for eb in sb.graph:
        by_dist[eb[0]].append(eb[1])
    common_dists = {}
    for dist, matches in by_dist.items():
        if len(matches) == 2:
            common_dists[dist] = matches

    # see what beacons are matches
    alignment = find_alignment(list(common_dists.values()), {})

    # check for beacons that should have matched?

    for baid in sa.beacons:
        if baid not in beacons:
            beacons[baid] = baid
    for baid, bbid in alignment.items():
        beacons[bbid] = baid

    print(said, sbid, len(alignment), len(sb.beacons))

print("count of beacon coords", sum(map(lambda s: len(s.beacons), scanners.values())))
print("count of beacon mappings", len(beacons))
print("count of unique beacons", len(set(beacons.values())))
