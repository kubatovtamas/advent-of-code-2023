import sys
from dataclasses import dataclass
from enum import Enum
from functools import cached_property
from pathlib import Path
from typing import Iterator, Self


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


@dataclass
class Tile:
    ch: str
    idx: tuple[int, int]


class Dir(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


class Maze:
    def __init__(self, rows: list[list[Tile]], s: Tile) -> None:
        self.rows = rows
        self.s = s

    def __getitem__(self, row: int) -> list[Tile]:
        return self.rows[row]

    def __iter__(self) -> Iterator[list[Tile]]:
        for row in self.rows:
            yield row

    def get_tile(self, row: int, col: int) -> Tile:
        return self[row][col]

    def print(self):
        for row in self.rows:
            print(" ".join(tile.ch for tile in row))

    @cached_property
    def start_tiles(self) -> list[tuple[Tile, Dir]]:
        up = self.get_tile(self.s.idx[0] - 1, self.s.idx[1])
        right = self.get_tile(self.s.idx[0], self.s.idx[1] + 1)
        down = self.get_tile(self.s.idx[0] + 1, self.s.idx[1])
        left = self.get_tile(self.s.idx[0], self.s.idx[1] - 1)

        starting_tiles: list[tuple[Tile, Dir]] = []
        if up.ch in ("|", "7", "F"):
            starting_tiles.append((up, Dir.DOWN))
        if right.ch in ("-", "J", "7"):
            starting_tiles.append((right, Dir.LEFT))
        if down.ch in ("|", "J", "L"):
            starting_tiles.append((down, Dir.UP))
        if left.ch in ("-", "L", "F"):
            starting_tiles.append((left, Dir.RIGHT))

        assert len(starting_tiles) == 2

        return starting_tiles

    @classmethod
    def create_game_maze(cls, fname: str) -> Self:
        rows: list[list[Tile]] = []
        start_idxs = (-1, -1)

        for idx_row, line in enumerate(read_input(fname)):
            # First line padding
            if idx_row == 0:
                padding_line = ["."] * (len(line) + 2)
                padding_row = [
                    Tile(ch, (idx_row, idx_col))
                    for idx_col, ch in enumerate(padding_line)
                ]
                rows.append(padding_row)

            # First and last col padding
            padded_line = "." + line + "."

            row: list[Tile] = []
            for idx_col, ch in enumerate(padded_line):
                if ch == "S":
                    start_idxs = (idx_row + 1, idx_col)
                row.append(Tile(ch, (idx_row + 1, idx_col)))

            rows.append(row)

        # Last line padding
        rows.append(rows[0].copy())

        s = rows[start_idxs[0]][start_idxs[1]]
        return Maze(rows, s)


class TilePointer:
    dir_map = {
        "|": ((1, 0, Dir.UP), (), (-1, 0, Dir.DOWN), ()),
        "-": ((), (0, -1, Dir.RIGHT), (), (0, 1, Dir.LEFT)),
        "L": ((0, 1, Dir.LEFT), (-1, 0, Dir.DOWN), (), ()),
        "J": ((0, -1, Dir.RIGHT), (), (), (-1, 0, Dir.DOWN)),
        "7": ((), (), (0, -1, Dir.RIGHT), (1, 0, Dir.UP)),
        "F": ((), (1, 0, Dir.UP), (0, 1, Dir.LEFT), ()),
    }

    def __init__(self, maze: Maze, tile: Tile, dist: int, came_from: Dir) -> None:
        self.maze = maze
        self.tile = tile
        self.dist = dist
        self.came_from = came_from

    def __repr__(self) -> str:
        return f"TilePointer({self.tile}, dist={self.dist}, came_from={self.came_from})"

    def step(self) -> None:
        next_info = self.dir_map[self.tile.ch][self.came_from.value]
        assert len(next_info) == 3

        row_delta, col_delta, new_came_from = next_info
        new_row_idx = self.tile.idx[0] + row_delta
        new_col_idx = self.tile.idx[1] + col_delta

        self.tile = self.maze.get_tile(new_row_idx, new_col_idx)
        self.dist += 1
        self.came_from = new_came_from


def calculate_area(vertices: list[tuple[int, int]]) -> int:
    n = len(vertices)
    area = 0

    for i in range(n):
        x1, y1 = vertices[i]
        x2, y2 = vertices[(i + 1) % n]
        area += (x1 * y2) - (y1 * x2)

    area = abs(area) / 2
    return int(area)


def main():
    part, fname = get_args()

    if part == 1:
        maze = Maze.create_game_maze(fname)

        pointers = [TilePointer(maze, tile, 1, dir) for tile, dir in maze.start_tiles]
        p1 = pointers[0]
        p2 = pointers[1]

        max_dist = 0
        while p1.tile.idx != p2.tile.idx:
            max_dist = max(max_dist, p1.dist, p2.dist)
            p1.step()
            p2.step()

        print("SOLUTION:", max_dist + 1)

    if part == 2:
        maze = Maze.create_game_maze(fname)

        p = [TilePointer(maze, tile, 1, dir) for tile, dir in maze.start_tiles][0]

        num_boundary_pts = 1
        corner_pts: list[tuple[int, int]] = []
        corner_pts.append(maze.s.idx)

        while p.tile.ch != "S":
            num_boundary_pts += 1

            if p.tile.ch in list("FJL7"):
                corner_pts.append(p.tile.idx)

            p.step()

        area = calculate_area(corner_pts)
        num_inside_pts = int(area + 1 - (num_boundary_pts / 2))

        print("SOLUTION:", num_inside_pts)


if __name__ == "__main__":
    main()
