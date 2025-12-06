import sys
from pathlib import Path


def accumulate(col: list[int], op: str) -> int:
    col_tot = 1 if op == "*" else 0
    for num in col:
        if op == "*":
            col_tot *= num
        else:
            col_tot += num
    return col_tot


def part1(data: list[str]) -> int:
    *numbers, operations = data
    numbers = [list(map(int, row.split())) for row in numbers]
    operations = operations.split()
    res = 0
    for col, op in zip(zip(*numbers), operations):
        res += accumulate(col, op)
    return res


def part2(data: list[str]):
    res = []
    i = 0
    col_wise = list(zip(*data))
    op = col_wise[0][-1]
    group = []
    while i in range(len(col_wise)):
        col = col_wise[i]
        if all(x == " " for x in col):
            res.append(accumulate(group, op))
            group = []
            i += 1
            if i not in range(len(col_wise)):
                break
            op = col_wise[i][-1]
            continue
        *num, _ = col
        num = int("".join(n for n in num if n))
        group.append(num)
        i += 1
    res.append(accumulate(group, op))
    return sum(res)


def parse(data: str):
    return data.split("\n")


if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else f"../data/{Path(__file__).stem}.txt"
    with open(filename) as f:
        inp = f.read()
    inp_data = parse(inp)

    print("part1=" + str(part1(inp_data)))
    print("part2=" + str(part2(inp_data)))
