import itertools as it
import multiprocessing
import sys
from math import lcm
from pathlib import Path
from typing import Iterator

type MapLine = tuple[str, tuple[str, str]]


def get_args() -> tuple[int, str]:
    if len(sys.argv) != 3:
        print("Usage: python main.py <1 or 2> <example or full>")
        sys.exit(1)

    part = int(sys.argv[1])
    if part not in (1, 2):
        print("First argument must be either 1 or 2")
        sys.exit(1)

    mode = sys.argv[2]
    if mode not in ("example", "full"):
        print("Second argument must be either example or full")
        sys.exit(1)

    return part, mode


def read_input(name: str) -> Iterator[str]:
    file_path = Path(__file__).parent / ".." / "input" / name
    with open(file_path, "r") as f:
        for line in f:
            yield line.rstrip()


def parse_line(line: str) -> MapLine:
    key, val = line.split(" = ")
    left, right = val.strip("()").split(", ")
    dirs = (left, right)

    return key, dirs


def worker_step(args: tuple[str, dict[str, tuple[str, str]], str]):
    current_pos, maps, direction = args
    idx = 0 if direction == "L" else 1
    next_pos = maps[current_pos][idx]

    return next_pos.endswith("Z"), next_pos


def main():
    dir_map = {"L": 0, "R": 1}
    part, mode = get_args()

    if part == 1:
        lines = read_input(mode)

        directions_line = next(lines)
        map_lines = (line for line in lines if line != "")
        map_objs = (parse_line(line) for line in map_lines)

        directions = it.cycle(c for c in directions_line)
        maps = {key: dirs for key, dirs in map_objs}

        steps_req = 0
        current_pos = "AAA"
        while current_pos != "ZZZ":
            dir_to_take = next(directions)
            idx = dir_map[dir_to_take]

            next_pos = maps[current_pos][idx]

            current_pos = next_pos
            steps_req += 1

        print("SOLUTION:", steps_req)

    if part == 2:
        lines = read_input(mode)

        directions_line = next(lines)
        map_lines = (line for line in lines if line != "")
        map_objs = (parse_line(line) for line in map_lines)

        directions = it.cycle(directions_line)
        maps = {key: dirs for key, dirs in map_objs}

        step_req_list: list[int] = []
        current_positions = tuple(key for key in maps.keys() if key.endswith("A"))
        for current_pos in current_positions:
            steps_req = 0
            while not current_pos.endswith("Z"):
                dir_to_take = next(directions)
                idx = dir_map[dir_to_take]

                next_pos = maps[current_pos][idx]

                current_pos = next_pos
                steps_req += 1
            step_req_list.append(steps_req)

        solution = lcm(*step_req_list)
        print("SOLUTION:", solution)


if __name__ == "__main__":
    main()
