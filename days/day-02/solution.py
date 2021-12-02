from pathlib import Path


def read_input(filename):
    with Path(filename).open() as f:
        return [(line.split()[0], int(line.split()[1])) for line in f.readlines()]

def move(command_type, value, current_position):
    horizontal_position, depth, aim = current_position
    if command_type == 'up':
        aim = aim - value
    elif command_type == 'down':
        aim = aim + value
    elif command_type == 'forward':
        horizontal_position = horizontal_position + value
        depth = depth + aim * value

    return (horizontal_position, depth, aim)

if __name__ == "__main__":
    commands = read_input("days/day-02/input.txt")

    horizontal_position = sum(
        value for command_type, value in commands if command_type == "forward"
    )

    vertical_position = sum(
        - value for command_type, value in commands if command_type == "up"
    ) + sum(
        value for command_type, value in commands if command_type == "down"
    )

    print(horizontal_position * vertical_position)

    initial_position = (0, 0, 0)
    current_position = initial_position
    for command_type, value in commands:
        current_position = move(command_type, value, current_position)
    print(current_position[0] * current_position[1])
