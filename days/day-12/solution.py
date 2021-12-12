from collections import *
from itertools import *
from functools import *

from aocd.models import Puzzle
import numpy as np
import parse
from aocp import *

example = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""
example_sol_a: int = 10
example_sol_b: int = 36


def parse_input(raw_data: str):
    return ListParser(TupleParser(splitter="-")).parse(raw_data)


def graph_to_node_map(graph: list[tuple[str, str]]) -> dict[str, str]:
    node_map = defaultdict(list)
    for a, b in graph:
        if b != "start" and a != "end":
            node_map[a].append(b)
        if b != "end" and a != "start":
            node_map[b].append(a)
    return dict(node_map)


def find_paths(
    cave_map: dict[str, list[str]],
    path_validator: callable,
    path: list[tuple[str, str]] = None,
    start: str = "start",
    end: str = "end",
):
    path = path or [start]
    for next in cave_map[path[-1]]:
        if next == end:
            yield path + [end]
        elif path_validator(new_path := (path + [next])):
            yield from find_paths(cave_map, path_validator, new_path)


def is_valid_path_a(path: list[str]) -> bool:
    return max((v for k, v in Counter(path).items() if k.islower()), default=0) < 2


def is_valid_path_b(path: list[str]) -> bool:
    return np.prod([v for k, v in Counter(path).items() if k.islower()]) <= 2


def solve_a(data) -> int:
    return sum(1 for _ in find_paths(graph_to_node_map(data), is_valid_path_a))


def solve_b(data) -> int:
    return sum(1 for _ in find_paths(graph_to_node_map(data), is_valid_path_b))


if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=12)
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
