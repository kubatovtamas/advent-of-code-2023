import sys
from enum import Enum
from pathlib import Path
from typing import Iterator, Optional
from copy import deepcopy


type Matrix = list[list[Tile]]


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


class TileType(Enum):
    BACKSLASH = "\\"
    FORWSLASH = "/"
    VERTSPLIT = "|"
    HORISPLIT = "-"
    EMPTSPACE = "."
    OUTOFBNDS = "#"


class Tile:
    def __init__(self, symbol: str, is_hit: bool = False) -> None:
        self.type = TileType(symbol)
        self.is_hit = is_hit
        self.hit_from_dirs: set[Dir] = set()

    def __repr__(self) -> str:
        if self.is_hit:
            return f"\033[91m{self.type.value}\033[0m"  # Escape chars for red color
        else:
            return self.type.value


class Pos:
    def __init__(self, row: int, col: int) -> None:
        self.row = row
        self.col = col

    def __repr__(self) -> str:
        return f"[{self.row}, {self.col}]"

    @classmethod
    def based_on_dir(cls, pos: "Pos", dir: "Dir") -> "Pos":
        match dir:
            case Dir.NORTH:
                return Pos(pos.row - 1, pos.col)
            case Dir.EAST:
                return Pos(pos.row, pos.col + 1)
            case Dir.SOUTH:
                return Pos(pos.row + 1, pos.col)
            case Dir.WEST:
                return Pos(pos.row, pos.col - 1)


class Dir(Enum):
    NORTH = "N"
    EAST = "E"
    SOUTH = "S"
    WEST = "W"

    def get_arrow(self) -> str:
        arrows = {"N": "↑", "E": "→", "S": "↓", "W": "←"}
        return arrows[self.value]

    @classmethod
    def from_positions(cls, curr_pos: Pos, prev_pos: Pos) -> "Dir":
        if curr_pos.col == prev_pos.col:
            if curr_pos.row > prev_pos.row:
                return cls.SOUTH
            else:
                return cls.NORTH

        if curr_pos.col > prev_pos.col:
            return cls.EAST

        return cls.WEST


class Beam:
    def __init__(
        self, curr_row: int, curr_col: int, prev_row: int, prev_col: int
    ) -> None:
        self.curr_pos: Pos = Pos(curr_row, curr_col)
        self.prev_pos: Pos = Pos(prev_row, prev_col)
        self.dir = Dir.from_positions(self.curr_pos, self.prev_pos)
        self.out_of_bounds = False

    def __repr__(self) -> str:
        return f"{self.prev_pos} {self.dir.get_arrow()} {self.curr_pos}"

    def step(self, matrix: Matrix) -> tuple["Beam", Optional["Beam"]]:
        new_beam = None

        curr_tile = matrix[self.curr_pos.row][self.curr_pos.col]

        # Check if the tile has already been hit from this direction
        if self.dir in curr_tile.hit_from_dirs:
            self.out_of_bounds = True
            return (self, None)
        else:
            curr_tile.hit_from_dirs.add(self.dir)

        # Get new direction, optionally create new Beam if on split tile type
        match curr_tile.type:
            case TileType.OUTOFBNDS:
                self.out_of_bounds = True
                return (self, None)
            case TileType.EMPTSPACE:
                new_dir = self.dir
            case TileType.BACKSLASH:
                match self.dir:
                    case Dir.NORTH:
                        new_dir = Dir.WEST
                    case Dir.EAST:
                        new_dir = Dir.SOUTH
                    case Dir.SOUTH:
                        new_dir = Dir.EAST
                    case Dir.WEST:
                        new_dir = Dir.NORTH
            case TileType.FORWSLASH:
                match self.dir:
                    case Dir.NORTH:
                        new_dir = Dir.EAST
                    case Dir.EAST:
                        new_dir = Dir.NORTH
                    case Dir.SOUTH:
                        new_dir = Dir.WEST
                    case Dir.WEST:
                        new_dir = Dir.SOUTH
            case TileType.VERTSPLIT:
                match self.dir:
                    case Dir.NORTH:
                        new_dir = self.dir
                    case Dir.EAST:
                        new_dir = Dir.SOUTH
                        new_beam = Beam(
                            self.curr_pos.row - 1,
                            self.curr_pos.col,
                            self.curr_pos.row,
                            self.curr_pos.col,
                        )
                    case Dir.SOUTH:
                        new_dir = self.dir
                    case Dir.WEST:
                        new_dir = Dir.SOUTH
                        new_beam = Beam(
                            self.curr_pos.row - 1,
                            self.curr_pos.col,
                            self.curr_pos.row,
                            self.curr_pos.col,
                        )
            case TileType.HORISPLIT:
                match self.dir:
                    case Dir.NORTH:
                        new_dir = Dir.EAST
                        new_beam = Beam(
                            self.curr_pos.row,
                            self.curr_pos.col - 1,
                            self.curr_pos.row,
                            self.curr_pos.col,
                        )
                    case Dir.EAST:
                        new_dir = self.dir
                    case Dir.SOUTH:
                        new_dir = Dir.EAST
                        new_beam = Beam(
                            self.curr_pos.row,
                            self.curr_pos.col - 1,
                            self.curr_pos.row,
                            self.curr_pos.col,
                        )
                    case Dir.WEST:
                        new_dir = self.dir

        new_pos = Pos.based_on_dir(self.curr_pos, new_dir)

        self.dir = new_dir
        self.prev_pos, self.curr_pos = self.curr_pos, new_pos

        return (self, new_beam)


def create_game_matrix(mode: str) -> Matrix:
    matrix: Matrix = []

    for line in read_input(mode):
        tiles = [Tile("#")] + [Tile(c) for c in line] + [Tile("#")]
        matrix.append(tiles)

    pad_line = [Tile("#") for _ in range(len(matrix[0]))]
    matrix.insert(0, pad_line[:])
    matrix.append(pad_line[:])

    return matrix


def mark_hit_by_beam(matrix: Matrix, beam: Beam) -> None:
    matrix[beam.curr_pos.row][beam.curr_pos.col].is_hit = True


def print_matrix(matrix: Matrix, step: int) -> None:
    print("Step", step)
    max_row_digits = len(str(len(matrix) - 1))
    max_col_digits = len(str(len(matrix[0]) - 1)) + 1

    col_header = " " * (max_row_digits + 1)
    col_header += "".join(str(n).rjust(max_col_digits) for n in range(len(matrix[0])))
    print(col_header)

    for i, line in enumerate(matrix):
        row_num = str(i).rjust(max_row_digits)
        elems = [
            str(el).rjust(max_col_digits, " ") if not el.is_hit else f"  {el}"
            for el in line
        ]
        row_content = "".join(elems)
        print(f"{row_num} {row_content}")
    print()


def get_num_energized(matrix: Matrix) -> int:
    total = 0
    for i in range(1, len(matrix) - 1):
        for j in range(1, len(matrix[i]) - 1):
            if matrix[i][j].is_hit:
                total += 1

    return total


def main():
    part, mode = get_args()

    matrix = create_game_matrix(mode)

    if part == 1:
        starting_beam = Beam(1, 1, 1, 0)
        beams = [starting_beam]

        tick = 0
        while len(beams):
            print(tick)
            for b in beams:
                if b.out_of_bounds:
                    beams.remove(b)
                    continue

                mark_hit_by_beam(matrix, b)

                b, new_b = b.step(matrix)
                if new_b:
                    beams.append(new_b)

            # print_matrix(matrix, tick)
            tick += 1

        energized = get_num_energized(matrix)
        print("SOLUTION:", energized)

    if part == 2:
        to_right_beams: list[Beam] = []
        to_left_beams: list[Beam] = []
        to_down_beams: list[Beam] = []
        to_up_beams: list[Beam] = []

        for i in range(1, len(matrix) - 1):
            to_right_beams.append(Beam(i, 1, i, 0))
            to_left_beams.append(Beam(i, len(matrix) - 2, i, len(matrix) - 1))
            to_down_beams.append(Beam(1, i, 0, i))
            to_up_beams.append(Beam(len(matrix) - 2, i, len(matrix) - 1, i))

        all_beam_configs = to_right_beams + to_left_beams + to_down_beams + to_up_beams
        max_energized = 0
        for i, starting_beam in enumerate(all_beam_configs, start=1):
            curr_matrix = deepcopy(matrix)
            beams = [starting_beam]

            while len(beams):
                for b in beams:
                    if b.out_of_bounds:
                        beams.remove(b)
                        continue

                    mark_hit_by_beam(curr_matrix, b)

                    b, new_b = b.step(curr_matrix)
                    if new_b:
                        beams.append(new_b)

            energized = get_num_energized(curr_matrix)
            max_energized = max(max_energized, energized)
            print(f"Done Beam config {i}/{len(all_beam_configs)}")
            print("Curr energized:", energized)

        print("SOLUTION:", max_energized)


if __name__ == "__main__":
    main()
