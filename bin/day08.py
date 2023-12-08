from advent import input, mathutil
from functools import reduce
import itertools


def main():
    [directions], lines = input.hunks()
    map = {}

    for line in lines:
        key, locs = line.split(" = ")
        l, r = locs[1:-1].split(", ")
        map[key] = (l, r)

    part1 = search(directions, map, "AAA")

    part2 = reduce(
        mathutil.lcm,
        (search(directions, map, node) for node in map if node.endswith("A")),
    )

    print(f"part 1: {part1}")
    print(f"part 2: {part2}")


# Returns length of the path
def search(directions, map, start) -> int:
    moves = 0
    cur = start

    for dir in itertools.cycle(directions):
        moves += 1
        locs = map[cur]
        cur = locs[0] if dir == "L" else locs[1]
        if cur.endswith("Z"):
            return moves

    assert False


if __name__ == "__main__":
    main()
