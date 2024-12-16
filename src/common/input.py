from fileinput import input as file_input
from typing import Callable, Dict, Optional, Tuple


def add_to(context: Optional[Dict | Tuple], value: Dict | Tuple) -> Dict | Tuple:
    if context is None:
        return value
    if isinstance(context, dict):
        if isinstance(value, dict):
            return context | value
        raise Exception(
            f"{context.keys()} are named variables, but {value} is not a named variable"
        )
    elif isinstance(context, tuple):
        if isinstance(value, tuple):
            return context + value
        raise Exception(
            f"{context} is an unnamed variable, but {value} is a named variable"
        )


def extract_type(pattern: str, i: int):
    remaining_pattern = pattern[i:]
    if remaining_pattern.startswith("<int"):
        # find the digits in the input starting at j
        def parse_int(input, j):
            digits = ""
            while j < len(input) and (input[j].isdigit() or input[j] in "+-"):
                digits += input[j]
                j += 1
            return int(digits), j

        return parse_int, i + 4
    if remaining_pattern.startswith("<str"):
        # find the characters ending at a word boundry in the input starting at j
        def parse_str(input, j):
            chars = ""
            while j < len(input) and input[j].isalpha():
                chars += input[j]
                j += 1
            return chars, j

        return parse_str, i + 4
    if remaining_pattern.startswith("<float"):
        # find the digits in the input starting at j
        def parse_float(input, j):
            digits = ""
            if j < len(input) and (input[j] == "-" or input[j] == "+"):
                digits += input[j]
                j += 1
            while j < len(input) and input[j].isdigit():
                digits += input[j]
                j += 1
            if j < len(input) and input[j] == ".":
                digits += "."
                j += 1
                while j < len(input) and input[j].isdigit():
                    digits += input[j]
                    j += 1
            if j < len(input) and input[j] == "e":
                digits += "e"
                j += 1
                if j < len(input) and (input[j] == "-" or input[j] == "+"):
                    digits += input[j]
                    j += 1
                while j < len(input) and input[j].isdigit():
                    digits += input[j]
                    j += 1
            return float(digits), j

        return parse_float, i + 6
    if remaining_pattern.startswith("<bool"):

        def parse_bool(input, j):
            if input[j : j + 4].lower() == "true":
                return True, j + 4
            if input[j : j + 5].lower() == "false":
                return False, j + 5
            raise Exception(f"Expected true or false, but got {input[j:]}")

        return parse_bool, i + 5
    raise Exception(
        f"Unknown type {remaining_pattern} expected <int, <str, <float, or <bool"
    )


def extract_name(pattern: str, i: int):
    name = ""
    i += 1
    while i < len(pattern) and pattern[i] != ">":
        name += pattern[i]
        i += 1
    return name, i + 1


def compile_match(pattern: str, i: int) -> Tuple[
    Callable[[str, int, Optional[Dict | Tuple]], Tuple[Optional[Dict | Tuple], int]],
    int,
]:
    func, i = extract_type(pattern, i)
    if pattern[i] == ":":
        name, i = extract_name(pattern, i)

        def match(input, j, context):
            value, j = func(input, j)
            return add_to(context, {name: value}), j

        return match, i
    elif pattern[i] == ">":

        def match(input, j, context):
            value, j = func(input, j)
            return add_to(context, (value,)), j

        return match, i + 1


def compile_list(pattern: str, i: int) -> Tuple[
    Callable[[str, int, Optional[Dict | Tuple]], Tuple[Optional[Dict | Tuple], int]],
    int,
]:
    end = pattern.index("]", i)
    try:
        name_start = pattern.index(":", i, end)
        name = pattern[name_start + 1 : end]
        end = name_start
    except ValueError:
        name = None
    func, i = extract_type(pattern[:end], i)
    sep, _ = compile_pattern(pattern[i + 1 : end], 0)
    i = end
    if pattern[i] == ":":
        name, i = extract_name(pattern, i)

        def match(input, j, context):
            values = []
            while j < len(input) and input[j] != "]":
                value, j = func(input, j)
                values.append(value)
            return add_to(context, {name: values}), j + 1

        return match, i
    elif pattern[i] == "]":

        def match(input, j, context):
            values = []
            while j < len(input):
                value, j = func(input, j)
                values.append(value)
                success = sep(input, j, None)
                if success is None:
                    break
            return add_to(context, (values,)), j + 1

        return match, i


def compile_literal(
    pattern: str, i: int
) -> Tuple[
    Callable[[str, Optional[Dict | Tuple]], Tuple[Optional[Dict | Tuple], int]], int
]:
    def match_literal(input, j, context):
        if j >= len(input) or input[j] != pattern[i]:
            raise Exception(f"Expected {pattern}, but got {input}")
        return context, j + 1

    return match_literal, i + 1


def match_empty(input: str, j: int, context: Optional[Dict | Tuple]):
    return context, j


def chain(func1, func2):
    def helper(input, j, context):
        context, j = func1(input, j, context)
        return func2(input, j, context)

    return helper


def compile_pattern(
    pattern: str, i: int
) -> Tuple[
    Callable[[str, Optional[Dict | Tuple]], Tuple[Optional[Dict | Tuple], int]], int
]:
    func = match_empty
    while i < len(pattern):
        if pattern[i] == "<":
            var_func, i = compile_match(pattern, i)
            func = chain(func, var_func)
        elif pattern[i] == "[":
            list_func, i = compile_list(pattern, i + 1)
            func = chain(func, list_func)
            i += 1
        else:
            lit_func, i = compile_literal(pattern, i)
            func = chain(func, lit_func)
    return func, i


def compile(pattern: str) -> Optional[Dict | Tuple]:
    """
    Compiles a pattern into a parser function
    "<int>   <int>" -> (int, int)
    "<int:left>   <int:right>" -> {"left": int, "right": int}
    """
    # wrap the compiled pattern to pass the in the inital context and
    # unwrap the output to only return the completed context
    matcher, _ = compile_pattern(pattern, 0)
    return lambda input: matcher(input, 0, None)[0]


def input():
    for line in file_input():
        yield line.strip()
