import sys
from pathlib import Path
from typing import Iterator
import more_itertools as mit


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


def get_diffs(nums: list[int]) -> list[int]:
    return [x[1] - x[0] for x in mit.sliding_window(nums, 2)]


def main():
    part, mode = get_args()

    if part == 1:
        total = 0
        for line in read_input(mode):
            diff_lines: list[list[int]] = []

            nums = [int(chrs) for chrs in line.split()]
            diff_lines.append(nums)

            diffs = get_diffs(nums)
            diff_lines.append(diffs)

            while not all(n == 0 for n in diffs):
                diffs = get_diffs(diffs)
                diff_lines.append(diffs)

            diff_lines[-1].append(0)
            for i in range(len(diff_lines) - 2, -1, -1):
                x = diff_lines[i + 1][-1] + diff_lines[i][-1]
                diff_lines[i].append(x)

            total += diff_lines[0][-1]
        print("SOLUTION:", total)

    if part == 2:
        total = 0
        for line in read_input(mode):
            diff_lines: list[list[int]] = []

            nums = list(reversed([int(chrs) for chrs in line.split()]))
            diff_lines.append(nums)

            diffs = get_diffs(nums)
            diff_lines.append(diffs)

            while not all(n == 0 for n in diffs):
                diffs = get_diffs(diffs)
                diff_lines.append(diffs)

            diff_lines[-1].append(0)
            for i in range(len(diff_lines) - 2, -1, -1):
                x = diff_lines[i + 1][-1] + diff_lines[i][-1]
                diff_lines[i].append(x)

            total += diff_lines[0][-1]
        print("SOLUTION:", total)


if __name__ == "__main__":
    main()
