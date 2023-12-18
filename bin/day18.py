from advent import input


def main():
    lines = []

    for line in input.lines():
        dir, n, color = line.split()
        lines.append((dir, int(n), color))

    grid = make_grid(lines)
    print(fill_grid(grid, (1, 1)))


def make_grid(lines):
    grid = set()
    grid.add((0, 0))

    dirs = {"U": (-1, 0), "D": (1, 0), "R": (0, 1), "L": (0, -1)}

    pos = (0, 0)

    for line in lines:
        dir, n, _ = line
        dr, dc = dirs[dir]
        for i in range(n):
            pos = (pos[0] + dr, pos[1] + dc)
            grid.add(pos)

    return grid


def fill_grid(grid, start):
    todo = [start]

    def neighbors(r, c):
        ret = []
        for dr, dc in [(-1, 0), (1, 0), (0, 1), (0, -1)]:
            if (r + dr, c + dc) not in grid:
                ret.append((r + dr, c + dc))

        return ret

    while todo:
        cur = todo.pop()
        if cur not in grid:
            grid.add(cur)
            todo.extend(neighbors(*cur))

    return len(grid)


def pg(grid):
    rs = [r for r, _ in grid]
    cs = [c for _, c in grid]

    for r in range(min(rs), max(rs) + 1):
        for c in range(min(cs), max(cs) + 1):
            if (r, c) == (0, 0):
                print("S", end="")
            elif (r, c) in grid:
                print("#", end="")
            else:
                print(".", end="")
        print("")


if __name__ == "__main__":
    main()
