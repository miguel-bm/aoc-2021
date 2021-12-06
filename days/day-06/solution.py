from aocd.models import Puzzle
import numpy as np
from collections import *
import parse

example = "3,4,3,1,2"
example_sol_a: int = 5934
example_sol_b: int = 26984457539


def parse_input(raw_data: str):
    return [int(num) for num in raw_data.strip().split(",")]


def advance_day(fish_ages: Counter) -> Counter:
    new_fish_ages = Counter()
    for age, count in fish_ages.items():
        if age == 0:
            new_fish_ages[8] += count
            new_fish_ages[6] += count
        else:
            new_fish_ages[age - 1] += count
    return new_fish_ages


def fish_after_n_days(data: list[int], num_days: int) -> int:
    fish_ages = Counter(data)
    for _ in range(num_days):
        fish_ages = advance_day(fish_ages)
    return sum(fish_ages.values())


def solve_a(data: list[int]) -> int:
    return fish_after_n_days(data, 80)


def solve_b(data: list[int]) -> int:
    return fish_after_n_days(data, 256)


if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=6)
    raw_data = puzzle.input_data
    data = parse_input(raw_data)

    if example:
        example = parse_input(example)

    # Part 1
    if example:
        assert example_sol_a == solve_a(example)
    solution_a = solve_a(data)
    print(solution_a)
    puzzle.answer_a = solution_a

    # Part 2
    if example:
        assert example_sol_b == solve_b(example)
    solution_b = solve_b(data)
    print(solution_b)
    puzzle.answer_b = solution_b
