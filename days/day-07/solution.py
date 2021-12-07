from aocd.models import Puzzle
import numpy as np

example = "16,1,2,0,4,2,7,1,2,14"
example_sol_a: int = 37
example_sol_b: int = 168


def parse_input(raw_data: str):
    return np.array([int(num) for num in raw_data.strip().split(",")])


def fuel_a(positions, alignment_position):
    distances = np.abs(positions - alignment_position)
    return int(distances.sum())


def solve_a(data):
    return fuel_a(data, np.median(data))


def fuel_b(positions, alignment_position):
    distances = np.abs(positions - alignment_position)
    return int(np.sum(distances * (distances + 1) / 2))


def solve_b(data) -> int:
    return min(fuel_b(data, pos) for pos in range(data.size))


if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=7)
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
