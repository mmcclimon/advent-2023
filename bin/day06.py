from advent import input
from functools import reduce
import operator


def main():
    lines = list(input.lines())

    part_one(lines)
    part_two(lines)


def part_one(lines):
    times = [int(n) for n in lines[0].removeprefix("Time:").split()]
    dists = [int(n) for n in lines[1].removeprefix("Distance:").split()]
    total = []

    for i in range(len(times)):
        time, d = times[i], dists[i]
        total.append(do_race(time, d))

    print(reduce(operator.mul, total))


def part_two(lines):
    time = int(lines[0].removeprefix("Time:").replace(" ", ""))
    dist = int(lines[1].removeprefix("Distance:").replace(" ", ""))

    print(do_race(time, dist))


# returns number of wins
def do_race(time, record) -> int:
    wins = 0
    for t in range(1, time):
        dist = (time - t) * t
        if dist > record:
            wins += 1

    return wins


if __name__ == "__main__":
    main()
