import sys
from typing import Callable, Iterator

strCompFn = Callable[[str, str], bool]
strShortenFn = Callable[[str], str]


def create_two_digit_num(*nums: int):
    return nums[0] * 10 + nums[-1]


str_dict = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}

char_dict = {
    "0": 0,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
}


def extract_num(line: str, str_compare: strCompFn, str_shorten: strShortenFn) -> int:
    while line:
        for k, v in char_dict.items():
            if str_compare(line, k):
                return v

        for k, v in str_dict.items():
            if str_compare(line, k):
                return v

        line = str_shorten(line)

    raise RuntimeError(f"no number could be extracted from {line}")


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


def main():
    part, mode = get_args()

    if part == 1:
        res = 0
        for line in read_input(mode):
            line_nums = [int(ch) for ch in line if ch.isdigit()]
            res += line_nums[0] * 10 + line_nums[-1]

        print(res)

    if part == 2:
        res = 0
        for line in read_input(mode):
            first_num = extract_num(line, str.startswith, lambda line: line[1:])
            last_num = extract_num(line, str.endswith, lambda line: line[:-1])
            res += first_num * 10 + last_num

        print(res)


if __name__ == "__main__":
    main()
