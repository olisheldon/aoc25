import sys
from pathlib import Path

def part1():
    pass

def part2():
    pass

def parse():
    pass

if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else f"../data/{Path(__file__).stem}.txt"
    with open(filename) as f:
        inp = f.read()

    print("part1=" + str(part1()))
    print("part2=" + str(part2()))