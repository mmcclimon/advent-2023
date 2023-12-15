from advent import input, ds
from collections import defaultdict, namedtuple


def main():
    [line] = input.lines()
    bits = line.split(",")

    p1 = sum(hash(bit) for bit in bits)
    print(f"part 1: {p1}")

    p2 = part_two_normal(bits)
    print(f"part 2: {p2}")

    ok = part_two_overkill(bits)
    print(f"part 2: {ok} (but with no dicts)")


def hash(s):
    cur = 0
    for c in s:
        cur = ((cur + ord(c)) * 17) % 256

    return cur


def part_two_normal(bits):
    # Just use a dict of dicts; they remember their insertion order, which we
    # need anyway.
    h = defaultdict(dict)

    for bit in bits:
        if bit[-1] == "-":
            label = bit[:-1]
            k = hash(label)
            if label in h[k]:
                del h[k][label]
        else:
            label, val = bit.split("=")
            k = hash(label)
            h[k][label] = val

    return sum(
        (k + 1) * (i + 1) * int(val)
        for k, d in h.items()
        for i, val in enumerate(d.values())
    )


def part_two_overkill(bits):
    hm = [ds.LinkedList() for _ in range(256)]

    Lens = namedtuple("Lens", ["label", "focallen"])

    for bit in bits:
        if bit[-1] == "-":
            label = bit[:-1]
            ll = hm[hash(label)]
            for node in ll:
                if node.data.label == label:
                    ll.remove(node)

            continue

        label, focallen = bit.split("=")
        lens = Lens(label, int(focallen))

        ll = hm[hash(label)]
        found = False

        for node in ll:
            if node.data.label == label:
                node.data = lens
                found = True
                break

        if not found:
            ll.append(lens)

    return sum(
        (k + 1) * (i + 1) * node.data.focallen
        for k, ll in enumerate(hm)
        for i, node in enumerate(ll)
    )


if __name__ == "__main__":
    main()
