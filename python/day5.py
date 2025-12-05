import sys
from pathlib import Path


def part1(fresh_ingredient_ranges, available_ingredient_ids):
    fresh_ingredient_ranges = [range(fresh[0], fresh[1] + 1) for fresh in fresh_ingredient_ranges]
    res = 0
    for ing_id in available_ingredient_ids:
        for fresh_range in fresh_ingredient_ranges:
            if ing_id in fresh_range:
                res += 1
                break
        else:
            continue
    return res


def part2():
    pass


def parse(data: str) -> tuple[list[tuple[int, int]], list[int]]:
    fresh_ingredient_ranges, available_ingredient_ids = data.split("\n\n")
    fresh_ingredient_ranges, available_ingredient_ids = fresh_ingredient_ranges.split("\n"), available_ingredient_ids.split("\n")
    fresh_ingredient_ranges = [list(map(int, r.split("-"))) for r in fresh_ingredient_ranges]
    available_ingredient_ids = list(map(int, available_ingredient_ids))
    return fresh_ingredient_ranges, available_ingredient_ids

if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else f"../data/{Path(__file__).stem}.txt"
    with open(filename) as f:
        inp = f.read()
    inp_data = parse(inp)

    print("part1=" + str(part1(*inp_data)))
    print("part2=" + str(part2(inp_data)))
