from advent import input
from collections import deque


def mprint(*args):
    return
    print(*args)


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


def do_beam(grid, max_r, max_c, start):
    todo = deque()
    beam = set()

    todo.append(start)

    while todo:
        r, c, d = todo.popleft()
        mprint(f"considering {r, c, d}")

        if (r, c, d) in beam:
            mprint("  seen")
            continue

        if (not 0 <= r < max_r) or (not 0 <= c < max_c):
            mprint("  out of the grid")
            continue

        beam.add((r, c, d))

        match grid.get((r, c), ".") + d:
            case r"-N" | r"-S":
                todo.append(new_dir(r, c, "E"))
                todo.append(new_dir(r, c, "W"))
                mprint(f"  -, added {todo[-2]} and {todo[-1]}")
            case r"|E" | r"|W":
                todo.append(new_dir(r, c, "N"))
                todo.append(new_dir(r, c, "S"))
                mprint(f"  |, added {todo[-2]} and {todo[-1]}")
            case r"/N":
                todo.append(new_dir(r, c, "E"))
                mprint(f"  /, added {todo[-1]}")
            case r"/S":
                todo.append(new_dir(r, c, "W"))
                mprint(f"  /, added {todo[-1]}")
            case r"/E":
                todo.append(new_dir(r, c, "N"))
                mprint(f"  /, added {todo[-1]}")
            case r"/W":
                todo.append(new_dir(r, c, "S"))
                mprint(f"  /, added {todo[-1]}")
            case r"\N":
                todo.append(new_dir(r, c, "W"))
                mprint(f"  \\, added {todo[-1]}")
            case r"\S":
                todo.append(new_dir(r, c, "E"))
                mprint(f"  \\, added {todo[-1]}")
            case r"\E":
                todo.append(new_dir(r, c, "S"))
                mprint(f"  \\, added {todo[-1]}")
            case r"\W":
                todo.append(new_dir(r, c, "N"))
                mprint(f"  \\, added {todo[-1]}")
            case _:
                # empty space, yo
                # dr, dc = dirs[d]
                todo.append((new_dir(r, c, d)))
                char = grid.get((r, c), ".")
                mprint(f"  {char}, added {todo[-1]}")

    mprint("done?", beam)

    energized = {(r, c) for r, c, _ in beam}
    return len(energized)


dirs = {"N": (-1, 0), "E": (0, 1), "S": (1, 0), "W": (0, -1)}


def new_dir(r, c, dir):
    global dirs
    dr, dc = dirs[dir]
    return r + dr, c + dc, dir


if __name__ == "__main__":
    main()
