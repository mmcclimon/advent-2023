from advent import input


def main():
    grid = {}
    start = None
    for r, line in enumerate(input.lines()):
        for c, char in enumerate(line):
            if char == "S":
                start = (r, c)
                char = "."

            grid[r, c] = char

    print("part 1:", part_one(grid, start, 64))

    # Ugh. Part 2 requires fitting to a quadratic. This requires a) realizing
    # the special shape of the input; b) math I do not know. This is...not my
    # favorite kind of advent problem. (Solution cribbed from the reddit.)

    steps = 26501365
    width = 131

    print("part 2:")

    v1 = part_two(grid, start, 65)
    print("  n=1", v1)

    v2 = part_two(grid, start, 65 + width)
    print("  n=2", v2)

    v3 = part_two(grid, start, 65 + width * 2)
    print("  n=3", v3)

    a = (v1 - 2 * v2 + v3) // 2
    b = (-3 * v1 + 4 * v2 - v3) // 2
    c = v1
    n = steps // 131

    print(f"  quadratic: {a}n^2 + {b}n + {c}, {n=}")
    print("part 2:", (a * n * n) + (b * n) + c)


def part_one(grid, start, n_steps):
    todo = [start]

    for n in range(n_steps):
        next_round = set()

        while todo:
            cur = todo.pop()
            for pos in neighbors(grid, *cur):
                next_round.add(pos)

        todo = list(next_round)

    return len(todo)


def neighbors(grid, r, c):
    return [
        rc
        for rc in [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]
        if grid.get(rc, "#") == "."
    ]


def part_two(grid, start, n_steps):
    todo = [start]
    len_r = 1 + max(r for r, _ in grid)
    len_c = 1 + max(c for _, c in grid)

    for n in range(n_steps):
        next_round = set()

        while todo:
            cur = todo.pop()
            for pos in neighbors_two(grid, (len_r, len_c), *cur):
                next_round.add(pos)

        todo = list(next_round)

    return len(todo)


def neighbors_two(grid, lens, r, c):
    for rc in [(r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)]:
        r2, c2 = rc
        r2 %= lens[0]
        c2 %= lens[1]

        if grid[r2, c2] != "#":
            yield rc


if __name__ == "__main__":
    main()
