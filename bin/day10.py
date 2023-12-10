from advent import input
from enum import Enum


def main():
    grid = Grid()

    for r, line in enumerate(input.lines()):
        for c, char in enumerate(line):
            grid.add(r, c, Pipe(char))

    print("part 1:", grid.find_loop() // 2)
    print("part 2:", grid.num_inside_squares())


class Dir(Enum):
    N = "N"
    E = "E"
    S = "S"
    W = "W"

    def opposite(self):
        return {
            Dir.N: Dir.S,
            Dir.S: Dir.N,
            Dir.E: Dir.W,
            Dir.W: Dir.E,
        }[self]

    def rowcol(self, r, c):
        return {
            Dir.N: (r - 1, c),
            Dir.S: (r + 1, c),
            Dir.E: (r, c + 1),
            Dir.W: (r, c - 1),
        }[self]


class Pipe:
    def __init__(self, char):
        lookup = {
            "|": (Dir.N, Dir.S),
            "-": (Dir.E, Dir.W),
            "L": (Dir.N, Dir.E),
            "J": (Dir.N, Dir.W),
            "7": (Dir.S, Dir.W),
            "F": (Dir.S, Dir.E),
            "S": (Dir.N, Dir.E, Dir.S, Dir.W),
        }

        self.char = char
        self.connections = lookup.get(char, ())
        self.is_start = char == "S"

    def __repr__(self):
        return f"<Pipe c={self.char}>"


class Grid:
    def __init__(self):
        self.grid = {}
        self.start = None
        self.loop = set()
        self.outside = set()

    def __str__(self):
        self.find_loop()

        rows = []
        for r in range(self.min_r, self.max_r + 1):
            row = []
            for c in range(self.min_c, self.max_c + 1):
                pipe = self.grid[(r, c)]
                char = "."
                if (r, c) in self.loop:
                    char = pipe.char
                elif (r, c) in self.outside:
                    char = "O"
                elif pipe.char != ".":
                    char = "?"

                row.append(char)

            rows.append("".join(row))

        return "\n".join(rows)

    @property
    def min_r(self):
        return min(r for r, _ in self.grid)

    @property
    def max_r(self):
        return max(r for r, _ in self.grid)

    @property
    def min_c(self):
        return min(c for _, c in self.grid)

    @property
    def max_c(self):
        return max(c for _, c in self.grid)

    def add(self, r, c, pipe):
        self.grid[(r, c)] = pipe
        if pipe.is_start:
            self.start = (r, c)

    def find_loop(self):
        if self.loop:
            return len(self.loop)

        # in which I write yet another DFS algo.
        todo = [self.start]

        while todo:
            cur = todo.pop()
            if cur not in self.loop:
                self.loop.add(cur)
                todo.extend(self.neighbors_of(cur))

        return len(self.loop)

    def neighbors_of(self, coords):
        r, c = coords

        ret = []
        for connection in self.grid[coords].connections:
            try:
                other = connection.rowcol(r, c)
                if connection.opposite() in self.grid[other].connections:
                    ret.append(other)
            except KeyError:
                pass

        return ret

    def num_inside_squares(self):
        # Ok, the plan is: expand the grid to double-size (so that all the
        # spaces between pipes become real tiles), then do a flood-fill DFS
        # starting on all outside tiles. Then, all we need to do is
        # re-contract the grid (by walking it two at a time), counting up the
        # tiles that aren't in the loop or in the set of outside tiles.
        big = self._expand()
        big._find_exits()

        total = 0

        for r in range(0, big.max_r, 2):
            for c in range(0, big.max_c, 2):
                coords = (r, c)
                if coords in big.loop or coords in big.outside:
                    continue

                total += 1

        return total

    # Zoom in! Enhance!
    def _expand(self):
        self.find_loop()

        # Each tile in the original generates 4 tiles in the expansion:
        # self, right, down, down-right
        big = Grid()
        for r in range(0, self.max_r + 1):
            for c in range(0, self.max_c + 1):
                r2, c2 = r * 2, c * 2

                # down-right tile is never interesting
                big.add(r2 + 1, c2 + 1, Pipe("."))

                if (r, c) not in self.loop:
                    big.add(r2, c2, Pipe("."))
                    big.add(r2 + 1, c2, Pipe("."))
                    big.add(r2, c2 + 1, Pipe("."))
                    continue

                # In the loop: top left is just our tile.
                big.add(r2, c2, self.grid[(r, c)])

                rxy = (r, c + 1)
                right = Pipe("-") if rxy in self.neighbors_of((r, c)) else Pipe(".")
                big.add(r2, c2 + 1, right)

                dxy = (r + 1, c)
                down = Pipe("|") if dxy in self.neighbors_of((r, c)) else Pipe(".")
                big.add(r2 + 1, c2, down)

        # Add an extra row on top and left, to make sure that we have a full
        # perimeter. (The expansion ensures we have one bottom/right already.)
        big.add(-1, -1, Pipe("."))

        for r in range(0, big.max_r + 1):
            big.add(r, -1, Pipe("."))

        for c in range(0, big.max_c + 1):
            big.add(-1, c, Pipe("."))

        return big

    # Do a DFS starting at a tile known to be outside. At the end of this
    # method, self.outside is filled with all such tiles.
    def _find_exits(self):
        self.find_loop()

        def relevant(r, c):
            return [
                coord
                for coord in [(r - 1, c), (r + 1, c), (r, c + 1), (r, c - 1)]
                if coord in self.grid and self.grid[coord].char == "."
            ]

        # I could reuse this algorithm, but also.
        todo = [(-1, -1)]

        while todo:
            cur = todo.pop()

            if cur not in self.outside:
                self.outside.add(cur)
                todo.extend(coord for coord in relevant(*cur))

        return


if __name__ == "__main__":
    main()
