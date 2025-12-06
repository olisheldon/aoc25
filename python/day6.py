import sys
from pathlib import Path


def part1(numbers: list[list[int]], operations: list[str]) -> int:
    res = 0
    for col, op in zip(zip(*numbers), operations):
        col_tot = 1 if op == "*" else 0
        for num in col:
            if op == "*":
                col_tot *= num
            else:
                col_tot += num
        res += col_tot
    return res


def part2():
    pass


def parse(data: str):
    *numbers, operations = data.split("\n")
    numbers = [list(map(int, row.split())) for row in numbers]
    return numbers, operations.split()


if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else f"../data/{Path(__file__).stem}.txt"
    with open(filename) as f:
        inp = f.read()
    inp_data = parse(inp)

    print("part1=" + str(part1(*inp_data)))
    print("part2=" + str(part2(inp_data)))
