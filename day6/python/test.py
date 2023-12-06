import numpy as np


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


Ns = [7, 15, 30]
ts = [9, 40, 200]

res = [count_series_points(N, t) for N, t in zip(Ns, ts)]

assert res == [4, 8, 9]
print(res)
