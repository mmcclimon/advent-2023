from advent import input
from collections import defaultdict


def main():
    sum1 = 0
    sum2 = 0

    for line in input.lines():
        id, r, g, b = parse(line)
        sum2 += r * g * b

        if r <= 12 and g <= 13 and b <= 14:
            sum1 += id

    print(f"part 1: {sum1}")
    print(f"part 2: {sum2}")


def parse(line):
    start, rest = line.split(": ")

    found = defaultdict(int)

    for hunk in rest.split("; "):
        for marbles in hunk.split(", "):
            num, color = marbles.split()
            num = int(num)
            found[color] = max(found[color], num)

    id = start.removeprefix("Game ")
    return int(id), found["red"], found["green"], found["blue"]


if __name__ == "__main__":
    main()
