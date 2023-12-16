import functools as ft
import re
import sys
from pathlib import Path
from typing import Iterator

PATTERN = re.compile("(#+)")


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


def parse_input1(line: str) -> tuple[str, tuple[int, ...]]:
    groups = line.split()
    symbols = groups[0]
    nums = tuple(int(n) for n in groups[1].split(","))

    return symbols, nums


def parse_input2(line: str) -> tuple[str, tuple[int, ...]]:
    groups = line.split()
    symbols = groups[0]
    symbols = "?".join([symbols for _ in range(5)])

    nums = groups[1]
    nums = ",".join([nums for _ in range(5)])
    nums = tuple(int(n) for n in nums.split(","))

    return symbols, nums


def count_len_hashes(symbols: str, nums: tuple[int, ...]) -> int:
    counter = 0
    for char in symbols:
        if char == "." or counter == nums[0]:
            break
        counter += 1

    return counter


@ft.cache
def count_valid_arrangements(symbols: str, nums: tuple[int, ...]) -> int:
    # Base cases
    if not symbols and not nums:
        # Valid arrangement
        return 1
    if not symbols and nums:
        # Invalid arrangement
        return 0

    # Recurse
    match symbols[0]:
        case ".":
            # Continue with the next symbol
            return count_valid_arrangements(symbols[1:], nums)

        case "?":
            # Count '?' as '.'
            unk_counted_as_dot = count_valid_arrangements(symbols[1:], nums)

            # Count '?' as '#'
            unk_counted_as_hash = 0
            if nums:
                # Calculate the length of consecutive '#'s
                counter = 0
                for char in symbols:
                    if char == "." or counter == nums[0]:
                        break
                    counter += 1

                # Validate and recurse if '#' sequence is valid
                if counter == nums[0]:
                    if counter == len(symbols) or symbols[counter] != "#":
                        unk_counted_as_hash += count_valid_arrangements(
                            symbols[counter + 1 :], nums[1:]
                        )

            return unk_counted_as_dot + unk_counted_as_hash

        case "#":
            # Handle '#' symbol
            if not nums:
                # Invalid arrangement if no numbers left
                return 0

            # Calculate the length of consecutive '#'s
            counter = 0
            for char in symbols:
                if char == "." or counter == nums[0]:
                    break
                counter += 1

            # Validate and recurse if '#' sequence is valid
            if counter == nums[0]:
                if counter == len(symbols) or symbols[counter] != "#":
                    return count_valid_arrangements(symbols[counter + 1 :], nums[1:])
            return 0

        case _:
            # Handle invalid symbol
            raise RuntimeError("Invalid symbol in input:", symbols[0])


def main():
    part, mode = get_args()

    if part == 1:
        total = 0

        for line_num, line in enumerate(read_input(mode), start=1):
            symbols, nums = parse_input1(line)

            line_valid = count_valid_arrangements(symbols, nums)

            total += line_valid

            print("Processed line:", line_num, "valid:", line_valid)

        print(total)
    if part == 2:
        total = 0

        for line_num, line in enumerate(read_input(mode), start=1):
            symbols, nums = parse_input2(line)
            total += count_valid_arrangements(symbols, nums)

            print("Processed line", line_num)

        print(total)


if __name__ == "__main__":
    main()
