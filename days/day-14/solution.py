from collections import *
from itertools import *
from functools import *

from aocd.models import Puzzle
import numpy as np
import parse
from aocp import *

example: str = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""
example_sol_a: int = 1588
example_sol_b: int = 2188189693529


def parse_input(raw_data: str):
    template, rules = TupleParser((str, ListParser(TupleParser()))).parse(raw_data)
    rules = {k: v for k, v in rules}
    return template, rules


def pair_insertion(
    pairs: dict[tuple[str, str], int], rules: dict[tuple[str, str]], elements: Counter
) -> dict[tuple[str, str], int]:
    new_pairs = Counter()
    new_elements = elements.copy()
    for pair, count in pairs.items():
        if insertion := rules.get(pair):
            new_pairs[pair[0] + insertion] += count
            new_pairs[insertion + pair[1]] += count
            new_elements[insertion] += count
        else:
            new_pairs[pair] += count
    return new_pairs, new_elements


def solve_a(data, iterations=10) -> int:
    template, rules = data
    pairs = Counter(template[i : i + 2] for i in range(len(template) - 1))
    elements = Counter(template)
    for _ in range(iterations):
        pairs, elements = pair_insertion(pairs, rules, elements)
    return max(elements.values()) - min(elements.values())


def solve_b(data) -> int:
    return solve_a(data, iterations=40)


if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=14)
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
