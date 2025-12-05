import sys
from pathlib import Path


def remove_rolls(grid: list[list[str]]):
    grid_copy = [row.copy() for row in grid]
    ROWS, COLS = len(grid), len(grid[0])
    NEIGHBOURS = (
        (1, 0),
        (-1, 0),
        (0, 1),
        (0, -1),
        (1, 1),
        (-1, 1),
        (1, -1),
        (-1, -1),
        )
    
    PAPER = '@'
    EMPTY = '.'
    res = 0
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] != PAPER:
                continue
            adj_paper_count = 0
            for dr, dc in NEIGHBOURS:
                nr, nc = r + dr, c + dc
                if (
                    nr not in range(ROWS) or
                    nc not in range(COLS) or
                    grid[nr][nc] != PAPER
                ):
                    continue
                adj_paper_count += 1
            if adj_paper_count < 4:
                res += 1
                grid_copy[r][c] = EMPTY
    return res, grid_copy


def part1(grid: list[list[str]]):
    return remove_rolls(grid)[0]


def part2(grid: list[list[str]]):
    res = 0
    while True:
        replacements, grid = remove_rolls(grid)
        res += replacements
        if replacements == 0:
            return res


def parse(data: str):
    return list(map(list,data.split("\n")))


if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else f"../data/{Path(__file__).stem}.txt"
    with open(filename) as f:
        inp = f.read()
    inp_data = parse(inp)

    print("part1=" + str(part1(inp_data)))
    print("part2=" + str(part2(inp_data)))
