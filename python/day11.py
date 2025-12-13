from collections import defaultdict
from functools import cache, lru_cache
import sys
from pathlib import Path


def part1(adj: dict[str, list[str]]) -> int:
    START = 'you'
    END = 'out'

    @lru_cache
    def dfs(u: str) -> int:
        if u == END:
            return 1
        
        res = 0
        for v in adj[u]:
            res += dfs(v)
        return res
    return dfs(START)


def part2(adj: dict[str, list[str]]):
    START = 'svr'
    CHECKPOINT1 = 'fft'
    CHECKPOINT2 = 'dac'
    END = 'out'
    route = [START, CHECKPOINT1, CHECKPOINT2, END]

    @cache
    def dfs(u: str, end: str) -> int:
        if u == end:
            return 1
        
        res = 0
        for v in adj[u]:
            res += dfs(v, end)
        return res
    res = 1
    for (u, end) in zip(route, route[1:]):
        res *= dfs(u, end)
    return res


def parse(data: str) -> dict[str, list[str]]:
    adj: dict[str, list[str]] = defaultdict(list)
    for row in data.split("\n"):
        u, neis = row.split(": ")
        adj[u] = list(neis.split())
    return adj


if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else f"../data/{Path(__file__).stem}.txt"
    with open(filename) as f:
        inp = f.read()
    inp_data = parse(inp)

    # print("part1=" + str(part1(inp_data)))
    print("part2=" + str(part2(inp_data)))
