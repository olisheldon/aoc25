from collections import defaultdict, deque
from functools import cache
import heapq
import sys
from pathlib import Path
from enum import StrEnum
import bisect

sys.setrecursionlimit(10000000)


class Tile(StrEnum):
    RED = '#'
    GREEN = 'X'
    PLAIN = '.'
    OUTSIDE = 'O'
    INSIDE = 'I'


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


def get_perimeter_points(corner1: tuple[int, int], corner2: tuple[int, int]) -> list[tuple[int, int]]:
    x1, y1 = corner1
    x2, y2 = corner2
    
    perimeter_points: list[tuple[int, int]] = []
    
    if x1 != x2:
        step = 1 if x2 > x1 else -1
        for x in range(x1, x2 + step, step):
            perimeter_points.append((x, y1))
    
    if y1 != y2:
        step = 1 if y2 > y1 else -1
        for y in range(y1 + step, y2 + step, step):
            perimeter_points.append((x2, y))
    
    return perimeter_points


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
    square_boundary = get_perimeter_points(points_i, points_j)
    for r, c in square_boundary:
        if (r, c) in boundary_points:
            continue
        r_crossing_count = bisect.bisect_right(boundary_r[r], c)
        c_crossing_count = bisect.bisect_right(boundary_c[c], r)
        if r_crossing_count % 2 != 1 or c_crossing_count % 2 != 1:
            return False
    return True


def compressed(red_tiles: list[tuple[int, int]]) -> int:
    r_coords, c_coords = zip(*red_tiles)
    ROWS, COLS = len(r_coords), len(c_coords)
    NEIGHBOURS = ((1, 0), (-1, 0), (0, 1), (0, -1))
    compressed_to_coord_r = {i : r for i, r in enumerate(r_coords)}
    compressed_to_coord_c = {i : c for i, c in enumerate(c_coords)}
    coord_to_compressed_r = {r : i for i, r in enumerate(r_coords)}
    coord_to_compressed_c = {c : i for i, c in enumerate(c_coords)}
    compressed_tiles: list[tuple[int, int]] = [(coord_to_compressed_r[r], coord_to_compressed_c[c]) for (r, c) in red_tiles]
    compressed_grid = [[Tile.INSIDE for _ in range(ROWS)] for _ in range(COLS)]
    boundary, boundary_r, _ = create_boundary(compressed_tiles)
    for r in boundary_r:
        for c in boundary_r[r]:
            if (r, c) in compressed_tiles:
                compressed_grid[r][c] = Tile.RED
            else:
                compressed_grid[r][c] = Tile.GREEN
    
    q = deque([(0, 0)])
    visited: set[tuple[int, int]] = set()
    while q:
        for _ in range(len(q)):
            r, c = q.popleft()
            if (
                r not in range(ROWS) or
                c not in range(COLS) or
                compressed_grid[r][c] is not Tile.INSIDE or
                (r, c) in visited
            ):
                continue
            visited.add((r, c))
            compressed_grid[r][c] = Tile.OUTSIDE
            
            for dr, dc in NEIGHBOURS:
                q.append((r + dr, c + dc))
    
    for row in compressed_grid:
        print("".join(row))
    
    max_areas_heap = max_areas(red_tiles)
    while max_areas_heap:
        area, (i_r, i_c), (j_r, j_c) = heapq.heappop(max_areas_heap)
        compressed_i_coord = coord_to_compressed_r[i_r], coord_to_compressed_c[i_c]
        compressed_j_coord = coord_to_compressed_r[j_r], coord_to_compressed_c[j_c]
        perimeter_points = get_perimeter_points(compressed_i_coord, compressed_j_coord)
        for r, c in perimeter_points:
            if compressed_grid[r][c] is Tile.OUTSIDE:
                break
        else:
            continue
        return -area
    return -1


def part2(red_tiles: list[tuple[int, int]]):
    return compressed(red_tiles)


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
