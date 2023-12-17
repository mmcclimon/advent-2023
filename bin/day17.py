from advent import input
import heapq


def main():
    grid = {}
    for r, line in enumerate(input.lines()):
        for c, char in enumerate(line):
            grid[r, c] = int(char)

    print("part 1:", go(grid, 1, 3))
    print("part 2:", go(grid, 4, 10))


def go(grid, min_steps, max_steps):
    start = (0, 0)
    end = max(grid)

    todo = [(0, start, (0, 0))]
    seen = set()

    while todo:
        heat, pos, prev_dir = heapq.heappop(todo)
        if (pos, prev_dir) in seen:
            continue

        seen.add((pos, prev_dir))

        if pos == end:
            return heat

        for dir in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
            dr, dc = dir

            # Don't go in the same direction we just went (the loop below
            # takes care of that), and don't go backwards.
            if (dr, dc) == prev_dir or (-dr, -dc) == prev_dir:
                continue

            h = heat
            r, c = pos

            for i in range(1, max_steps + 1):
                next_pos = (dr * i + r, dc * i + c)
                if next_pos in grid:
                    h += grid[next_pos]
                    if i >= min_steps:
                        heapq.heappush(todo, (h, next_pos, dir))


if __name__ == "__main__":
    main()
