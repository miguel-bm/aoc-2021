from collections import *
from itertools import *
from functools import *

from aocd.models import Puzzle
import numpy as np
import parse
from aocp import *

example: str = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""
example_sol_a: int = 40
example_sol_b: int = 315


puzzle = Puzzle(year=2021, day=15)
raw_data = puzzle.input_data


def parse_input(raw_data: str):
    return np.array(ListParser(ListParser(IntParser()))(raw_data))


def map_to_graph(map: np.ndarray):
    graph = defaultdict(list)
    for i, j in zip(*np.where(map)):
        for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
            if 0 <= i + dx < map.shape[0] and 0 <= j + dy < map.shape[1]:
                graph[(i, j)].append(((i + dx, j + dy), map[i + dx, j + dy]))
    return graph


def dijkstra_min_cost(graph: dict, start: int, end: int):
    distances = {start: 0}
    heap = deque([start])
    while heap:
        node = heap.popleft()
        for adj_node, adj_cost in graph[node]:
            distance = adj_cost + distances[node]
            if adj_node not in distances or distance < distances[adj_node]:
                distances[adj_node] = distance
                heap.append(adj_node)
    return distances[end]


def solve_a(data) -> int:
    return dijkstra_min_cost(
        map_to_graph(data), (0, 0), (data.shape[0] - 1, data.shape[1] - 1)
    )


def solve_b(data) -> int:
    map = (
        np.arange(5).reshape(5, 1, 1, 1)
        + np.arange(5).reshape(1, 1, 5, 1)
        + np.expand_dims(data, axis=(0, 2))
    )
    map = (np.vstack(np.vstack(map).transpose(1, 2, 0)).transpose() - 1) % 9 + 1
    return solve_a(map)


if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=15)
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
