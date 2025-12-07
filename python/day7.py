from collections import deque
import sys
from pathlib import Path
from enum import StrEnum


class Tachyon(StrEnum):
    EMPTY = '.'
    START = 'S'
    SPLITTER = '^'
    BEAM = '|'


def part1(grid: list[list[Tachyon]]):
    ROWS, COLS = len(grid), len(grid[0])
    r, c = 0, grid[0].index(Tachyon.START)
    q = deque([(r, c)])

    visited = set()
    split_count = 0
    while q:
        for _ in range(len(q)):
            r, c = q.popleft()
            if (
                r not in range(ROWS) or
                c not in range(COLS) or
                (r, c) in visited
                ):
                continue
            visited.add((r, c))
            match grid[r][c]:
                case Tachyon.EMPTY | Tachyon.START:
                    q.append((r + 1, c))
                case Tachyon.SPLITTER:
                    split_count += 1
                    q.append((r, c - 1))
                    q.append((r, c + 1))
                case _:
                    raise RuntimeError(f"{grid[r][c]=} not valid")
    return split_count


def part2():
    pass


def parse(data: str):
    grid = [list(row) for row in data.split("\n")]
    return [[Tachyon(elem) for elem in row] for row in grid]


if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else f"../data/{Path(__file__).stem}.txt"
    with open(filename) as f:
        inp = f.read()
    inp_data = parse(inp)

    print("part1=" + str(part1(inp_data)))
    print("part2=" + str(part2(inp_data)))
