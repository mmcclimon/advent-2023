from advent import input
from collections import defaultdict


def main():
    p1 = 0
    for hunk in input.hunks():
        p1 += process_hunk(hunk)

    print(f"part 1: {p1}")


def process_hunk(hunk) -> int:
    rows = defaultdict(list)
    cols = defaultdict(list)
    max_r, max_c = 0, 0

    for r, row in enumerate(hunk):
        rows[row].append(r)
        max_r = r

    for c in range(len(hunk[0])):
        col = "".join(line[c] for line in hunk)
        cols[col].append(c)
        max_c = c

    rv = compute_deltas(list(rows.values()), max_r)
    cv = compute_deltas(list(cols.values()), max_c)

    if rv:
        return 100 * rv

    assert cv is not None
    return cv


def compute_deltas(matches, biggest):
    lookup = {el: set(lst) - {el} for lst in matches for el in lst}

    for cur in range(0, biggest + 1):
        start = cur
        diff = 1
        while True:
            if cur + diff not in lookup[cur]:
                break

            cur -= 1
            diff += 2

            if cur < 0 or cur + diff > biggest:
                return start + 1


if __name__ == "__main__":
    main()
