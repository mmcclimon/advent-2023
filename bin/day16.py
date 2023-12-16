from advent import input
from collections import deque


def main():
    grid = {}
    max_r, max_c = 0, 0

    for r, line in enumerate(input.lines()):
        max_r += 1
        max_c = 0
        for c, char in enumerate(line):
            max_c += 1

            if char != ".":
                grid[r, c] = char

    print("part 1:", do_beam(grid, max_r, max_c, (0, 0, "E")))
    print("part 2:", part_two(grid, max_r, max_c))


dirs = {"N": (-1, 0), "E": (0, 1), "S": (1, 0), "W": (0, -1)}


def new_dir(r, c, dir):
    global dirs
    dr, dc = dirs[dir]
    return r + dr, c + dc, dir


def do_beam(grid, max_r, max_c, start):
    todo = deque()
    beam = set()

    todo.append(start)

    while todo:
        r, c, d = todo.popleft()

        if (r, c, d) in beam:
            continue

        if (not 0 <= r < max_r) or (not 0 <= c < max_c):
            continue

        beam.add((r, c, d))

        match grid.get((r, c), ".") + d:
            case r"-N" | r"-S":
                todo.append(new_dir(r, c, "E"))
                todo.append(new_dir(r, c, "W"))
            case r"|E" | r"|W":
                todo.append(new_dir(r, c, "N"))
                todo.append(new_dir(r, c, "S"))
            case r"/N":
                todo.append(new_dir(r, c, "E"))
            case r"/S":
                todo.append(new_dir(r, c, "W"))
            case r"/E":
                todo.append(new_dir(r, c, "N"))
            case r"/W":
                todo.append(new_dir(r, c, "S"))
            case r"\N":
                todo.append(new_dir(r, c, "W"))
            case r"\S":
                todo.append(new_dir(r, c, "E"))
            case r"\E":
                todo.append(new_dir(r, c, "S"))
            case r"\W":
                todo.append(new_dir(r, c, "N"))
            case _:
                todo.append(new_dir(r, c, d))

    energized = {(r, c) for r, c, _ in beam}
    return len(energized)


def part_two(grid, max_r, max_c):
    best = 0
    for r in range(max_r):
        e = do_beam(grid, max_r, max_c, (r, 0, "E"))
        w = do_beam(grid, max_r, max_c, (r, max_c - 1, "W"))
        best = max(e, w, best)

    for c in range(max_c):
        s = do_beam(grid, max_r, max_c, (0, c, "S"))
        n = do_beam(grid, max_r, max_c, (max_r - 1, c, "N"))
        best = max(s, n, best)

    return best


if __name__ == "__main__":
    main()
