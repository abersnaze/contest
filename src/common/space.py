from enum import Enum
from typing import Generator, NewType, Dict, Tuple, List
from collections import defaultdict
from math import inf, prod

from common.math import sign

V = NewType("UserId", int)


class Dir(Enum):
    N = (0, -1)
    E = (1, 0)
    S = (0, 1)
    W = (-1, 0)

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def turn(self, turn):
        if turn == "L":
            return Dir((-self.y, self.x))
        elif turn == "R":
            return Dir((self.y, -self.x))
        elif turn == "U":
            return Dir((-self.x, -self.y))
        elif turn == "F":
            return self
        else:
            raise ValueError(f"Unknown turn {turn}")

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __add__(self, other):
        return (self.x + other[0], self.y + other[1])

    def __radd__(self, other):
        return self.__add__(other)

    def __mul__(self, other):
        return Dir((self.x * other, self.y * other))

    def __rmul__(self, other):
        return self.__mul__(other)

    def __hash__(self):
        return hash((self.x, self.y))


def adjacent4(p):
    yield p + Dir.N
    yield p + Dir.E
    yield p + Dir.S
    yield p + Dir.W


def adjacent8(p):
    yield p + Dir.N
    yield p + Dir.N + Dir.E
    yield p + Dir.E
    yield p + Dir.E + Dir.S
    yield p + Dir.S
    yield p + Dir.S + Dir.W
    yield p + Dir.W
    yield p + Dir.W + Dir.N


class Space(Dict[Tuple[int, ...], V]):
    def __init__(self, default, to_str=str, dim_range=None) -> None:
        self.default = default
        self.points = defaultdict(lambda: default)
        self.dim_range = dim_range
        self.to_str = to_str

    def __getitem__(self, key: Tuple[int, ...]) -> V:
        return self.points[key]

    def __setitem__(self, key: Tuple[int, ...], value: V) -> None:
        if self.dim_range is None:
            self.dim_range = [(inf, -inf) for i in range(len(key))]
        # keep track the range for each dimension
        for i, k in enumerate(key):
            min_k, max_k = self.dim_range[i]
            self.dim_range[i] = (min(min_k, k), max(max_k, k))
        self.points[key] = value

    def __iadd__(self, other: Tuple[int, ...]) -> None:
        self[other] += 1

    def __len__(self) -> int:
        return len(self.points)

    def __contains__(self, key) -> bool:
        return key in self.points

    def range(self, depth: int) -> range:
        min_d, max_d = self.dim_range[depth]
        return range(min_d, max_d + 1)

    def dump(self, depth: int, path: List[int]) -> str:
        output = ""
        if path:
            output += "".join(map(self.to_str, path)) + "\n"
        if self.dim_range is None:
            return "empty"
        if depth >= len(self.dim_range) - 2:
            if self.dim_range[depth][1] - self.dim_range[depth][0] > 200:
                return "too big"
            if self.dim_range[depth + 1][1] - self.dim_range[depth + 1][0] > 200:
                return "too big"
            for y in self.range(depth + 1):
                for x in self.range(depth):
                    coords = tuple(path + [x, y])
                    output += self.to_str(self.points.get(coords, self.default))
                output += "\n"
        else:
            for d in self.range(depth):
                output += self.dump(1, path + [d])
        return output

    def copy(self):
        x = Space(self.default, self.to_str, self.dim_range)
        x.points = self.points.copy()
        return x
    
    def area(self):
        return prod([max - min for min, max in self.dim_range])

    def __repr__(self) -> str:
        return str(len(self.points)) + "/" + str(self.area())
    
    def __str__(self) -> str:
        return self.dump(0, [])


def line(
    frm: Tuple[int, ...], to: Tuple[int, ...]
) -> Generator[Tuple[int, ...], None, None]:
    """N-dimensional bresenham line drawing algorithm through a space"""
    print("#################")
    deltas = [t - f for t, f in zip(to, frm)]
    steps = [sign(delta) for delta in deltas]
    corrections = [2 * abs(delta) for delta in deltas]
    max_delta = max(corrections) >> 1
    error = [max_delta for correction in corrections]
    curr = list(frm)
    c = frm
    print("x\td\ts\tc\te\tm")

    def dump(i):
        print(
            f"{c[i]}\t{deltas[i]}\t{steps[i]}\t{corrections[i]}\t{error[i]}\t{max_delta}"
        )

    watch = 1
    dump(watch)
    for i in range(max_delta):
        yield c
        for dim, correction in enumerate(corrections):
            if error[dim] > 0:
                curr[dim] += steps[dim]
                error[dim] -= max_delta
            error[dim] += correction
        c = tuple(curr)
        dump(watch)
    yield c
