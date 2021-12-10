from collections import *
from itertools import *
from functools import *

from aocd.models import Puzzle
import numpy as np
import parse
from aocp import *

example = """"""
example_sol_a: int = None
example_sol_b: int = None


def parse_input(raw_data: str):
    return ListParser(str).parse(raw_data)


legal_closings = {"(": ")", "[": "]", "{": "}", "<": ">"}


def find_first_corrupted_char(line: str) -> str:
    openings_stack = deque()
    for c in line:
        if c in legal_closings.keys():
            openings_stack.append(c)
        elif c in legal_closings.values():
            if openings_stack:
                if legal_closings[openings_stack.pop()] != c:
                    return c
            else:
                return c


def solve_a(data) -> int:
    points = {")": 3, "]": 57, "}": 1197, ">": 25137}
    return sum(points[c] for line in data if (c := find_first_corrupted_char(line)))


def get_score_b(completion_chars):
    points = {")": 1, "]": 2, "}": 3, ">": 4}
    return int("".join(str(points[c]) for c in completion_chars), 5)


def complete_line(line: str):
    openings_stack = []
    for c in line:
        if c in legal_closings.keys():
            openings_stack.append(c)
        elif c in legal_closings.values():
            if openings_stack:
                if legal_closings[openings_stack.pop()] != c:
                    return None
            else:
                return None
    return "".join(reversed([legal_closings[o] for o in openings_stack]))


def solve_b(data) -> int:
    scores = [get_score_b(e) for l in data if (e := complete_line(l))]
    return sorted(scores)[len(scores) // 2]


if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=10)
    raw_data = puzzle.input_data
    data = parse_input(raw_data)

    if example:
        example_data = parse_input(example)

    # Part 1
    if example:
        assert example_sol_a == solve_a(example_data)
    solution_a = solve_a(data)
    print(solution_a)
    puzzle.answer_a = solution_a

    # Part 2
    if example:
        assert example_sol_b == solve_b(example_data)
    solution_b = solve_b(data)
    print(solution_b)
    puzzle.answer_b = solution_b
