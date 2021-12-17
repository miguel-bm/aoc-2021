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
    return list(parse.parse("target area: x={:d}..{:d}, y={:d}..{:d}", raw_data))


def solve_a(data) -> int:
    _, _, y_min, _ = data
    return int(abs(y_min) * (abs(y_min) - 1) / 2)


def next_step(p, v):
    return (p[0] + v[0], p[1] + v[1]), (max(v[0] - 1, 0), v[1] - 1)


def is_in_target(p, target):
    return target[0] <= p[0] <= target[1] and target[2] <= p[1] <= target[3]


def does_trajectory_pass(velocity: tuple, target: tuple):
    position = (0, 0)
    while position[1] >= target[2] and position[0] <= target[1]:
        position, velocity = next_step(position, velocity)
        if is_in_target(position, target):
            return True
    return False


def solve_b(data) -> int:
    x_min, x_max, y_min, y_max = data
    return sum(
        does_trajectory_pass(v, (x_min, x_max, y_min, y_max))
        for v in product(range(int(x_min ** 0.5), x_max + 1), range(y_min, -y_min))
    )


if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=17)
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
