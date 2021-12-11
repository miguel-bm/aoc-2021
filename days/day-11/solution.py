from collections import *
from itertools import *
from functools import *

from aocd.models import Puzzle
import numpy as np
import parse
from aocp import *

example = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""
example_sol_a: int = 1656
example_sol_b: int = 195


def parse_input(raw_data: str):
    return np.array(ListParser(ListParser(int)).parse(raw_data))


def simulate_step(current_energy: np.ndarray) -> np.ndarray:
    next_energy = current_energy + 1
    flashed = []
    while to_flash := [
        p for p in list(np.argwhere(next_energy > 9)) if tuple(p) not in flashed
    ]:
        flash = to_flash.pop()
        x_lo, x_hi = max(0, flash[0] - 1), min(flash[0] + 2, next_energy.shape[0])
        y_lo, y_hi = max(0, flash[1] - 1), min(flash[1] + 2, next_energy.shape[1])
        next_energy[x_lo:x_hi, y_lo:y_hi] += 1
        flashed.append(tuple(flash))
    for point in flashed:
        next_energy[point] = 0
    return next_energy


def solve_a(energy_levels: np.ndarray) -> int:
    num_flashes = 0
    for _ in range(100):
        energy_levels = simulate_step(energy_levels)
        num_flashes += (energy_levels == 0).sum()
    return num_flashes


def solve_b(energy_levels: np.ndarray) -> int:
    step = 0
    while True:
        energy_levels = simulate_step(energy_levels)
        step += 1
        if ((energy_levels == 0).sum() == 100) or step > 10000:
            break
    return step


if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=11)
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
