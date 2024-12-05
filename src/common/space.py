from enum import Enum
from typing import Generator, NewType, Dict, Tuple, List
from collections import defaultdict
from math import inf, prod

from common.math import sign

V = NewType("UserId", int)


class Dir4(Enum):
    N = (0, -1)
    E = (1, 0)
    S = (0, 1)
    W = (-1, 0)

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def turn(self, turn):
        if turn == "L":
            return Dir4((-self.y, self.x))
        elif turn == "R":
            return Dir4((self.y, -self.x))
        elif turn == "U":
            return Dir4((-self.x, -self.y))
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

    def __hash__(self):
        return hash((self.x, self.y))


class Dir8(Enum):
    N = (0, -1)
    NE = (1, -1)
    E = (1, 0)
    SE = (1, 1)
    S = (0, 1)
    SW = (-1, 1)
    W = (-1, 0)
    NW = (-1, -1)

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def __add__(self, other):
        return (self.x + other[0], self.y + other[1])

    def __radd__(self, other):
        return self.__add__(other)

    def __hash__(self):
        return hash((self.x, self.y))


def adjacent4(p):
    for d in Dir4:
        yield p + d


def adjacent8(p):
    for d in Dir8:
        yield p + d


class Space(Dict[Tuple[int, ...], V]):
    def __init__(
        self,
        default=".",
        to_str=str,
        dim_range=None,
        points=None,
        func=lambda p: (p[0], p[1]),
        unfunc=lambda p: (p[0], p[1]),
    ) -> None:
        self._default = default
        self._points = defaultdict(lambda: default) if points is None else points
        self._dim_range = dim_range
        self._to_str = to_str
        self._func = func
        self._unfunc = unfunc

    def __getitem__(self, key: Tuple[int, ...]) -> V:
        return self._points[self._func(key)]

    def __setitem__(self, key: Tuple[int, ...], value: V) -> None:
        if self._dim_range is None:
            self._dim_range = [(inf, -inf) for i in range(len(key))]
        # keep track the range for each dimension
        for i, k in enumerate(key):
            min_k, max_k = self._dim_range[i]
            self._dim_range[i] = (min(min_k, k), max(max_k, k))
        self._points[self._func(key)] = value

    def keys(self):
        return map(self._unfunc, self._points.keys())

    def __iadd__(self, other: Tuple[int, ...]) -> None:
        self[self._func(other)] += 1

    def __len__(self) -> int:
        return len(self._points)

    def __contains__(self, key) -> bool:
        return self._func(key) in self._points

    def range(self, depth: int) -> range:
        min_d, max_d = self._func(self._dim_range)[depth]
        return range(min_d, max_d + 1)

    def dump(self, depth: int, path: List[int]) -> str:
        output = ""
        if path:
            output += "".join(map(self._to_str, path)) + "\n"
        if self._dim_range is None:
            return "empty"
        if depth >= len(self._dim_range) - 2:
            if self._dim_range[depth][1] - self._dim_range[depth][0] > 200:
                return "too big"
            if self._dim_range[depth + 1][1] - self._dim_range[depth + 1][0] > 200:
                return "too big"
            for y in self.range(depth + 1):
                for x in self.range(depth):
                    coords = tuple(path + [x, y])
                    coords = self._func(coords)
                    output += self._to_str(self._points.get(coords, self._default))
                output += "\n"
        else:
            for d in self.range(depth):
                output += self.dump(1, path + [d])
        return output

    def copy(self):
        return Space(
            default=self._default,
            to_str=self._to_str,
            dim_range=self._dim_range,
            points=self._points.copy(),
            func=self._func,
        )

    def area(self):
        return prod([max - min for min, max in self._dim_range])

    def __repr__(self) -> str:
        return str(len(self._points)) + "/" + str(self.area())

    def __str__(self) -> str:
        return self.dump(0, [])

    def transform(self, func):
        new_space = Space(
            default=self._default,
            to_str=self._to_str,
            dim_range=self._dim_range,
            func=func,
        )
        for key, value in self._points.items():
            new_space[func(key)] = value
        return new_space


class Matrix3:
    def __init__(self, values):
        self.m00, self.m01, self.m02 = values[0]
        self.m10, self.m11, self.m12 = values[1]
        self.m20, self.m21, self.m22 = values[2]

    @staticmethod
    def rotateLeft():
        return Matrix3(((0, -1, 0), (1, 0, 0), (0, 0, 1)))

    @staticmethod
    def rotateRight():
        return Matrix3(((0, 1, 0), (-1, 0, 0), (0, 0, 1)))

    @staticmethod
    def rotate180():
        return Matrix3(((-1, 0, 0), (0, -1, 0), (0, 0, 1)))

    @staticmethod
    def flipHorizontal():
        return Matrix3(((-1, 0, 0), (0, 1, 0), (0, 0, 1)))

    @staticmethod
    def flipVertical():
        return Matrix3(((1, 0, 0), (0, -1, 0), (0, 0, 1)))

    @staticmethod
    def translate(x, y):
        return Matrix3(((1, 0, x), (0, 1, y), (0, 0, 1)))

    @staticmethod
    def scale(x, y):
        return Matrix3(((x, 0, 0), (0, y, 0), (0, 0, 1)))

    @staticmethod
    def transpose():
        return Matrix3(((0, 1, 0), (1, 0, 0), (0, 0, 1)))

    def __mul__(self, other):
        if isinstance(other, Matrix3):
            m00 = self.m00 * other.m00 + self.m01 * other.m10 + self.m02 * other.m20
            m01 = self.m00 * other.m01 + self.m01 * other.m11 + self.m02 * other.m21
            m02 = self.m00 * other.m02 + self.m01 * other.m12 + self.m02 * other.m22
            m10 = self.m10 * other.m00 + self.m11 * other.m10 + self.m12 * other.m20
            m11 = self.m10 * other.m01 + self.m11 * other.m11 + self.m12 * other.m21
            m12 = self.m10 * other.m02 + self.m11 * other.m12 + self.m12 * other.m22
            m20 = self.m20 * other.m00 + self.m21 * other.m10 + self.m22 * other.m20
            m21 = self.m20 * other.m01 + self.m21 * other.m11 + self.m22 * other.m21
            m22 = self.m20 * other.m02 + self.m21 * other.m12 + self.m22 * other.m22
            return Matrix3(((m00, m01, m02), (m10, m11, m12), (m20, m21, m22)))
        elif isinstance(other, Tuple):
            other_z = other[2] if len(other) > 2 else 1
            x = self.m00 * other[0] + self.m01 * other[1] + self.m02 * other_z
            y = self.m10 * other[0] + self.m11 * other[1] + self.m12 * other_z
            z = self.m20 * other[0] + self.m21 * other[1] + self.m22 * other_z
            return (x, y, z) if len(other) > 2 else (x, y)

    def __rmul__(self, other):
        if isinstance(other, Matrix3):
            m00 = other.m00 * self.m00 + other.m01 * self.m10 + other.m02 * self.m20
            m01 = other.m00 * self.m01 + other.m01 * self.m11 + other.m02 * self.m21
            m02 = other.m00 * self.m02 + other.m01 * self.m12 + other.m02 * self.m22
            m10 = other.m10 * self.m00 + other.m11 * self.m10 + other.m12 * self.m20
            m11 = other.m10 * self.m01 + other.m11 * self.m11 + other.m12 * self.m21
            m12 = other.m10 * self.m02 + other.m11 * self.m12 + other.m12 * self.m22
            m20 = other.m20 * self.m00 + other.m21 * self.m10 + other.m22 * self.m20
            m21 = other.m20 * self.m01 + other.m21 * self.m11 + other.m22 * self.m21
            m22 = other.m20 * self.m02 + other.m21 * self.m12 + other.m22 * self.m22
            return Matrix3(((m00, m01, m02), (m10, m11, m12), (m20, m21, m22)))
        elif isinstance(other, Tuple):
            other_z = other[2] if len(other) > 2 else 1
            x = other[0] * self.m00 + other[1] * self.m10 + other_z * self.m20
            y = other[0] * self.m01 + other[1] * self.m11 + other_z * self.m21
            z = other[0] * self.m02 + other[1] * self.m12 + other_z * self.m22
            return (x, y, z) if len(other) > 2 else (x, y)

    def inverse(self):
        det = (
            self.m00 * self.m11 * self.m22
            + self.m01 * self.m12 * self.m20
            + self.m02 * self.m10 * self.m21
            - self.m02 * self.m11 * self.m20
            - self.m01 * self.m10 * self.m22
            - self.m00 * self.m12 * self.m21
        )
        m00 = (self.m11 * self.m22 - self.m12 * self.m21) / det
        m01 = (self.m02 * self.m21 - self.m01 * self.m22) / det
        m02 = (self.m01 * self.m12 - self.m02 * self.m11) / det
        m10 = (self.m12 * self.m20 - self.m10 * self.m22) / det
        m11 = (self.m00 * self.m22 - self.m02 * self.m20) / det
        m12 = (self.m02 * self.m10 - self.m00 * self.m12) / det
        m20 = (self.m10 * self.m21 - self.m11 * self.m20) / det
        m21 = (self.m01 * self.m20 - self.m00 * self.m21) / det
        m22 = (self.m00 * self.m11 - self.m01 * self.m10) / det
        return Matrix3(((m00, m01, m02), (m10, m11, m12), (m20, m21, m22)))


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
