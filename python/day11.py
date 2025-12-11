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
    END = 'out'

    @cache
    def dfs(u: str, visited: frozenset[str]) -> int:
        if u == END:
            return 1 if 'fft' in visited and 'dac' in visited else 0
        
        res = 0
        for v in adj[u]:
            visited = visited.union({v})
            res += dfs(v, visited)
            visited = visited.difference({v})
        return res
    return dfs(START, frozenset())


def parse(data: str) -> dict[str, list[str]]:
    adj: dict[str, list[str]] = {}
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
