from advent import input
from collections import deque


def main():
    grid = {}

    for r, line in enumerate(input.lines()):
        for c, char in enumerate(line):
            grid[r, c] = char

    print("part 1:", do_beam(grid, (0, 0, "E")))
    print("part 2:", part_two(grid))


def step(r, c, dir):
    return {
        "N": (r - 1, c, dir),
        "E": (r, c + 1, dir),
        "S": (r + 1, c, dir),
        "W": (r, c - 1, dir),
    }[dir]


def do_beam(grid, start):
    todo = deque()
    beam = set()

    todo.append(start)

    while todo:
        r, c, d = todo.popleft()

        if (r, c, d) in beam or (r, c) not in grid:
            continue

        beam.add((r, c, d))

        match grid[r, c] + d:
            case r"-N" | r"-S":
                todo.append(step(r, c, "E"))
                todo.append(step(r, c, "W"))
            case r"|E" | r"|W":
                todo.append(step(r, c, "N"))
                todo.append(step(r, c, "S"))
            case r"/N":
                todo.append(step(r, c, "E"))
            case r"/S":
                todo.append(step(r, c, "W"))
            case r"/E":
                todo.append(step(r, c, "N"))
            case r"/W":
                todo.append(step(r, c, "S"))
            case r"\N":
                todo.append(step(r, c, "W"))
            case r"\S":
                todo.append(step(r, c, "E"))
            case r"\E":
                todo.append(step(r, c, "S"))
            case r"\W":
                todo.append(step(r, c, "N"))
            case _:
                todo.append(step(r, c, d))

    energized = {(r, c) for r, c, _ in beam}
    return len(energized)


def part_two(grid):
    best = 0
    rows = 1 + max(r for r, _ in grid)
    cols = 1 + max(c for _, c in grid)

    for r in range(rows):
        e = do_beam(grid, (r, 0, "E"))
        w = do_beam(grid, (r, cols - 1, "W"))
        best = max(e, w, best)

    for c in range(cols):
        s = do_beam(grid, (0, c, "S"))
        n = do_beam(grid, (rows - 1, c, "N"))
        best = max(s, n, best)

    return best


if __name__ == "__main__":
    main()
