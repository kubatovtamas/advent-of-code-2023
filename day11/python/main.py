import itertools as it
import sys
from pathlib import Path
from typing import Iterator


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


def manhattan_dist(pt1: tuple[int, int], pt2: tuple[int, int]) -> int:
    x1, y1 = pt1
    x2, y2 = pt2
    return abs(x2 - x1) + abs(y2 - y1)


def main():
    part, mode = get_args()

    if part == 1:
        line_len = -1
        galaxy_pts: list[tuple[int, int]] = []
        expand_rows: list[int] = []

        for row_idx, line in enumerate(read_input(mode)):
            if line_len == -1:
                line_len = len(line)

            line_has_galaxy = False
            for col_idx, ch in enumerate(line):
                if ch == "#":
                    line_has_galaxy = True
                    galaxy_pts.append((row_idx, col_idx))

            if not line_has_galaxy:
                expand_rows.append(row_idx)

            # print(line)

        galaxy_cols = {col for _, col in galaxy_pts}
        expand_cols = [i for i in range(line_len) if i not in galaxy_cols]

        # print(galaxy_pts)
        # print(expand_rows)
        # print(expand_cols)

        for i, (row_idx, col_idx) in enumerate(galaxy_pts):
            new_row_idx = row_idx
            new_col_idx = col_idx

            for expand_row in expand_rows:
                if expand_row < row_idx:
                    new_row_idx += 1

            for expand_col in expand_cols:
                if expand_col < col_idx:
                    new_col_idx += 1

            galaxy_pts[i] = (new_row_idx, new_col_idx)

        total_dist = 0
        for pt1, pt2 in it.combinations(galaxy_pts, r=2):
            total_dist += manhattan_dist(pt1, pt2)

        print(total_dist)

    if part == 2:
        expand_by = 999999
        line_len = -1
        galaxy_pts: list[tuple[int, int]] = []
        expand_rows: list[int] = []

        for row_idx, line in enumerate(read_input(mode)):
            if line_len == -1:
                line_len = len(line)

            line_has_galaxy = False
            for col_idx, ch in enumerate(line):
                if ch == "#":
                    line_has_galaxy = True
                    galaxy_pts.append((row_idx, col_idx))

            if not line_has_galaxy:
                expand_rows.append(row_idx)

        galaxy_cols = {col for _, col in galaxy_pts}
        expand_cols = [i for i in range(line_len) if i not in galaxy_cols]

        for i, (row_idx, col_idx) in enumerate(galaxy_pts):
            new_row_idx = row_idx
            new_col_idx = col_idx

            for expand_row in expand_rows:
                if expand_row < row_idx:
                    new_row_idx += expand_by

            for expand_col in expand_cols:
                if expand_col < col_idx:
                    new_col_idx += expand_by

            galaxy_pts[i] = (new_row_idx, new_col_idx)

        total_dist = 0
        for pt1, pt2 in it.combinations(galaxy_pts, r=2):
            total_dist += manhattan_dist(pt1, pt2)

        print(total_dist)


if __name__ == "__main__":
    main()
