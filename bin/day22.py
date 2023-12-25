from advent import input
from collections import namedtuple
from functools import reduce


def main():
    pieces = set()
    for line in input.lines():
        p = Piece(line)
        pieces.add(p)

    def by_z(piece):
        return piece.min_z()

    grid = Grid()

    for p in sorted(pieces, key=by_z):
        print("will attempt to drop", p)
        p.drop(grid)

    for p in grid.pieces:
        print(p, grid.pieces[p])

    disintegrate(grid)


def disintegrate(grid):
    total = 0
    for candidate in grid.pieces:
        can_remove = True
        print(f"checking for {candidate} ({grid.pieces[candidate]})")

        for other, supported_by in grid.pieces.items():
            if other == candidate:
                continue

            if len(supported_by) == 1 and candidate in supported_by:
                print(f"  nope only thing supporting {other}")
                can_remove = False
                break

        if can_remove:
            total += 1

    print(total)


Cube = namedtuple("Cube", ["x", "y", "z"])


class Piece:
    def __init__(self, line):
        start, end = line.split("~")
        self.text = line.replace("~", "|")
        sx, sy, sz = (int(n) for n in start.split(","))
        ex, ey, ez = (int(n) for n in end.split(","))

        self.cubes = set()

        if sx != ex:
            assert sy == ey
            assert sz == ez
            for x in range(sx, ex + 1):
                self.cubes.add(Cube(x, sy, sz))

        elif sy != ey:
            assert sx == ex
            assert sz == ez
            for y in range(sy, ey + 1):
                self.cubes.add(Cube(sx, y, sz))

        elif sz != ez:
            assert sx == ex
            assert sy == ey
            for z in range(sz, ez + 1):
                self.cubes.add(Cube(sx, sy, z))

        elif start == end:
            self.cubes.add(Cube(sx, sy, sz))

    def __repr__(self):
        return f"<P {self.text}>"

    def min_z(self):
        return min(z for _, _, z in self.cubes)

    def drop(self, onto):
        # for every cube:
        #   try to subtract z - 1
        #   if it hits 0, stop.
        #   if it hits something else, stop.
        while True:
            repl = set()

            for cube in self.cubes:
                c2 = Cube(cube.x, cube.y, cube.z - 1)

                if c2.z == 0:
                    onto.add(self)
                    return

                if c2 in onto:
                    onto.add(self)
                    return

                repl.add(c2)

            print(self, "drop 1.")
            self.cubes = repl
            onto.add(self)


class Grid:
    def __init__(self):
        self.pieces = {}
        self.cubes = set()

    def __contains__(self, cube):
        # print(self.cubes)
        return cube in self.cubes

    def _update_cubes(self):
        self.cubes = reduce(lambda acc, el: acc.union(el.cubes), self.pieces, set())

    def add(self, piece):
        self.pieces[piece] = set()

        # obviously stupid.
        for cube in piece.cubes:
            x, y, z = cube
            below = (x, y, z - 1)
            if below in self.cubes:
                for other in self.pieces:
                    if other == piece:
                        continue

                    if below in other.cubes:
                        self.pieces[piece].add(other)

        # print("ADD:", piece, piece.cubes)
        self._update_cubes()

    def remove(self, piece):
        self.pieces.pop(piece, None)
        # print("ADD:", piece, piece.cubes)
        self._update_cubes()


if __name__ == "__main__":
    main()
