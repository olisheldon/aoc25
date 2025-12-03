import sys
from pathlib import Path
import heapq


def max_joltage(bank: list[int], digits=12) -> int:
    res = []
    start = 0
    
    for i in range(digits):
        end = len(bank) - (digits - i) + 1

        max_digit = max(bank[start:end])
        max_idx = bank.index(max_digit, start, end)
        
        res.append(max_digit)
        start = max_idx + 1
    return int("".join(map(str, res)))


def part1(banks: list[list[int]]):
    res = []
    for bank in banks:
        res.append(max_joltage(bank, digits=2))
    return sum(res)


def part2(banks: list[list[int]]):
    res = []
    for bank in banks:
        res.append(max_joltage(bank, digits=12))
    return sum(res)


def parse(data: str) -> list[list[int]]:
    banks = data.split("\n")
    return [list(map(int, bank)) for bank in banks]


if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else f"../data/{Path(__file__).stem}.txt"
    with open(filename) as f:
        inp = f.read()
    inp_data = parse(inp)

    print("part1=" + str(part1(inp_data)))
    print("part2=" + str(part2(inp_data)))
