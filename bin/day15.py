from advent import input
from collections import defaultdict


def main():
    [line] = input.lines()

    p1 = sum(hash(bit) for bit in line.split(","))
    print(p1)

    # part 2
    h = defaultdict(dict)

    for bit in line.split(","):
        if bit[-1] == "-":
            label = bit[:-1]
            k = hash(label)
            if label in h[k]:
                del h[k][label]
        else:
            label, val = bit.split("=")
            k = hash(label)
            h[k][label] = val

    p2 = sum(
        (k + 1) * (i + 1) * int(val)
        for k, d in h.items()
        for i, val in enumerate(d.values())
    )
    print(p2)


def hash(s):
    cur = 0
    for c in s:
        cur = ((cur + ord(c)) * 17) % 256

    return cur


if __name__ == "__main__":
    main()
