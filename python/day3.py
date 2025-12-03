import sys
from pathlib import Path
from collections import Counter
import heapq


def max_joltage(bank: list[int]) -> int:
    first_digit = max(bank[:len(bank) - 1])
    second_digit = max(bank[bank.index(first_digit) + 1 : len(bank)])
    return int("".join(map(str,[first_digit, second_digit])))


def part1(banks: list[list[int]]):
    res = 0
    for bank in banks:
        res += max_joltage(bank)
    return res


def part2():
    pass


def parse(data: str) -> list[list[int]]:
    banks = data.split("\n")
    return [list(map(int, bank)) for bank in banks]


if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else f"../data/{Path(__file__).stem}.txt"
    with open(filename) as f:
        inp = f.read()
    inp_data = parse(inp)

    print("part1=" + str(part1(inp_data)))
    # print("part2=" + str(part2(inp_data)))
