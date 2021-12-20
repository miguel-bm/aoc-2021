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
    return TupleParser(
        (
            TupleParser(
                ChainParser([ReplaceTransform({"#": "1", ".": "0"}), IntParser()])
            ),
            TupleParser(
                TupleParser(
                    ChainParser([ReplaceTransform({"#": "1", ".": "0"}), IntParser()])
                )
            ),
        )
    ).parse(raw_data)


def enhance_image(image: np.ndarray, algorithm: tuple) -> np.ndarray:
    new_img = np.zeros((image.shape[0] + 2, image.shape[1] + 2), dtype=int)
    image = np.pad(image, 2, "edge")
    for i, j in np.ndindex(new_img.shape):
        number = int("".join(image[i : i + 3, j : j + 3].flatten().astype(str)), 2)
        new_img[i, j] = algorithm[number]
    return new_img


def solve_a(data, num: int = 2) -> int:
    algorithm, image = data
    image = np.pad(np.array(image), 1, "constant")
    for _ in range(num):
        image = enhance_image(image, algorithm)
    return image.sum()


def solve_b(data) -> int:
    return solve_a(data, num=50)


if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=20)
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
