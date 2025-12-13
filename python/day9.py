from collections import defaultdict
import heapq
import sys
from pathlib import Path
from enum import StrEnum
from typing import Generator


class Tile(StrEnum):
    RED = '#'
    GREEN = 'X'
    PLAIN = '.'

def max_areas(tiles: list[tuple[int, int]]) -> list[tuple[int, int, int]]:
    max_heap: list[tuple[int, int, int]] = []
    for i in range(len(tiles)):
        r1, c1 = tiles[i]
        for j in range(i + 1, len(tiles)):
            r2, c2 = tiles[j]
            area = abs(r1 - r2 + 1) * abs(c1 - c2 + 1)
            heapq.heappush(max_heap, (-area, i, j))
    return max_heap


def part1(tiles: list[tuple[int, int]]) -> int:
    return -max_areas(tiles)[0][0]


def create_boundary(red_tiles: list[tuple[int, int]]) -> defaultdict[int, set[int]]:
    boundary: defaultdict[int, set[int]] = defaultdict(set)
    for ((r1, c1), (r2, c2)) in zip(red_tiles, red_tiles[1:]):
        if r1 == r2:
            dc = +1 if c2 > c1 else -1
            while c1 != c2:
                boundary[r1].add(c1)
                c1 += dc
        else:
            dr = +1 if r2 > r1 else -1
            while r1 != r2:
                boundary[r1].add(c1)
                r1 += dr
    return boundary


def print_boundary(boundary: defaultdict[int, set[int]], red_tiles) -> None:
    max_r = max(r for (r, _) in red_tiles)
    max_c = max(c for (_, c) in red_tiles)
    grid = [[Tile.PLAIN for _ in range(max_c + 1)] for _ in range(max_r + 1)]
    for r in boundary:
        for c in boundary[r]:
            grid[r][c] = Tile.GREEN
    for row in grid:
        print(" ".join(str(elem) for elem in row))


def is_valid_point():
    pass
    

def create_area_for_point_pairs(points_i: tuple[int, int], points_j: tuple[int, int]):
    r1, c1 = points_i
    r2, c2 = points_j
    for r in range(min(r1, r2), max(r1, r2) + 1):
        for c in range(min(c1, c2), max(c1, c2) + 1):
            yield (r, c)


def is_valid_area(boundary: defaultdict[int, set[int]], points_i: tuple[int, int], points_j: tuple[int, int]) -> bool:
    N, E, S, W = (-1, 0), (0, 1), (1, 0), (0, -1)
    for point in create_area_for_point_pairs(points_i, points_j):
        pass
    print("hello")



def part2(red_tiles: list[tuple[int, int]]):
    boundary = create_boundary(red_tiles)
    # print_boundary(boundary, red_tiles)
    max_areas_heap = max_areas(red_tiles)
    while max_areas_heap:
        max_area, i, j = heapq.heappop(max_areas_heap)
        print(i, j)
        if is_valid_area(boundary, red_tiles[i], red_tiles[j]):
            pass


def parse(data: str) -> list[tuple[int, int]]:
    split_data = data.split("\n")
    total_data = split_data + [split_data[0]]
    return [tuple(map(int, row.split(","))) for row in total_data]


if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else f"../data/{Path(__file__).stem}.txt"
    with open(filename) as f:
        inp = f.read()
    inp_data = parse(inp)

    print("part1=" + str(part1(inp_data)))
    print("part2=" + str(part2(inp_data)))
