from typing import Generator, NewType, Dict, Tuple, List
from collections import defaultdict
from math import inf

from common.math import sign

V = NewType("UserId", int)


class Space(Dict[Tuple[int, ...], V]):
    def __init__(self, default, to_str=str) -> None:
        self.default = default
        self.points = defaultdict(lambda: default)
        self.dim_range = None
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

    def range(self, depth: int) -> range:
        min_d, max_d = self.dim_range[depth]
        return range(min_d, max_d + 1)

    def dump(self, depth: int, path: List[int]) -> str:
        output = ""
        if path:
            output += "".join(map(self.to_str, path)) + "\n"
        if depth >= len(self.dim_range) - 2:
            for y in self.range(depth):
                for x in self.range(depth + 1):
                    coords = tuple(path + [x, y])
                    output += self.to_str(self.points.get(coords, self.default))
                output += "\n"
        else:
            for d in self.range(depth):
                output += self.dump(1, path + [d])
        return output

    def __rep__(self) -> str:
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
