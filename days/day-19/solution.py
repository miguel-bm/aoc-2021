from __future__ import annotations
from collections import *
from itertools import *

from aocd.models import Puzzle
import numpy as np
from aocp import *


example: str = """--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14"""
example_sol_a: int = 79
example_sol_b: int = 3621


puzzle = Puzzle(year=2021, day=19)
raw_data = puzzle.input_data


def parse_input(raw_data: str):
    return dict(
        ListParser(TupleParser((IntParser(), SetParser(TupleParser(int))))).parse(
            raw_data
        )
    )


def rot_matrix_line_gen():
    for i, v in product((0, 1, 2), (1, -1)):
        vec = np.zeros(3)
        vec[i] = v
        yield vec


def rot_matrix_gen():
    for v1, v2, v3 in product(rot_matrix_line_gen(), repeat=3):
        if np.linalg.det(R := np.array([v1, v2, v3])) == 1:
            yield R


class Scanner:
    def __init__(self, id: int, probe_positions: set[tuple[int, int, int]]):
        self.id = id
        self.probe_positions = {tuple(pos) for pos in probe_positions}

    def rotation(self, R):
        return Scanner(
            self.id, [np.dot(R, np.array(p)).astype(int) for p in self.probe_positions]
        )

    def rotate(self, R) -> Scanner:
        self = self.rotation(R)

    def iter_rotations(self) -> Iterator[tuple[np.ndarray, Scanner]]:
        for R in rot_matrix_gen():
            yield R, self.rotation(R)

    def compare_positions(
        self, other: Scanner
    ) -> tuple[np.ndarray, tuple[int, int, int]]:
        for R, scanner in other.iter_rotations():
            difs = []
            for pos_1 in self.probe_positions:
                for pos_2 in scanner.probe_positions:
                    dif = np.array(pos_1) - np.array(pos_2)
                    difs.append(tuple(dif))
            count_difs = Counter(difs)
            if max(count_difs.values()) >= 12:
                return R, count_difs.most_common(1)[0][0]
        return None, None

    def add_probes(self, probes):
        self.probe_positions.update(probes)


def position_probes_and_scanners(
    data: dict[int, set[tuple[int, int, int]]], reference: int = 0
) -> tuple[set[tuple[int, int, int]], dict[int, tuple[int, int, int]]]:
    scanners = {id: Scanner(id, pos) for id, pos in data.items()}
    reference_scanner = scanners[reference]
    scanner_positions = {reference: (0, 0, 0)}
    while len(scanner_positions) < len(scanners):
        for id_can, candidate_scanner in scanners.items():
            if reference == id_can or id_can in scanner_positions:
                continue
            R, dif = reference_scanner.compare_positions(candidate_scanner)
            if dif is not None:
                scanner_positions[id_can] = dif
                shifted_positions = [
                    tuple(np.array(pos) + np.array(dif))
                    for pos in candidate_scanner.rotation(R).probe_positions
                ]
                reference_scanner.add_probes(shifted_positions)
    return reference_scanner.probe_positions, scanner_positions


def solve_a(data: dict) -> int:
    probes, _ = position_probes_and_scanners(data)
    return len(probes)


def manhattan_distance(pos1, pos2):
    return sum(abs(pos1[i] - pos2[i]) for i in range(3))


def solve_b(data) -> int:
    _, scanner_positions = position_probes_and_scanners(data)
    max_distance = max(
        manhattan_distance(pos1, pos2)
        for pos1, pos2 in product(scanner_positions.values(), repeat=2)
    )
    return max_distance


if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=19)
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
