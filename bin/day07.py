from advent import input
from collections import Counter
from enum import IntEnum
import functools


def main():
    lines = list(input.lines())

    sum = 0
    for i, hand in enumerate(sorted(Hand(line) for line in lines)):
        sum += hand.bid * (i + 1)

    print(f"part 1: {sum}")

    sum2 = 0
    for i, hand in enumerate(sorted(WildHand(line) for line in lines)):
        sum2 += hand.bid * (i + 1)

    print(f"part 2: {sum2}")


class Rank(IntEnum):
    HIGH = 1
    PAIR = 2
    TWO_PAIR = 3
    THREE = 4
    FULL = 5
    FOUR = 6
    FIVE = 7

    @classmethod
    def for_hand(cls, counts):
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
        return f"<Hand hand={self.hand} bid={self.bid}, rank={self.rank}>"

    def __lt__(self, other):
        me, them = self.rank, other.rank
        if me == them:
            for i in range(5):
                if self.hand[i] == other.hand[i]:
                    continue

                return self.value_for(self.hand[i]) < self.value_for(other.hand[i])

        return me < them

    @functools.cached_property
    def rank(self) -> Rank:
        return Rank.for_hand(Counter(self.hand).values())

    def value_for(self, val):
        return self.Values[val]


class WildHand(Hand):
    @functools.cached_property
    def rank(self) -> Rank:
        counts = Counter(self.hand)
        jokers = counts.pop("J", 0)

        if not jokers or jokers == 5:
            return super().rank

        # Add the jokers to whatever the most cards we have is
        vals = sorted(counts.values(), reverse=True)
        vals[0] += jokers
        return Rank.for_hand(vals)

    def value_for(self, val):
        return 1 if val == "J" else self.Values[val]


if __name__ == "__main__":
    main()
