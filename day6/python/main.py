import re
import sys
from typing import Iterator

import numpy as np


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
    with open(f"../input/{name}", "r") as f:
        for line in f:
            yield line.rstrip()


def count_series_points(time_avail: int, dist_record: int) -> int:
    """
    Count the number of points in a series where the value is strictly greater than a given record.

    The series is defined by the formula a_n = (N - n) * n, where:
    - N is the total time available.
    - n is an integer ranging from 0 to N (inclusive).
    - a_n is the value at each point in the series.

    The function calculates how many points in this series exceed a given distance record,
    by solving for the quadratic inequality (N - n) * n > t == -n^2 + Nn - t > 0

    Args:
        time_avail (int): The total time available (N in the series formula).
        dist_record (int): The distance record to compare against.

    Returns:
        int: The number of points in the series exceeding the distance record.
    """
    # Adding epsilon to ensure distances equal to record are not counted
    thresh = dist_record + 1e-6

    coefficients = [-1, time_avail, -thresh]

    roots = np.roots(coefficients)

    num_points = np.ceil(roots.max()) - np.ceil(roots.min())

    return int(num_points)


def main():
    part, mode = get_args()

    if part == 1:
        line_nums: list[list[int]] = []
        for line in read_input(mode):
            numbers = re.findall(r"\d+", line)
            numbers = [int(num) for num in numbers]
            line_nums.append(numbers)

        total = 1
        times = line_nums[0]
        dists = line_nums[1]

        for time, dist in zip(times, dists):
            num_points = count_series_points(time, dist)
            total *= num_points

        print("SOLUTION:", total)

    if part == 2:
        for line in read_input(mode):
            print(line)


if __name__ == "__main__":
    main()
