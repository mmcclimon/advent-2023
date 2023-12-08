from advent import input, mathutil
from collections import namedtuple
from functools import reduce
import itertools


def main():
    [directions], lines = input.hunks()
    map = {}

    for line in lines:
        key, locs = line.split(" = ")
        l, r = locs[1:-1].split(", ")
        map[key] = (l, r)

    legend = namedtuple('Legend', ["directions", "map"])(directions, map)

    part_one(legend)
    part_two(legend)


def part_one(legend):
    moves = search(legend, "AAA", lambda n: n == "ZZZ")
    print(f"part 1: {moves}")


def part_two(legend):
    starts = [node for node in legend.map if node.endswith("A")]
    zs = [search(legend, node, lambda n: n.endswith("Z")) for node in starts]

    print(f"part 2: {reduce(mathutil.lcm, zs)}")


# Returns length of the path
def search(legend, start, pred) -> int:
    moves = 0
    cur = start

    for dir in itertools.cycle(legend.directions):
        moves += 1
        locs = legend.map[cur]
        cur = locs[0] if dir == "L" else locs[1]
        if pred(cur):
            return moves

    assert False


if __name__ == "__main__":
    main()
