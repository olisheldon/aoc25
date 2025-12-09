import sys
from pathlib import Path
from enum import StrEnum


class Tile(StrEnum):
    RED = '#'
    PLAIN = '.'


def part1(tiles: list[tuple[int, int]]) -> int:
    res = 0
    for i in range(len(tiles)):
        r1, c1 = tiles[i]
        for j in range(i + 1, len(tiles)):
            r2, c2 = tiles[j]
            res = max(res, abs(r1 - r2 + 1) * abs(c1 - c2 + 1))
    return res


def part2():
    pass


def parse(data: str) -> list[tuple[int, int]]:
    return [tuple(map(int, row.split(","))) for row in data.split("\n")]


if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else f"../data/{Path(__file__).stem}.txt"
    with open(filename) as f:
        inp = f.read()
    inp_data = parse(inp)

    print("part1=" + str(part1(inp_data)))
    print("part2=" + str(part2(inp_data)))
