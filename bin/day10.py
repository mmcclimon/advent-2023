from advent import input
from enum import Enum


def main():
    grid = Grid()

    for r, line in enumerate(input.lines()):
        for c, char in enumerate(line):
            grid.add(r, c, Pipe(char))

    grid.find_loop()


Dir = Enum("Dir", ["N", "E", "S", "W"])


def opposite_dir(direction):
    return {
        Dir.N: Dir.S,
        Dir.S: Dir.N,
        Dir.E: Dir.W,
        Dir.W: Dir.E,
    }[direction]


class Pipe:
    def __init__(self, char):
        lookup = {
            "|": (Dir.N, Dir.S),
            "-": (Dir.E, Dir.W),
            "L": (Dir.N, Dir.E),
            "J": (Dir.N, Dir.W),
            "7": (Dir.S, Dir.W),
            "F": (Dir.S, Dir.E),
            ".": (),
            "S": (Dir.N, Dir.E, Dir.S, Dir.W),  # I might regret this
        }

        self.char = char
        self.connections = lookup[char]
        self.is_start = char == "S"

    def __repr__(self):
        return f"<Pipe c={self.char}>"


class Grid:
    def __init__(self):
        self.grid = {}
        self.start = None
        self.loop = set()

    def add(self, r, c, pipe):
        self.grid[(r, c)] = pipe
        if pipe.is_start:
            self.start = (r, c)

    def find_loop(self):
        if self.loop:
            return

        # in which I write yet another DFS algo.
        todo = [self.start]

        while todo:
            cur = todo.pop()
            if cur not in self.loop:
                self.loop.add(cur)
                for neighbor in self.neighbors_of(cur):
                    todo.append(neighbor)

        print(len(self.loop) // 2)

    def neighbors_of(self, coords):
        r, c = coords

        neighbors = {
            Dir.N: (r - 1, c),
            Dir.S: (r + 1, c),
            Dir.E: (r, c + 1),
            Dir.W: (r, c - 1),
        }

        ret = []
        for connection in self.grid[coords].connections:
            try:
                nc = neighbors[connection]
                neighbor = self.grid[nc]
                if opposite_dir(connection) in neighbor.connections:
                    ret.append(nc)
            except KeyError:
                pass

        return ret


if __name__ == "__main__":
    main()
