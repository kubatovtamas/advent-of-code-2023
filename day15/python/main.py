import re
import sys
from collections import defaultdict
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


def hash(s: str) -> int:
    res = 0
    for ch in s:
        res += ord(ch)
        res *= 17
        res %= 256

    return res


def main():
    part, mode = get_args()

    if part == 1:
        steps = list(read_input(mode))[0].split(",")
        hashes = [hash(step) for step in steps]
        print("SOLUTION:", sum(hashes))

    if part == 2:
        pattern = re.compile(r"(?P<label>\w+)(?P<op>[\=\-])(?P<num>\d*)")

        steps = list(read_input(mode))[0].split(",")

        hash_map: defaultdict[int, list[tuple[str, int]]] = defaultdict(list)
        for step in steps:
            if not (match := re.match(pattern, step)):
                raise RuntimeError(f"Cannot parse {step}")

            label, op, num = match.groups()
            hashed_label = hash(label)

            match op:
                case "=":
                    num = int(num)

                    try:
                        labels_ = [lbl for lbl, _ in hash_map[hashed_label]]
                        idx = labels_.index(label)
                        hash_map[hashed_label][idx] = (label, num)
                    except ValueError:
                        hash_map[hashed_label].append((label, num))

                case "-":
                    for idx, (lbl, _) in enumerate(hash_map[hashed_label]):
                        if lbl == label:
                            del hash_map[hashed_label][idx]
                            break
                case _:
                    raise RuntimeError(f"Operator {op} not supported")

        total = sum(
            (k + 1) * (i + 1) * num
            for k, v in hash_map.items()
            for i, (_, num) in enumerate(v)
        )

        print(total)
        assert total == 244403


if __name__ == "__main__":
    main()
