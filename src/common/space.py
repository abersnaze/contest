from enum import Enum
from typing import Any, Generator, NewType, Dict, Optional, Tuple, List
from collections import defaultdict
from math import cos, inf, pi, prod, sin

from common.math import sign


class Point(Tuple[int, ...]):
    def __add__(self, other):
        return Point(ai + bi for ai, bi in zip(self, other))

    def __sub__(self, other):
        return Point(ai - bi for ai, bi in zip(self, other))

    def __mul__(self, other):
        return Point(ai * other for ai in self)

    def __truediv__(self, other):
        return Point(ai / other for ai in self)

    def __floordiv__(self, other):
        return Point(ai // other for ai in self)

    def __mod__(self, other):
        return Point(ai % other for ai in self)

    def __pow__(self, other):
        return Point(ai**other for ai in self)

    def __lshift__(self, other):
        return Point(ai << other for ai in self)

    def __rshift__(self, other):
        return Point(ai >> other for ai in self)

    def __and__(self, other):
        return Point(ai & other for ai in self)

    def __xor__(self, other):
        return Point(ai ^ other for ai in self)

    def __or__(self, other):
        return Point(ai | other for ai in self)

    def __radd__(self, other):
        return Point(ai + bi for ai, bi in zip(other, self))

    def __rsub__(self, other):
        return Point(ai - bi for ai, bi in zip(other, self))

    def __rmul__(self, other):
        return Point(ai * other for ai in self)

    def __rtruediv__(self, other):
        return Point(ai / other for ai in self)

    def __rfloordiv__(self, other):
        return Point(ai // other for ai in self)

    def __rmod__(self, other):
        return Point(ai % other for ai in self)

    def __rpow__(self, other):
        return Point(ai**other for ai in self)

    def __rlshift__(self, other):
        return Point(ai << other for ai in self)

    def __rrshift__(self, other):
        return Point(ai >> other for ai in self)

    def __rand__(self, other):
        return Point(ai & other for ai in self)

    def __rxor__(self, other):
        return Point(ai ^ other for ai in self)

    def manhattan(self):
        return sum(map(abs, self))


class Dir2(Enum):
    NS = Point((1, 0))
    EW = Point((0, 1))

    def __repr__(self):
        return self.name


class Dir4(Enum):
    N = Point((0, -1))
    E = Point((1, 0))
    S = Point((0, 1))
    W = Point((-1, 0))

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def turn(self, turn):
        if turn == "L":
            return Dir4((self.y, -self.x))
        elif turn == "R":
            return Dir4((-self.y, self.x))
        elif turn == "U":
            return -self
        elif turn == "F":
            return self
        else:
            raise ValueError(f"Unknown turn {turn}")

    def __str__(self):
        if self == Dir4.N:
            return "^"
        if self == Dir4.E:
            return ">"
        if self == Dir4.S:
            return "v"
        if self == Dir4.W:
            return "<"

    def __repr__(self):
        return self.name

    def __add__(self, other):
        return (self.x + other[0], self.y + other[1])

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        return (self.x - other[0], self.y - other[1])

    def __rsub__(self, other):
        return (other[0] - self.x, other[1] - self.y)

    def __hash__(self):
        return hash((self.x, self.y))

    def __neg__(self):
        return Dir4((-self.x, -self.y))


class Dir8(Enum):
    N = Point((0, -1))
    NE = Point((1, -1))
    E = Point((1, 0))
    SE = Point((1, 1))
    S = Point((0, 1))
    SW = Point((-1, 1))
    W = Point((-1, 0))
    NW = Point((-1, -1))

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return self.name


def adjacent4(p):
    for d in Dir4:
        yield p + d.value


def adjacent8(p):
    for d in Dir8:
        yield p + d.value


class Space(Dict[Tuple[int, ...], Any]):
    def __init__(
        self,
        default=".",
        to_str=str,
        dim_range=None,
        points=None,
        func=lambda p: Point(p),
        unfunc=lambda p: Point(p),
        under_layer: Optional["Space"] = None,
    ) -> None:
        self._default = default
        self._points = defaultdict(lambda: default) if points is None else points
        self._dim_range = dim_range
        self._to_str = to_str
        self._func = func
        self._unfunc = unfunc
        self._under_layer = under_layer
        self._values = defaultdict(set)

    @staticmethod
    def read(input, vfunc=lambda p: p, **kwargs):
        space = Space(**kwargs)
        for y, line in enumerate(input):
            if line == "":
                break
            for x, char in enumerate(line):
                if char == space._default:
                    space.cover((x, y))
                else:
                    space[(x, y)] = vfunc(char)
        return space

    def index(self, value) -> Generator[Tuple[int, ...], None, None]:
        return self._values[value]

    def __getitem__(self, key: Tuple[int, ...]) -> Any:
        value = self._points.get(self._func(key), self._default)
        if callable(value):
            value = value()
            self._points[self._func(key)] = value
        return value

    def __setitem__(self, key: Tuple[int, ...], value: Any) -> None:
        self.cover(key)
        func_key = self._func(key)
        # Clean up old reverse index entry if key already exists
        if func_key in self._points:
            old_value = self._points[func_key]
            self._values[old_value].discard(key)
        self._points[func_key] = value
        self._values[value].add(key)

    def cover(self, key):
        if self._dim_range is None:
            self._dim_range = [(inf, -inf) for i in range(len(key))]
        # keep track the range for each dimension
        for i, k in enumerate(key):
            if type(k) == int:
                min_k, max_k = self._dim_range[i]
                self._dim_range[i] = (min(min_k, k), max(max_k, k))
            else:
                if type(self._dim_range[i]) != set:
                    self._dim_range[i] = set()
                self._dim_range[i].add(k)

    def __delitem__(self, key: Tuple[int, ...]) -> None:
        func_key = self._func(key)
        if func_key in self._points:
            old_value = self._points[func_key]
            self._values[old_value].discard(key)
            del self._points[func_key]

    def inside(self, key: Tuple[int, ...]) -> bool:
        if self._dim_range is None:
            return True
        for i, k in enumerate(key):
            if type(k) == int:
                min_k, max_k = self._dim_range[i]
                if k < min_k or k > max_k:
                    return False
            else:
                if k not in self._dim_range[i]:
                    return False
        return True

    def items(self):
        return map(lambda i: (self._unfunc(i[0]), i[1]), self._points.items())

    def keys(self):
        return map(self._unfunc, self._points.keys())

    def values(self):
        return self._values.keys()

    def __iadd__(self, other: Tuple[int, ...]) -> None:
        self[self._func(other)] += 1

    def __len__(self) -> int:
        return len(self._points)

    def __contains__(self, key) -> bool:
        return self._func(key) in self._points

    def minmax(self, depth: int) -> Tuple[int, int]:
        return self._dim_range[depth]

    def range(self, depth: int) -> range:
        if type(self._dim_range[depth]) == tuple:
            min_d, max_d = self._func(self._dim_range)[depth]
            return range(min_d, max_d + 1)
        return iter(self._dim_range[depth])

    def len(self, depth: int) -> int:
        if type(self._dim_range[depth]) == tuple:
            min_d, max_d = self._func(self._dim_range)[depth]
            return max_d - min_d
        return len(self._dim_range[depth])

    def project(self, rm_depth: int, **kwargs) -> "Space":
        output = Space(**kwargs, default=lambda: defaultdict(lambda: self._default))
        for key, value in self.items():
            shadow_key = key[:rm_depth] + key[rm_depth + 1 :]
            output.cover(shadow_key)
            output[shadow_key][key[rm_depth]] = value
        return output

    def dump(self, depth: int, path: List[int]) -> str:
        output = ""
        if path:
            output += "".join(map(str, path)) + "\n"
        if self._dim_range is None:
            return "empty"
        if depth >= len(self._dim_range) - 2:
            if self.len(depth) > 200:
                return "too big"
            for y in self.range(depth + 1):
                for x in self.range(depth):
                    coords = tuple(path + [x, y])
                    coords = self._func(coords)
                    output += self._to_str(self[coords])
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
    def rotateLeft(x=0, y=0):
        if x != 0 or y != 0:
            return (
                Matrix3.translate(x, y)
                * Matrix3.rotateLeft()
                * Matrix3.translate(-x, -y)
            )
        return Matrix3(((0, -1, 0), (1, 0, 0), (0, 0, 1)))

    @staticmethod
    def rotateRight(x=0, y=0):
        if x != 0 or y != 0:
            return (
                Matrix3.translate(x, y)
                * Matrix3.rotateLeft()
                * Matrix3.translate(-x, -y)
            )
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
    frms: Tuple[int, ...], tos: Tuple[int, ...]
) -> Generator[Tuple[int, ...], None, None]:
    """N-dimensional bresenham line drawing algorithm through a space"""

    def nth(frm, to, n):
        delta = to - frm
        # return a tuple with the nth element set to sign and all others set to 0
        step = tuple(sign(delta) if i == n else 0 for i in range(len(frms)))
        return (abs(delta), step)

    def add(p1, p2):
        for i in range(len(p1)):
            p1[i] += p2[i]

    pairs = [nth(frm, to, i) for i, (to, frm) in enumerate(zip(tos, frms))]
    pairs.sort(reverse=True, key=lambda x: x[0])
    steps = tuple(map(lambda x: x[1], pairs))
    deltas = tuple(map(lambda x: x[0], pairs))
    # the corrections start at half the max delta
    max_delta = deltas[0]
    errors = [abs(max_delta) / 2.0] * len(frms)

    curr = list(frms)
    for i in range(max_delta):
        yield tuple(curr)
        for dim in range(len(errors)):
            errors[dim] -= deltas[dim]
            if errors[dim] < 0:
                add(curr, steps[dim])
                errors[dim] += max_delta
    yield tuple(curr)


def square(frms: Tuple[int, ...], tos: Tuple[int, ...], fill=False):
    for x in range(frms[0], tos[0] + 1):
        if fill or x in (frms[0], tos[0]):
            for y in range(frms[1], tos[1] + 1):
                yield (x, y)
        else:
            yield (x, frms[1])
            yield (x, tos[1])
