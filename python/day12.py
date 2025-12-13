from collections import defaultdict
from dataclasses import dataclass
from enum import StrEnum
import sys
from pathlib import Path

class Tiles(StrEnum):
    PRESENT = '#'
    EMPTY = '.'


@dataclass
class Region:
    r: int
    c: int
    shapes: dict[int, list[list[Tiles]]]
    required_shapes: list[int]


def part1():
    # we want to minimize void space
    # we do dfs but priority queue or something like that
    # place blocks that minimize void space

    # void space 


def part2():
    pass


def parse(data: str):
    *shapes, regions = data.split("\n\n")
    shape_by_index: dict[int, list[list[Tiles]]] = defaultdict(list)
    for i, shape in enumerate(shapes):
        for row in shape.split("\n")[1:]:
            shape_by_index[i].append(list(map(Tiles, row)))
    required: list[Region] = []
    for region in regions.split("\n"):
        dimensions, requirements = region.split(": ")
        r, c = list(map(int, dimensions.split("x")))
        required.append(Region(r, c, shape_by_index, list(map(int, requirements.split()))))

if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else f"../data/{Path(__file__).stem}.txt"
    with open(filename) as f:
        inp = f.read()
    inp_data = parse(inp)

    print("part1=" + str(part1(inp_data)))
    print("part2=" + str(part2(inp_data)))
