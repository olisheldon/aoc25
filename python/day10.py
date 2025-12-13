from collections import deque
import sys
from pathlib import Path
from enum import Enum, StrEnum, auto


class IndicatorLight(StrEnum):
    ON = '#'
    OFF = '.'

    @staticmethod
    def toggle(light: 'IndicatorLight') -> 'IndicatorLight':
        return IndicatorLight.ON if light is IndicatorLight.OFF else IndicatorLight.OFF
    

class Target(Enum):
    LIGHTS = auto()
    JOLTAGE = auto()


Row = tuple[list[IndicatorLight], list[list[int]], list[int]]
Comparer = list[IndicatorLight] | list[int]

class Scheme:

    def __init__(self, row: Row, target: Target):
        self.target: Target = target

        self.target_lights: list[IndicatorLight] = row[0]
        self.buttons: list[list[int]] = row[1]
        self.target_joltage: list[int] = row[2]
    

    @staticmethod
    def create_schemes(rows: list[Row], target: Target = Target.LIGHTS) -> list['Scheme']:
        return [Scheme(row, target) for row in rows]
    

    def press_button(self, comparer: Comparer, button: list[int]) -> Comparer:
        comparer = comparer.copy()
        match self.target:
            case Target.LIGHTS:
                for b in button:
                    comparer[b] = IndicatorLight.toggle(comparer[b])
                return comparer
            case Target.JOLTAGE:
                for b in button:
                    comparer[b] += 1
                return comparer
            case _:
                raise RuntimeError()
            
    
    def have_we_gone_past(self, comparer: Comparer) -> bool:
        match self.target:
            case Target.LIGHTS:
                return False
            case Target.JOLTAGE:
                return any(c > t for c, t in zip(comparer, self.target_joltage))
            case _:
                raise RuntimeError()

    

    def are_we_there_yet(self, comparer: Comparer) -> bool:
        match self.target:
            case Target.LIGHTS:
                return comparer == self.target_lights
            case Target.JOLTAGE:
                return comparer == self.target_joltage
            case _:
                raise RuntimeError()
    

    def init_comparer(self) -> list[IndicatorLight] | list[int]:
        match self.target:
            case Target.LIGHTS:
                return [IndicatorLight.OFF] * len(self.target_lights)
            case Target.JOLTAGE:
                return [0] * len(self.target_joltage)
            case _:
                raise RuntimeError()
    
    
    def simulate(self) -> int:
        return self.bfs()

    def bfs(self) -> int:
        comparer: Comparer = self.init_comparer()
        visited: set[tuple[IndicatorLight, ...]] = set()
        q: deque[tuple[list[IndicatorLight], list[int]]] = deque([(comparer, [])]) # (light state, list of buttons pressed)
        steps = 0
        while q:
            for _ in range(len(q)):
                comparer, buttons_pressed = q.popleft()
                if self.are_we_there_yet(comparer):
                    return steps
                if self.have_we_gone_past(comparer):
                    continue
                if tuple(comparer) in visited:
                    continue
                visited.add(tuple(comparer))

                for i, button in enumerate(self.buttons):
                    q.append((self.press_button(comparer, button), buttons_pressed + [i]))
            steps += 1
            print(steps)
        return -1


def part1(rows: list[Row]):
    schemes = Scheme.create_schemes(rows, target=Target.LIGHTS)
    return sum(scheme.simulate() for scheme in schemes)


def part2(rows: list[Row]):
    schemes = Scheme.create_schemes(rows, target=Target.JOLTAGE)
    return sum(scheme.simulate() for scheme in schemes[:1])


def parse(data: str) -> list[Row]:
    rows: list[Row] = []
    for row in data.split("\n"):
        target_indicator_lights, *buttons, joltage = row.split()
        target_indicator_lights = [IndicatorLight(light) for light in target_indicator_lights[1:-1]]
        buttons = [list(map(int, button[1:-1].split(","))) for button in buttons]
        joltage = list(map(int, joltage[1:-1].split(",")))
        rows.append((target_indicator_lights, buttons, joltage))
    return rows


if __name__ == "__main__":
    filename = sys.argv[1] if len(sys.argv) > 1 else f"../data/{Path(__file__).stem}.txt"
    with open(filename) as f:
        inp = f.read()
    inp_data = parse(inp)

    print("part1=" + str(part1(inp_data)))
    print("part2=" + str(part2(inp_data)))
