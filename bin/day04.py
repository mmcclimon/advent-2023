from advent import input
from collections import Counter


def main():
    scores = calc_scores()

    # part 1
    p1 = sum(2 ** (s - 1) for s in scores.values() if s)

    # part 2
    copies = Counter()

    for card, score in scores.items():
        copies[card] += 1

        for n in range(card + 1, card + score + 1):
            copies[n] += copies[card]

    p2 = copies.total()

    print(f"part 1: {p1}")
    print(f"part 1: {p2}")


def calc_scores():
    scores = {}

    for line in input.lines():
        start, rest = line.split(": ")
        card = int(start.removeprefix("Card "))

        winners, ours = rest.split(" | ")
        winners = {int(n) for n in winners.split()}
        ours = {int(n) for n in ours.split()}

        scores[card] = len(winners.intersection(ours))

    return scores


if __name__ == "__main__":
    main()
