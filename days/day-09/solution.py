from collections import *
from itertools import *
from functools import *

from aocd.models import Puzzle
import numpy as np
import parse
from aocp import *

from collections import *
from itertools import *
from functools import *

from aocd.models import Puzzle
import numpy as np
import parse
from aocp import *

example: str = """2199943210
3987894921
9856789892
8767896789
9899965678"""
example_sol_a: int = 15
example_sol_b: int = 1134


def parse_input(raw_data: str):
    return np.array(ListParser(ListParser(int)).parse(raw_data))


def get_diff_map(data: np.ndarray) -> np.ndarray:
    up = np.concatenate(
        (np.ones((1, data.shape[1]), dtype=int) * 10, data[:-1, :] - data[1:, :]),
        axis=0,
    )
    left = np.concatenate(
        (np.ones((data.shape[0], 1), dtype=int) * 10, data[:, :-1] - data[:, 1:]),
        axis=1,
    )
    down = np.concatenate(
        (data[1:, :] - data[:-1, :], np.ones((1, data.shape[1]), dtype=int) * 10),
        axis=0,
    )
    right = np.concatenate(
        (data[:, 1:] - data[:, :-1], np.ones((data.shape[0], 1), dtype=int) * 10),
        axis=1,
    )
    return np.array([up, right, down, left])


def solve_a(data) -> int:
    diff_map = get_diff_map(data)
    is_low_point = np.all(diff_map > 0, axis=0)
    return np.sum(data[is_low_point] + 1)


def flows_towards(diff_map, pos):
    dir = np.argmin(diff_map[:, pos[0], pos[1]])
    if dir == 0:
        return (pos[0] - 1, pos[1])
    elif dir == 1:
        return (pos[0], pos[1] + 1)
    elif dir == 2:
        return (pos[0] + 1, pos[1])
    elif dir == 3:
        return (pos[0], pos[1] - 1)


def get_flows_map(data: np.ndarray) -> np.ndarray:
    diff_map = get_diff_map(data)
    is_low_point = np.all(diff_map > 0, axis=0)
    points = np.argwhere(data >= 0).tolist()
    lowpoints = np.argwhere(is_low_point).tolist()
    highpoints = np.argwhere(data == 9).tolist()
    flowpoints = [
        point for point in points if point not in lowpoints and point not in highpoints
    ]
    flows_mapping = {
        tuple(pos): flows_towards(diff_map, tuple(pos)) for pos in flowpoints
    }
    return flows_mapping


def get_lowpoint_mapping(flows_mapping: dict) -> dict:
    lowpoint_mapping = {}
    for pos, flow in flows_mapping.items():
        point = flow
        while True:
            if point not in flows_mapping:
                lowpoint_mapping[pos] = point
                break
            point = flows_mapping[point]
    return lowpoint_mapping


def solve_b(data) -> int:
    flows_mapping = get_flows_map(data)
    lowpoint_mapping = get_lowpoint_mapping(flows_mapping)
    _, counts = np.unique(
        np.array(list(lowpoint_mapping.values())), axis=0, return_counts=True
    )
    sizes = counts + 1
    return np.prod(sizes[sizes.argsort()[-3:]])


if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=9)
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
