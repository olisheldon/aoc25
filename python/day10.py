from collections import deque
import sys
from pathlib import Path
from enum import StrEnum


class IndicatorLight(StrEnum):
    ON = '#'
    OFF = '.'

    @staticmethod
    def toggle(light: 'IndicatorLight') -> 'IndicatorLight':
        return IndicatorLight.ON if light is IndicatorLight.OFF else IndicatorLight.OFF

Row = tuple[list[IndicatorLight], list[list[int]], list[int]]

class Scheme:

    def __init__(self, row: Row):
        self.target_lights: list[IndicatorLight] = row[0]
        self.buttons: list[list[int]] = row[1]
        self.joltage: list[int] = row[2]
        self.lights = [IndicatorLight.OFF for _ in range(len(self.target_lights))]
    

    @staticmethod
    def create_schemes(rows: list[Row]) -> list['Scheme']:
        return list(map(Scheme, rows))
    

    @staticmethod
    def press_button(lights: list[IndicatorLight], button: list[int]):
        lights = lights.copy()
        for b in button:
            lights[b] = IndicatorLight.toggle(lights[b])
        return lights
    
    
    def simulate(self) -> int:
        lights = [IndicatorLight.OFF for _ in range(len(self.target_lights))]
        visited: set[tuple[IndicatorLight, ...]] = set()
        q: deque[tuple[list[IndicatorLight], list[int]]] = deque([(lights, [])]) # (light state, list of buttons pressed)
        steps = 0
        while q:
            for _ in range(len(q)):
                lights, buttons_pressed = q.popleft()
                if lights == self.target_lights:
                    return steps
                if tuple(lights) in visited:
                    continue
                visited.add(tuple(lights))

                for i, button in enumerate(self.buttons):
                    q.append((Scheme.press_button(lights, button), buttons_pressed + [i]))
            steps += 1
        return -1


def part1(rows: list[Row]):
    schemes = Scheme.create_schemes(rows)
    return sum(scheme.simulate() for scheme in schemes)


def part2():
    pass


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
