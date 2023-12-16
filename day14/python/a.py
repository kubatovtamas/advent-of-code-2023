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


x = """O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""
print(run_length_encode(x))
