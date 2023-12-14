from advent import input
import itertools


def main():
    lines = list(input.lines())
    p1 = Grid(lines)
    p1.tilt("N")
    print("part 1:", p1.total_load())


class Grid:
    def __init__(self, lines):
        self.n_rows = 0
        self.n_cols = 0
        self._grid = {}

        for r, line in enumerate(lines):
            self.n_rows += 1
            self.n_cols = 0
            for c, char in enumerate(line):
                self[r, c] = char
                self.n_cols += 1

    def __getitem__(self, idx):
        return self._grid[idx]

    def __setitem__(self, idx, val):
        self._grid[idx] = val

    def print(self):
        for r in range(self.n_rows):
            line = []
            for c in range(self.n_cols):
                line.append(self[r, c])

            print("".join(line))

    def total_load(self):
        return sum(
            self.n_rows - r
            for r in range(self.n_rows)
            for c in range(self.n_cols)
            if self[r, c] == "O"
        )

    def tilt(self, dir):
        def _next(coords):
            r, c = coords
            return {
                "N": (r - 1, c),
                "S": (r + 1, c),
                "E": (r, c + 1),
                "W": (r, c - 1),
            }[dir]

        # we must iterate in reverse order if tilting south or east
        wrap = reversed if dir in "SE" else itertools.chain

        for cur, char in wrap(self._grid.items()):
            if char != "O":
                continue

            nxt = _next(cur)
            while nxt in self._grid:
                if self[nxt] != ".":
                    break

                self[nxt] = "O"
                self[cur] = "."
                cur, nxt = nxt, _next(nxt)


if __name__ == "__main__":
    main()
