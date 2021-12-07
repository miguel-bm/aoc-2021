from aocd.models import Puzzle
import numpy as np
from collections import *
import parse

example = """"""
example_sol_a: int = None
example_sol_b: int = None


def parse_input(raw_data: str):
    return None


def solve_a(data) -> int:
    return None


def solve_b(data) -> int:
    return None


if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=__DAY__)
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
