#!/usr/bin/env python3

from pathlib import Path
import argparse


def copy_with_substitutions(source_path: Path, target_path: Path, substitutions: dict):
    with open(source_path, "r") as source_file:
        with open(target_path, "w") as target_file:
            target = source_file.read()
            for key, value in substitutions.items():
                target = target.replace(key, value)
            target_file.write(target)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("day", type=int, help="The day of the challenge")
    args = parser.parse_args()

    day = args.day
    if day < 1 or day > 25:
        raise ValueError(f"Day must be between 1 and 25, not {day}")
    substitutions = {"__DAY__": str(day)}

    print(f"Creating folder and files for day {day}")

    template_path = Path(__file__).parent / "template"
    solution_template_path = template_path / "solution.py"
    dev_template_path = template_path / "dev.ipynb"

    day_path = Path(__file__).parent.parent / f"days/day-{day:02}"
    if day_path.exists():
        raise ValueError(f"Day {day} already exists")
    day_path.mkdir(parents=True, exist_ok=False)
    solution_path = day_path / "solution.py"
    dev_path = day_path / "dev.ipynb"

    copy_with_substitutions(solution_template_path, solution_path, substitutions)
    copy_with_substitutions(dev_template_path, dev_path, substitutions)

    print("Done")
