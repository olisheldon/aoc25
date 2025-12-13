from collections import defaultdict
import heapq
import sys
from pathlib import Path

TEST = True
CONNECTIONS = 10 if TEST else 1000


def create_circuits(coords: list[tuple[int, int, int]]):
    min_heap: list[tuple[int, tuple[int, int]]] = [] # (dist, (i, j))
    for i in range(len(coords)):
        x1, y1, z1 = coords[i]
        for j in range(i + 1, len(coords)):
            x2, y2, z2 = coords[j]
            dist = (x1 - x2)**2 + (y1 - y2)**2 + (z1 - z2)**2
            heapq.heappush(min_heap, (dist, (i, j)))
    return min_heap


def connect_circuits(min_heap: list[tuple[int, tuple[int, int]]], node_to_circuit: dict[int, set[int]]) -> tuple[int, int]:
    _, (i, j) = heapq.heappop(min_heap)
    if i not in node_to_circuit and j not in node_to_circuit:
        # neither nodes are in a circuit, so just join and create circuit
        node_to_circuit[i] = {i, j}
        node_to_circuit[j] = node_to_circuit[i]
    elif i in node_to_circuit and j in node_to_circuit:
        # both in circuits, maybe different circuits so join the circuits (add j's circuit with i's circuit)
        if node_to_circuit[i] is node_to_circuit[j]:
            return (i, j)
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
    return (i, j)


def part1(coords: list[tuple[int, int, int]]):
    min_heap = create_circuits(coords)
    node_to_circuit: dict[int, set[int]] = {} # {i : circuit}
    connections = 0
    while connections < CONNECTIONS:
        connect_circuits(min_heap, node_to_circuit)
        connections += 1
    circuits = sorted(list({id(s): s for s in node_to_circuit.values()}.values()), reverse=True, key=set.__sizeof__)
    return len(circuits[0]) * len(circuits[1]) * len(circuits[2])
            

def part2(coords: list[tuple[int, int, int]]):
    min_heap = create_circuits(coords)
    node_to_circuit: dict[int, set[int]] = {} # {i : circuit}
    get_num_circuits = lambda: len(set(id(s) for s in node_to_circuit.values()))
    # completely arbitrary, not a sign of good code
    INIT_CIRCUIT = 10
    for _ in range(INIT_CIRCUIT):
        connect_circuits(min_heap, node_to_circuit)
    while get_num_circuits() != 0:
        connect_circuits(min_heap, node_to_circuit)
    res = []
    while min_heap:
        _, (i, j) = heapq.heappop(min_heap)
        res.append(coords[i][0] * coords[j][0])
    return res
    return coords[i][0] * coords[j][0]


def parse(data: str) -> list[tuple[int, int, int]]:
    return [tuple(map(int, row.split(","))) for row in data.split("\n")]


if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else f"../data/{Path(__file__).stem}.txt"
    with open(filename) as f:
        inp = f.read()
    inp_data = parse(inp)

    print("part1=" + str(part1(inp_data)))
    print("part2=" + str(part2(inp_data)))
