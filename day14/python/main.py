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


def str_repl(s: str, idx: int, r: str) -> str:
    return s[:idx] + r + s[idx + 1 :]


def rotate_matrix_90_degrees(matrix: list[str]) -> list[str]:
    transposed = ["".join(row) for row in zip(*matrix)]
    return [row[::-1] for row in transposed]


def run_sim_north(inp_lines: list[str]) -> list[str]:
    # Add helper first line
    lines = inp_lines[:]
    lines.insert(0, "#" * len(lines[0]))

    # Counts round rocks encountered on each index
    mask = [0 for _ in lines[0]]

    # Holds the data after running the simulation
    transformed_lines: list[str] = []

    for line in reversed(lines):
        # 1. Insert line without round rocks
        transformed_lines.insert(0, line.replace("O", "."))

        # 2. Collect sq rock indexes, modify mask that counts round rocks encountered
        square_rock_idxs: list[int] = []
        for i, ch in enumerate(line):
            if ch == "O":
                mask[i] += 1
            if ch == "#":
                square_rock_idxs.append(i)

        # Count of 'O's for each '#' index
        counts = [mask[i] for i in square_rock_idxs]

        # 3. While there are 'O's to place, modify lines below current line
        line_idx_to_change = 1  # Pointer to lines below current, for placing 'O's
        while not all(count == 0 for count in counts):
            # Iterate over all '#' idx and count pair
            for i in range(len(counts)):
                count = counts[i]
                curr_sq_rock_idx = square_rock_idxs[i]

                # If remaining count: place 'O' in lines below
                if count > 0:
                    transformed_lines[line_idx_to_change] = str_repl(
                        transformed_lines[line_idx_to_change], curr_sq_rock_idx, "O"
                    )

                    mask[curr_sq_rock_idx] -= 1  # Count 'O's: 1 less to place
                    counts = [mask[i] for i in square_rock_idxs]  # Recompute counts

            line_idx_to_change += 1

    # Remove helper first line
    transformed_lines = transformed_lines[1:]

    return transformed_lines


def count_total_load(lines: list[str]) -> int:
    total = 0
    for i, line in enumerate(lines):
        weight = len(lines) - i
        num_rocks = sum(1 for ch in line if ch == "O")

        total += num_rocks * weight

    return total


def run_length_encode(matrix: list[str]):
    encoding: list[str] = []
    last_char = matrix[0][0]
    count = 0

    for row in matrix:
        for char in row:
            if char == "\n":
                continue

            if char == last_char:
                count += 1
            else:
                encoding.append(f"{count}{last_char}")
                last_char = char
                count = 1

    # Adding the last character and its count
    encoding.append(f"{count}{last_char}")

    return "".join(encoding)


def main():
    part, mode = get_args()

    if part == 1:
        lines = list(read_input(mode))

        transformed_lines = run_sim_north(lines)
        total_load = count_total_load(transformed_lines)

        print("SOLUTION:", total_load)
    if part == 2:
        lines = list(read_input(mode))

        matrix_configurations: list[str] = []
        loads: list[int] = []

        north_matrix = lines
        for cycle in range(1_000_000_000):
            print("Running cycle:", cycle)

            north_matrix = run_sim_north(north_matrix)

            west_matrix = rotate_matrix_90_degrees(north_matrix)
            west_matrix = run_sim_north(west_matrix)

            south_matrix = rotate_matrix_90_degrees(west_matrix)
            south_matrix = run_sim_north(south_matrix)

            east_matrix = rotate_matrix_90_degrees(south_matrix)
            east_matrix = run_sim_north(east_matrix)

            north_matrix = rotate_matrix_90_degrees(east_matrix)

            load_after_cycle = count_total_load(north_matrix)
            loads.append(load_after_cycle)

            for row in north_matrix:
                print(row)
            print()

            encoded_sim_res = run_length_encode(north_matrix)
            # encoded_sim_res = "".join(north_matrix)
            if encoded_sim_res in matrix_configurations:
                cycle_len = len(matrix_configurations)
                print("cycle len=", cycle_len)
                return
            else:
                matrix_configurations.append(encoded_sim_res)

        # print("SOLUTION:", total_load)


if __name__ == "__main__":
    main()
