from advent import input
from collections import deque


def main():
    grid = {}
    goal = ()
    for r, line in enumerate(input.lines()):
        for c, char in enumerate(line):
            grid[r, c] = char
            if char == ".":
                goal = (r, c)

    part_one(grid, (0, 1), goal)
    part_two(grid, (0, 1), goal)


def part_one(grid, start, goal):
    # dfs with path memory
    todo = deque()

    todo.append([start, [], set()])

    longest = 0

    while todo:
        cur, path, seen = todo.pop()

        path.append(cur)
        seen.add(cur)

        if cur == goal:
            length = len(path) - 1
            longest = max(length, longest)
            continue

        n = [pos for pos in neighbors(grid, cur) if pos not in seen]

        for neighbor in n:
            todo.append([neighbor, path.copy(), seen.copy()])

    print(f"part 1: {longest}")


def part_two(grid, start, goal):
    # dfs with path memory
    todo = deque()

    todo.append([start, [], set()])

    longest = 0

    while todo:
        cur, path, seen = todo.pop()

        path.append(cur)
        seen.add(cur)

        if cur == goal:
            length = len(path) - 1
            print(length)
            longest = max(length, longest)
            continue

        n = [pos for pos in neighbors2(grid, cur) if pos not in seen]

        for neighbor in n:
            todo.append([neighbor, path.copy(), seen.copy()])

    print(f"part 2: {longest}")


def neighbors(grid, cur):
    r, c = cur

    match grid[r, c]:
        case '^':
            return [(r-1, c)]
        case 'v':
            return [(r+1, c)]
        case '<':
            return [(r, c-1)]
        case '>':
            return [(r, c+1)]
        case _:
            # fall through
            pass

    neighbors = []
    for rc in [(r+1, c), (r-1, c), (r, c+1), (r, c-1)]:
        char = grid.get(rc, '#')
        if char not in '.^v<>':
            continue

        if rc == (r+1, c) and char == '^':
            continue
        if rc == (r-1, c) and char == 'v':
            continue
        if rc == (r, c-1) and char == '>':
            continue
        if rc == (r, c+1) and char == '<':
            continue

        neighbors.append(rc)

    # print(neighbors)
    return neighbors


def neighbors2(grid, cur):
    r, c = cur

    return [
        rc
        for rc in [(r+1, c), (r-1, c), (r, c+1), (r, c-1)]
        if grid.get(rc, '#') in '.^v<>'
    ]


if __name__ == '__main__':
    main()
