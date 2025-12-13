from collections import defaultdict
import heapq
import sys
from pathlib import Path

TEST = False
CONNECTIONS = 10 if TEST else 1000

def part1(coords: list[tuple[int, int, int]]):
    adj: dict[int, list[tuple[int, int]]] = defaultdict(list) # {i : (dist, j)}
    min_heap: list[tuple[int, tuple[int, int]]] = [] # (dist, (i, j))
    for i in range(len(coords)):
        x1, y1, z1 = coords[i]
        for j in range(i + 1, len(coords)):
            x2, y2, z2 = coords[j]
            dist = (x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2
            adj[i].append((j, dist))
            adj[j].append((i, dist))
            heapq.heappush(min_heap, (dist, (i, j)))

    connections = 0
    node_to_circuit: dict[int, set[int]] = {} # {i : circuit}
    while connections < CONNECTIONS:
        dist, (i, j) = heapq.heappop(min_heap)
        if i not in node_to_circuit and j not in node_to_circuit:
            # neither nodes are in a circuit, so just join and create circuit
            node_to_circuit[i] = {i, j}
            node_to_circuit[j] = node_to_circuit[i]
        elif i in node_to_circuit and j in node_to_circuit:
            # both in circuits, maybe different circuits so join the circuits (add j's circuit with i's circuit)
            if node_to_circuit[i] is node_to_circuit[j]:
                connections += 1
                continue
            node_to_circuit[i] = node_to_circuit[i].union(node_to_circuit[j])
            for node in node_to_circuit[i]:
                node_to_circuit[node] = node_to_circuit[i]
            # del node_to_circuit[j]
        elif i in node_to_circuit:
            # i is in a circuit, so join j with that circuit
            node_to_circuit[i].add(j)
            node_to_circuit[j] = node_to_circuit[i]
        elif j in node_to_circuit:
            # j is in a circuit, so join i with that circuit
            node_to_circuit[j].add(i)
            node_to_circuit[i] = node_to_circuit[j]
        else:
            raise RuntimeError(f"should have enumerated all possibilities, {i=}, {j=}, {node_to_circuit=}, {node_to_circuit=}")
        connections += 1
        circuits = sorted(list({id(s): s for s in node_to_circuit.values()}.values()), reverse=True, key=set.__sizeof__)
    circuits = sorted(list({id(s): s for s in node_to_circuit.values()}.values()), reverse=True, key=set.__sizeof__)
    return len(circuits[0]) * len(circuits[1]) * len(circuits[2])
            

def part2():
    pass


def parse(data: str):
    return [tuple(map(int, row.split(","))) for row in data.split("\n")]


if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else f"../data/{Path(__file__).stem}.txt"
    with open(filename) as f:
        inp = f.read()
    inp_data = parse(inp)

    print("part1=" + str(part1(inp_data)))
    print("part2=" + str(part2(inp_data)))
