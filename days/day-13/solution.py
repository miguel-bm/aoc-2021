from collections import *
from itertools import *
from functools import *

from aocd.models import Puzzle
import numpy as np
import parse
from aocp import *

example = """"""
example_sol_a: int = 17


def parse_input(raw_data: str):
    return TupleParser(
        (
            SetParser(TupleParser(int)),
            ListParser(
                TupleParser(
                    (CustomTransform(lambda x: x[-1]), IntParser()), splitter="="
                )
            ),
        )
    ).parse(raw_data)


def execute_fold(
    dots: list[tuple[int, int]], fold: tuple[str, int]
) -> list[tuple[int, int]]:
    dir, pos = fold
    if dir == "x":
        return {((x, y) if x < pos else (pos - (x - pos), y)) for x, y in dots}
    elif dir == "y":
        return {((x, y) if y < pos else (x, pos - (y - pos))) for x, y in dots}


def solve_a(data) -> int:
    dots, folds = data
    return len(execute_fold(dots, folds[0]))


def solve_b(data) -> int:
    dots, folds = data
    for fold in folds:
        dots = execute_fold(dots, fold)
    dims = (max(x for x, _ in dots) + 1, max(y for _, y in dots) + 1)
    panel = np.zeros(dims, dtype=int)
    for dot in dots:
        panel[dot] = 1
    for line in panel.transpose():
        for char in line:
            print(("█" if char else " "), end="")
        print()


if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=13)
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
    solution_b = solve_b(data)
