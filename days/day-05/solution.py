from aocd.models import Puzzle
import numpy as np
import parse


def parse_input(data):
    vent_format = parse.compile("{} -> {}")
    coord_format = parse.compile("{:d},{:d}")
    return np.array(
        [
            [list(coord_format.parse(coord)) for coord in vent_format.parse(vent)]
            for vent in data.splitlines()
        ],
        dtype=int,
    )


def filter_straight_vents(vents):
    horizontal = vents[:, 0, 0] == vents[:, 1, 0]
    vertical = vents[:, 0, 1] == vents[:, 1, 1]
    return vents[horizontal | vertical]


def vent_length(vent):
    return max(abs(vent[0, 0] - vent[1, 0]), abs(vent[0, 1] - vent[1, 1])) + 1


def vent_points(vent):
    return np.round(np.linspace(vent[0], vent[1], vent_length(vent))).astype(int)


def count_overlapping_points(vents):
    all_points = np.concatenate([vent_points(vent) for vent in vents])
    points, count = np.unique(all_points, return_counts=True, axis=0)
    return sum(count >= 2)


def solve_a(vents):
    straight_vents = filter_straight_vents(vents)
    return count_overlapping_points(straight_vents)


def solve_b(vents):
    return count_overlapping_points(vents)


if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=5)
    data = parse_input(puzzle.input_data)

    example = """"""
    example_sol_a: int = None
    example_sol_b: int = None
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
