import pytest
from common.input import compile, compile_literal, compile_match, compile_pattern


def test_compile_match_named():
    pattern, i = compile_match("<int:age>", 0)
    assert i == 9
    assert pattern("12", 0, None) == ({"age": 12}, 2)
    assert pattern("12", 0, {"name": "bob"}) == ({"age": 12, "name": "bob"}, 2)
    assert pattern("12", 0, {"age": 13}) == ({"age": 12}, 2)


def test_compile_match_unnamed():
    pattern, i = compile_match("<int>", 0)
    assert i == 5
    assert pattern("12", 0, None) == ((12,), 2)
    assert pattern("12", 0, ("bob",)) == (("bob", 12), 2)


float_inputs = ["12.3", "-12.3", "+12.3", "12.3e4", "12.3e-4", "12.3e+4", "12.3e+4"]


@pytest.mark.parametrize("input", float_inputs)
def test_compile_match_float(input):
    pattern, i = compile_match("<float>", 0)
    assert i == 7
    expected = ((float(input),), len(input))
    actual = pattern(input, 0, None)
    assert actual == expected, f"{input} -> {actual} != {expected}"


def test_compile_match_bool():
    pattern, i = compile_match("<bool>", 0)
    assert i == 6
    assert pattern("true", 0, None) == ((True,), 4)
    assert pattern("false", 0, None) == ((False,), 5)


def test_compile_match_str():
    pattern, i = compile_match("<str>", 0)
    assert i == 5
    assert pattern("asdf.", 0, None) == (("asdf",), 4)
    assert pattern("asdf ", 0, None) == (("asdf",), 4)


def test_compile_match_literal():
    pattern, i = compile_pattern("asdf", 0)
    assert i == 4
    assert pattern("asdf", 0, None) == (None, 4)
    # if the literal doesn't match, it should raise an exception
    try:
        pattern("asd", 0, None)
    except Exception as e:
        assert str(e) == "Expected asdf, but got asd"


cases = [
    ("<int>,<int> -> <int>,<int>", "12,13 -> 14,15", (12, 13, 14, 15)),
    ("move <int> from <int> to <int>", "move 2 from 3 to 4", (2, 3, 4)),
]


@pytest.mark.parametrize("pattern, input, expected", cases)
def test_compile_match_combined(pattern, input, expected):
    parser = compile(pattern)
    actual = parser(input)
    assert actual == expected, f"{pattern} -> parser({input}) -> {actual} != {expected}"


def test_compile_list_unnamed():
    pattern = compile("[<int> ]")
    assert pattern("") == ([],)
    assert pattern("1 2 3") == ([1, 2, 3],)


def test_compile_list_named():
    pattern = compile("[<int>, :numbers]")
    assert pattern("") == ({"numbers": []})
    assert pattern("1 2 3") == ({"numbers": [1, 2, 3]})


def test_backtrack():
    pattern = compile("<str> <int>")
    assert pattern("turn off 1") == ("turn off", 1)
