import sys
from collections import defaultdict
from typing import Iterator

AVAILABLE_CUBES = {
    "red": 12,
    "green": 13,
    "blue": 14,
}


def split_off_game_id(line: str) -> tuple[int, str]:
    game_num, rest_of_line = line.removeprefix("Game ").split(":", 1)

    return int(game_num), rest_of_line


def get_game_sets(line: str) -> list[str]:
    sets = [s.strip() for s in line.split(";")]

    return sets


def get_set_cubes(a_set: str) -> dict[str, int]:
    # You may find this too readable
    # set_cubes = {}

    # num_color_groups = a_set.split(", ")

    # for num_color in num_color_groups:
    #     elems = num_color.split(" ")

    #     quant, color = int(elems[0]), elems[1]

    #     set_cubes[color] = quant

    # return set_cubes

    # In that case, use this
    return {
        color: int(quant)
        for num_color in a_set.split(", ")
        for quant, color in (num_color.split(" "),)
    }


def valid_cube_quantities(set_cubes: dict[str, int]) -> bool:
    for color, quant in set_cubes.items():
        if AVAILABLE_CUBES[color] < quant:
            return False

    return True


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
        sum_valid_ids = 0

        for line in read_input(mode):
            game_id, rest_of_line = split_off_game_id(line)

            game_sets = get_game_sets(rest_of_line)

            game_is_valid = True
            for game_set in game_sets:
                set_cubes = get_set_cubes(game_set)

                if not valid_cube_quantities(set_cubes):
                    game_is_valid = False
                    break

            if game_is_valid:
                sum_valid_ids += game_id

        print(sum_valid_ids)

    if part == 2:
        for line in read_input(mode):
            print(line)


if __name__ == "__main__":
    main()
