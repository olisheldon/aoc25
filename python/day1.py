import sys
from pathlib import Path
from typing import Type
from enum import StrEnum, auto


NUMBER_OF_COMBINATIONS = 100
INITIAL_COMBINATION = 50
SENTINEL_COMBINATION = 0

class RotationDirection(StrEnum):
    L = "L"
    R = "R"

    @staticmethod
    def get_rot_direction(direction: "RotationDirection") -> int:
        match direction:
            case RotationDirection.L:
                return -1
            case RotationDirection.R:
                return 1
            case _:
                raise RuntimeError()
    

def rot(direction: RotationDirection, distance: int, combination: int) -> tuple[int, int]:
    init_combination = combination
    distance *= RotationDirection.get_rot_direction(direction)
    num_of_clicks = abs((init_combination + distance) // 100)
    combination += distance
    return (combination % 100), num_of_clicks


def part1(instructions: list[tuple["RotationDirection", int]]):
    res = 0
    combination = INITIAL_COMBINATION
    for rot_dir, dist in instructions:
        combination, _ = rot(rot_dir, dist, combination)
        if combination == SENTINEL_COMBINATION:
            res += 1
    return res


def part2(instructions: list[tuple["RotationDirection", int]]):
    res = 0
    combination = INITIAL_COMBINATION
    for instruction in instructions:
        rot_dir, dist = instruction
        combination, num_of_clicks = rot(rot_dir, dist, combination)
        print(f"{combination=}, {instruction=}, {num_of_clicks=}")
        res += num_of_clicks > 0
    return res


def parse(data: str) -> list[tuple["RotationDirection", int]]:
    res = []
    for row in data.split("\n"):
        rot, dist = RotationDirection(row[0]), int(row[1:])
        res.append((rot, dist))
    return res


if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else f"../data/{Path(__file__).stem}.txt"
    with open(filename) as f:
        inp = f.read()
    inp_data = parse(inp)

    print("part1=" + str(part1(inp_data)))
    print("part2=" + str(part2(inp_data)))
