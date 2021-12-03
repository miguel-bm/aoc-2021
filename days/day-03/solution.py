from pathlib import Path
import numpy as np


def read_input(filename):
    with Path(filename).open() as f:
        return [[int(b) for b in line.strip()] for line in f.readlines()]


def binary_array_to_int(arr: np.array) -> int:
    return int("".join(map(str, map(int, arr))), 2)


def sift_most_common(arr: np.array, position: int, val: bool) -> np.array:
    return arr[arr[:, position] == ((np.mean(arr[:, position]) >= 0.5) == val)]


def find_rate(arr: np.array, val: bool) -> int:
    candidates = arr.copy()
    for position in range(arr.shape[1]):
        candidates = sift_most_common(candidates, position, val)
        if len(candidates) == 1:
            return binary_array_to_int(candidates[0])


if __name__ == "__main__":
    diagnostic = np.array(read_input("days/day-03/input.txt"))

    # Part 1
    gamma = binary_array_to_int(np.round(diagnostic.mean(axis=0)))
    epsilon = binary_array_to_int(1 - np.round(diagnostic.mean(axis=0)))
    print(gamma * epsilon)

    # Part 2
    oxigen_rate = find_rate(diagnostic, True)
    co2_rate = find_rate(diagnostic, False)
    print(oxigen_rate * co2_rate)
