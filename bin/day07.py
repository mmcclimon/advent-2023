from advent import input
from collections import Counter
from enum import IntEnum


def main():
    sum = 0
    for i, hand in enumerate(sorted(Hand(line) for line in input.lines())):
        sum += hand.bid * (i + 1)

    print(sum)


class Rank(IntEnum):
    HIGH = 1
    PAIR = 2
    TWO_PAIR = 3
    THREE = 4
    FULL = 5
    FOUR = 6
    FIVE = 7


class Hand:
    Values = {str(i): i for i in range(2, 10)} | {
        "T": 10,
        "J": 11,
        "Q": 12,
        "K": 13,
        "A": 14,
    }

    def __init__(self, line):
        hand, bid = line.split()
        self.hand = hand
        self.bid = int(bid)

    def __repr__(self):
        return f"<Hand hand={self.hand} bid={self.bid}, rank={self.rank()}>"

    def __lt__(self, other):
        me, them = self.rank(), other.rank()
        if me == them:
            for i in range(5):
                if self.hand[i] == other.hand[i]:
                    continue

                return self.Values[self.hand[i]] < self.Values[other.hand[i]]

        return me < them

    def rank(self) -> Rank:
        counts = list(Counter(self.hand).values())

        if 5 in counts:
            return Rank.FIVE
        elif 4 in counts:
            return Rank.FOUR
        elif 3 in counts:
            return Rank.FULL if 2 in counts else Rank.THREE
        elif 2 in counts:
            return Rank.TWO_PAIR if Counter(counts)[2] == 2 else Rank.PAIR
        else:
            return Rank.HIGH


if __name__ == "__main__":
    main()
