from pathlib import Path


def read_input(filename):
    with Path(filename).open() as f:
        return [int(line) for line in f.readlines()]


if __name__ == "__main__":
    depths = read_input("days/day-01/input.txt")
    
    increases = sum(d2 > d1 for d1, d2 in zip(depths[:-1], depths[1:]))
    print(increases)

    sliding = [
        d1 + d2 + d3 for d1, d2, d3 in zip(depths[:-2], depths[1:-1], depths[2:])
    ]
    sliding_increases = sum(s2 > s1 for s1, s2 in zip(sliding[:-1], sliding[1:]))
    print(sliding_increases)
