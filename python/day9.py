from collections import defaultdict
import heapq
import sys
from pathlib import Path
from enum import StrEnum
import bisect


class Tile(StrEnum):
    RED = '#'
    GREEN = 'X'
    PLAIN = '.'


def max_areas(tiles: list[tuple[int, int]]) -> list[tuple[int, tuple[int, int], tuple[int, int]]]:
    max_heap: list[tuple[int, tuple[int, int], tuple[int, int]]] = []
    for i in range(len(tiles)):
        r1, c1 = tiles[i]
        for j in range(i + 1, len(tiles)):
            r2, c2 = tiles[j]
            area = abs(r1 - r2 + 1) * abs(c1 - c2 + 1)
            heapq.heappush(max_heap, (-area, tiles[i], tiles[j]))
    return max_heap


def part1(tiles: list[tuple[int, int]]) -> int:
    return -max_areas(tiles)[0][0]


def get_boundary_points(corner1: tuple[int, int], corner2: tuple[int, int]) -> list[tuple[int, int]]:
    x1, y1 = corner1
    x2, y2 = corner2
    
    coordinates: list[tuple[int, int]] = []
    
    if x1 != x2:
        step = 1 if x2 > x1 else -1
        for x in range(x1, x2 + step, step):
            coordinates.append((x, y1))
    
    if y1 != y2:
        step = 1 if y2 > y1 else -1
        for y in range(y1 + step, y2 + step, step):
            coordinates.append((x2, y))
    
    return coordinates


def create_boundary(red_tiles: list[tuple[int, int]]) -> tuple[set[tuple[int, int]], defaultdict[int, list[int]], defaultdict[int, list[int]]]:
    boundary_r: defaultdict[int, list[int]] = defaultdict(list)
    boundary_c: defaultdict[int, list[int]] = defaultdict(list)
    boundary_points: set[tuple[int, int]] = set()
    for ((r1, c1), (r2, c2)) in zip(red_tiles, red_tiles[1:]):
        if r1 == r2:
            dc = +1 if c2 > c1 else -1
            while c1 != c2:
                boundary_r[r1].append(c1)
                boundary_c[c1].append(r1)
                boundary_points.add((r1, c1))
                c1 += dc
        else:
            dr = +1 if r2 > r1 else -1
            while r1 != r2:
                boundary_r[r1].append(c1)
                boundary_c[c1].append(r1)
                boundary_points.add((r1, c1))
                r1 += dr
    for _, cs in boundary_r.items():
        cs.sort()
    for _, rs in boundary_c.items():
        rs.sort()
    return boundary_points, boundary_r, boundary_c


def print_boundary(boundary: defaultdict[int, list[int]], red_tiles: list[tuple[int, int]]) -> None:
    max_r = max(r for (r, _) in red_tiles)
    max_c = max(c for (_, c) in red_tiles)
    grid = [[Tile.PLAIN for _ in range(max_c + 1)] for _ in range(max_r + 1)]
    print("  " + " ".join(map(str, range(max_c + 1))))
    for r in boundary:
        for c in boundary[r]:
            if (r, c) in red_tiles:
                grid[r][c] = Tile.RED
            else:
                grid[r][c] = Tile.GREEN
    for r, row in enumerate(grid):
        print(f"{str(r)[-1]} " + " ".join(str(elem) for elem in row))
    

# def create_area_for_point_pairs(points_i: tuple[int, int], points_j: tuple[int, int]):
#     r1, c1 = points_i
#     r2, c2 = points_j
#     for r in range(min(r1, r2), max(r1, r2) + 1):
#         for c in range(min(c1, c2), max(c1, c2) + 1):
#             yield (r, c)


def is_valid_area(boundary_points: set[tuple[int, int]], boundary_r: defaultdict[int, list[int]], boundary_c: defaultdict[int, list[int]], points_i: tuple[int, int], points_j: tuple[int, int]) -> bool:
    square_boundary = get_boundary_points(points_i, points_j)
    for r, c in square_boundary:
        if (r, c) in boundary_points:
            continue
        r_crossing_count = bisect.bisect_right(boundary_r[r], c)
        c_crossing_count = bisect.bisect_right(boundary_c[c], r)
        if r_crossing_count % 2 != 1 or c_crossing_count % 2 != 1:
            return False
    return True


def part2(red_tiles: list[tuple[int, int]]):
    boundary_points, boundary_r, boundary_c = create_boundary(red_tiles)
    # print_boundary(boundary_r, red_tiles)
    max_areas_heap = max_areas(red_tiles)
    while max_areas_heap:
        max_area, point_i, point_j = heapq.heappop(max_areas_heap)
        if not is_valid_area(boundary_points, boundary_r, boundary_c, point_i, point_j):
            continue
        return -max_area
    return -1


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
