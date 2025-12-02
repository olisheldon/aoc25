import sys
from pathlib import Path


def invalid_p1(id_val: int) -> bool:
    id_str = str(id_val)
    if len(id_str) % 2:
        return False
    first_half = id_str[:len(id_str) // 2]
    second_half = id_str[len(id_str) // 2:]
    return first_half == second_half


def part1(id_pairs: list[list[int]]):
    res = 0
    for start, end in id_pairs:
        for i in range(start, end + 1):
            if invalid_p1(i):
                res += i
    return res


def invalid_p2(id_val: int) -> bool:
    id_str = str(id_val)
    for digit_len in range(1, len(id_str) // 2 + 1):
        sub_id = id_str[:digit_len]
        s = sub_id * (len(id_str) // digit_len)
        if id_str == s:
            return True
    return False


def part2(id_pairs: list[list[int]]):
    res = 0
    for start, end in id_pairs:
        for i in range(start, end + 1):
            if invalid_p2(i):
                res += i
    return res


def parse(data: str) -> list[list[int]]:
    id_pairs = data.split(",")
    res = []
    for id_pair in id_pairs:
        res.append(list(map(int, id_pair.split("-"))))
    return res


if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else f"../data/{Path(__file__).stem}.txt"
    with open(filename) as f:
        inp = f.read()
    inp_data = parse(inp)

    print("part1=" + str(part1(inp_data)))
    print("part2=" + str(part2(inp_data)))
