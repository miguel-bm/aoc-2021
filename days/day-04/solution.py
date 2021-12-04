from pathlib import Path
import numpy as np


def parse_board(board: str):
    return [[int(num) for num in line.split()] for line in board.split("\n")]


def read_input(filename):
    with Path(filename).open() as f:
        lines = f.readlines()
        bingo_numbers = list(map(int, lines[0].split(",")))
        boards = map(parse_board, "".join(lines[1:]).strip("\n").split("\n\n"))
        return bingo_numbers, np.array(list(boards))


def find_bingo_winners(bingo_record):
    wins_by_rows = np.any(np.all(bingo_record, axis=2), axis=1)
    wins_by_cols = np.any(np.all(bingo_record, axis=1), axis=1)
    return wins_by_rows | wins_by_cols


def find_first_winner(bingo_numbers, bingo_boards):
    bingo_record = np.zeros_like(bingo_boards, dtype=bool)
    for number in bingo_numbers:
        bingo_record += bingo_boards == number
        if any(winners := find_bingo_winners(bingo_record)):
            return number, bingo_boards[winners][0], bingo_record[winners][0]


def find_last_winner(bingo_numbers, bingo_boards):
    bingo_record = np.zeros_like(bingo_boards, dtype=bool)
    for number in bingo_numbers:
        bingo_record += bingo_boards == number
        if all(winners := find_bingo_winners(bingo_record)):
            return number, bingo_boards[losers][0], bingo_record[losers][0]
        losers = ~winners


def compute_solution(number, board, board_record):
    return np.sum(board[board_record == 0]) * number


if __name__ == "__main__":
    bingo_numbers, bingo_boards = read_input("days/day-04/input.txt")
    print(compute_solution(*find_first_winner(bingo_numbers, bingo_boards)))
    print(compute_solution(*find_last_winner(bingo_numbers, bingo_boards)))
