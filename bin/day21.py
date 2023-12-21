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


def part_one(grid, start, n_steps):
    todo = [start]

    for n in range(n_steps):
        # print("STEP", n + 1)
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


if __name__ == "__main__":
    main()
