import sys
from pathlib import Path
from enum import StrEnum


class Tile(StrEnum):
    RED = '#'
    GREEN = 'X'
    PLAIN = '.'


def part1(tiles: list[tuple[int, int]]) -> int:
    res = 0
    for i in range(len(tiles)):
        r1, c1 = tiles[i]
        for j in range(i + 1, len(tiles)):
            r2, c2 = tiles[j]
            res = max(res, abs(r1 - r2 + 1) * abs(c1 - c2 + 1))
    return res


def create_grid(red_tiles: list[tuple[int, int]]) -> list[list[Tile]]:
    max_r = max(r for (r, _) in red_tiles)
    max_c = max(c for (_, c) in red_tiles)
    grid = [[Tile.PLAIN for _ in range(max_c + 1)] for _ in range(max_r + 1)]
    for ((r1, c1), (r2, c2)) in zip(red_tiles, red_tiles[1:]):
        if r1 == r2:
            dc = +1 if c2 > c1 else -1
            while c1 != c2:
                grid[r1][c1] = Tile.GREEN
                c1 += dc
        else:
            dr = +1 if r2 > r1 else -1
            while r1 != r2:
                grid[r1][c1] = Tile.GREEN
                r1 += dr
    return grid


def print_grid(grid: list[list[Tile]]) -> None:
    for row in grid:
        print("".join(str(elem) for elem in row))


def part2(red_tiles: list[tuple[int, int]]):
    grid = create_grid(red_tiles)
    print_grid(grid)


def parse(data: str) -> list[tuple[int, int]]:
    return [tuple(map(int, row.split(","))) for row in data.split("\n")]


if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else f"../data/{Path(__file__).stem}.txt"
    with open(filename) as f:
        inp = f.read()
    inp_data = parse(inp)

    print("part1=" + str(part1(inp_data)))
    print("part2=" + str(part2(inp_data)))
