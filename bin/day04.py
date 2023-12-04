from advent import input
from collections import Counter


def main():
    lines = list(input.lines())
    print(part_one(lines))
    print(part_two(lines))


def part_one(lines):
    sum = 0

    for line in lines:
        card, rest = line.split(": ")
        if score := calc_score(rest):
            sum += 2 ** (score - 1)

    return sum


def part_two(lines):
    copies = Counter()

    for line in lines:
        start, rest = line.split(": ")
        card = int(start.removeprefix("Card "))
        copies[card] += 1

        score = calc_score(rest)

        for n in range(card + 1, card + score + 1):
            copies[n] += copies[card]

    return copies.total()


def calc_score(nums):
    winners, ours = nums.split(" | ")
    winners = {int(n) for n in winners.split()}
    ours = {int(n) for n in ours.split()}

    return len(winners.intersection(ours))


if __name__ == "__main__":
    main()
