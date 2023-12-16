import sys
from enum import Enum, auto
from pathlib import Path
from typing import Iterable, Iterator

import more_itertools as mit

type Matrix = list[str]


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


def print_matrix(matrix: Matrix) -> None:
    for row in matrix:
        print(row)


def transpose_matrix(matrix: Matrix) -> Matrix:
    return ["".join(col) for col in zip(*matrix)]


def rows_pairwise_equal(
    matrix: Matrix, row_idxs1: Iterable[int], row_idxs2: Iterable[int]
) -> bool:
    for fst, snd in zip(row_idxs1, row_idxs2):
        if matrix[fst] != matrix[snd]:
            return False
    return True


def calc_value_for_matrix(matrix: Matrix, kind: str, num: int) -> int:
    for i in range(1, len(matrix)):
        idxs_lt = list(range(i))
        idxs_ge = list(range(i, len(matrix)))

        if rows_pairwise_equal(matrix, reversed(idxs_lt), idxs_ge):
            print(f"{num=}, {kind=}, {i=}")
            return i

    return 0


def calc_value_for_matrix_with_replace(matrix: Matrix, kind: str, num: int) -> int:
    for i in range(1, len(matrix)):
        matching_rows = 0
        one_diff_rows = 0

        idxs_lt = list(range(i))
        idxs_ge = list(range(i, len(matrix)))

        for fst, snd in zip(reversed(idxs_lt), idxs_ge):
            row1 = matrix[fst]
            row2 = matrix[snd]
            if row1 != row2:
                diff_idxs = get_diff_idxs_for_strs(matrix[fst], matrix[snd])
                if len(diff_idxs) == 1:
                    one_diff_rows += 1
            else:
                matching_rows += 1

        window_len = min(len(idxs_lt), len(idxs_ge))
        if one_diff_rows > 0 and matching_rows + one_diff_rows == window_len:
            print(f"{num=}, {kind=}, {i=}")
            return i

    return 0


def get_diff_idxs_for_strs(s1: str, s2: str) -> list[int]:
    diff_idxs: list[int] = []
    for i, (c1, c2) in enumerate(zip(s1, s2)):
        if c1 != c2:
            diff_idxs.append(i)

    return diff_idxs


def main():
    part, mode = get_args()

    if part == 1:
        lines = read_input(mode)
        matrices = list(mit.split_at(lines, lambda line: line.strip() == ""))

        total = 0
        for i, matrix in enumerate(matrices):
            row_idx = calc_value_for_matrix(matrix, kind="row", num=i)
            col_idx = calc_value_for_matrix(transpose_matrix(matrix), kind="col", num=i)

            current = (row_idx * 100) + col_idx
            total += current

        print("SOLUTION:", total)

    if part == 2:
        lines = read_input(mode)
        matrices = list(mit.split_at(lines, lambda line: line.strip() == ""))

        total = 0
        for i, matrix in enumerate(matrices):
            col_idx = calc_value_for_matrix_with_replace(
                transpose_matrix(matrix), kind="col", num=i
            )

            row_idx = calc_value_for_matrix_with_replace(matrix, kind="row", num=i)

            current = (row_idx * 100) + col_idx
            total += current

        print("SOLUTION:", total)


if __name__ == "__main__":
    main()
