from typing import Callable

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


def main():
    res = 0
    with open("../input/full", "r") as f:
        while line := f.readline().rstrip():
            first_num = extract_num(line, str.startswith, lambda line: line[1:])
            last_num = extract_num(line, str.endswith, lambda line: line[:-1])
            res += first_num * 10 + last_num

    print(res)


if __name__ == "__main__":
    main()
