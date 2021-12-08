from aocd.models import Puzzle
import numpy as np
from collections import *
import parse

example = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""
example_sol_a: int = 26
example_sol_b: int = 61229


def parse_input(raw_data: str):
    return [
        (
            tuple(set(p) for p in line.strip().split("|")[0].strip().split(" ")),
            tuple(set(p) for p in line.strip().split("|")[1].strip().split(" ")),
        )
        for line in raw_data.strip().split("\n")
    ]


def solve_a(data: list[tuple[set, set]]) -> int:
    return sum(len([e for e in outs if len(e) in (2, 3, 4, 7)]) for _, outs in data)


num_to_segments = {
    0: set("abcefg"),
    1: set("cf"),
    2: set("acdeg"),
    3: set("acdfg"),
    4: set("bcdf"),
    5: set("abdfg"),
    6: set("abdefg"),
    7: set("acf"),
    8: set("abcdefg"),
    9: set("abcdfg"),
}
num_to_num_segments = {i: len(s) for i, s in num_to_segments.items()}
len_to_digits = defaultdict(set)
for num, segments in num_to_segments.items():
    len_to_digits[len(segments)].add(num)


def possible_translations(pattern: set, translations: dict[str, int]) -> set:
    return set(
        num
        for num in len_to_digits[len(pattern)] - set(translations.values())
        if all(
            (
                len(pattern & set(other_pattern))
                == len(num_to_segments[num] & num_to_segments[other_num])
                for other_pattern, other_num in translations.items()
            )
        )
    )


set_to_str = lambda s: "".join(sorted(s))


def find_translations(patterns: tuple[set]) -> dict[str, int]:
    translations = {}
    while len(translations) < 10:
        for pattern in (p for p in patterns if set_to_str(p) not in translations):
            if len(candidates := possible_translations(pattern, translations)) == 1:
                translations[set_to_str(pattern)] = candidates.pop()
    return translations


def translate_line(patterns: tuple[set], switched_outputs: str) -> str:
    translations = find_translations(patterns)
    return int("".join(str(translations[set_to_str(p)]) for p in switched_outputs))


def solve_b(data) -> int:
    return sum(
        translate_line(patterns, switched_outputs)
        for patterns, switched_outputs in data
    )


if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=8)
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
