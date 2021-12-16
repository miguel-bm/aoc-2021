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
    return "".join([bin(int(c, 16))[2:].zfill(4) for c in raw_data])


Packet = namedtuple("Packet", ["version", "type", "length", "packets", "literal"])


def parse_packet(data: str, offset: int = 0):
    string = data[offset:]
    version = int(string[:3], 2)
    packet_type = int(string[3:6], 2)
    packets = []
    if packet_type == 4:
        i = 6
        literals = []
        is_last = False
        while not is_last:
            group = string[i : i + 5]
            literals.append(group[1:])
            is_last = True if group[0] == "0" else False
            i += 5
        literal = int("".join(literals), 2)
        length = len(literals) * 5 + 6
        return Packet(version, packet_type, length, packets, literal)
    else:
        total_length, num_packets, start = (
            (0, int(string[7:18], 2), 18)
            if int(string[6:7], 2)
            else (int(string[7:22], 2), 0, 22)
        )
        parsed_len = 0
        while len(packets) < num_packets or parsed_len < total_length:
            packet = parse_packet(string, start + parsed_len)
            packets.append(packet)
            parsed_len += packet.length
        return Packet(version, packet_type, start + parsed_len, packets, 0)


def sum_versions(packet: Packet):
    return packet.version + sum(sum_versions(p) for p in packet.packets)


def solve_a(data) -> int:
    return sum_versions(parse_packet(data))


def operate_packet(packet: Packet):
    if packet.type == 4:
        return packet.literal
    elif packet.type == 0:
        return sum([operate_packet(p) for p in packet.packets])
    elif packet.type == 1:
        return np.prod([operate_packet(p) for p in packet.packets])
    elif packet.type == 2:
        return min([operate_packet(p) for p in packet.packets])
    elif packet.type == 3:
        return max([operate_packet(p) for p in packet.packets])
    elif packet.type == 5:
        return operate_packet(packet.packets[0]) > operate_packet(packet.packets[1])
    elif packet.type == 6:
        return operate_packet(packet.packets[0]) < operate_packet(packet.packets[1])
    elif packet.type == 7:
        return operate_packet(packet.packets[0]) == operate_packet(packet.packets[1])


def solve_b(data) -> int:
    return operate_packet(parse_packet(data))


if __name__ == "__main__":
    puzzle = Puzzle(year=2021, day=16)
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
