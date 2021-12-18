from __future__ import annotations
from collections import *
from itertools import *
from functools import *
import json
import math
from typing import Union


from aocd.models import Puzzle
import numpy as np
import parse
from aocp import *

example: str = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"""
example_sol_a: int = 4140
example_sol_b: int = 3993


def parse_input(raw_data: str):
    return [json.loads(line) for line in raw_data.splitlines()]


class SFNumber:
    def __init__(self, data):
        left, right = data
        self.left = left if isinstance(left, int) else SFNumber(left)
        self.right = right if isinstance(right, int) else SFNumber(right)

    def __repr__(self):
        return f"({self.left},{self.right})"

    def __iter__(self):
        return iter([self.left, self.right])

    @classmethod
    def _add(cls, number: Union[SFNumber, int], addition: int, to_left: bool):
        if isinstance(number, int):
            return number + (addition or 0)
        if to_left:
            return SFNumber((cls._add(number.left, addition, to_left), number.right))
        else:
            return SFNumber((number.left, cls._add(number.right, addition, to_left)))

    @classmethod
    def _explode_sfnumber(
        cls, number: Union[SFNumber, int], nesting=0
    ) -> tuple[Union[SFNumber, int], Union[SFNumber, int], Union[SFNumber, int], bool]:
        if isinstance(number, int):
            return number, None, None, False
        if nesting == 4:
            return 0, number.left, number.right, True
        sub, left, right, explodes = cls._explode_sfnumber(number.left, nesting + 1)
        if explodes:
            return (
                SFNumber((sub, cls._add(number.right, right, True))),
                left,
                None,
                True,
            )
        sub, left, right, explodes = cls._explode_sfnumber(number.right, nesting + 1)
        if explodes:
            return (
                SFNumber((cls._add(number.left, left, False), sub)),
                None,
                right,
                True,
            )
        return number, None, None, False

    @classmethod
    def _split_sfnumber(
        cls, number: Union[SFNumber, int]
    ) -> tuple[Union[SFNumber, int], bool]:
        if isinstance(number, int):
            if number >= 10:
                return SFNumber((math.floor(number / 2), math.ceil(number / 2))), True
            return number, False
        left, splits = cls._split_sfnumber(number.left)
        if splits:
            return SFNumber((left, number.right)), True
        right, splits = cls._split_sfnumber(number.right)
        if splits:
            return SFNumber((number.left, right)), True
        return number, False

    @classmethod
    def _magnitude(cls, number: Union[SFNumber, int]):
        if isinstance(number, int):
            return number
        return 3 * cls._magnitude(number.left) + 2 * cls._magnitude(number.right)

    def explode(self):
        number, _, _, explodes = self._explode_sfnumber(self)
        self.left = number.left
        self.right = number.right
        return explodes

    def split(self):
        number, splits = self._split_sfnumber(self)
        self.left = number.left
        self.right = number.right
        return splits

    def reduce(self):
        while True:
            if self.explode():
                continue
            if self.split():
                continue
            break
        return self

    def magnitude(self):
        return self._magnitude(self)

    def __add__(self, other: SFNumber):
        return SFNumber((self, other)).reduce()


def solve_a(data) -> int:
    result = reduce(SFNumber.__add__, [SFNumber(line) for line in data])
    return result.magnitude()


def solve_b(data) -> int:
    numbers = [SFNumber(line) for line in data]
    results = [(a + b).magnitude() for a, b in product(numbers, numbers)]
    return max(results)


if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=18)
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
