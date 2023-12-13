from advent import input
from collections import defaultdict


def main():
    p1 = 0
    for hunk in input.hunks():
        p1 += process_hunk(hunk)

    print(f"part 1: {p1}")


def process_hunk(hunk) -> int:
    if rv := compute(hunk):
        return 100 * rv

    cv = compute(rotate(hunk))
    assert cv is not None
    return cv


def compute(hunk) -> int | None:
    rows = defaultdict(list)
    max_r = 0

    for r, row in enumerate(hunk):
        rows[row].append(r)
        max_r = r

    return calc_deltas(list(rows.values()), max_r)


def rotate(hunk):
    """Take a hunk and rotate it such that all columns become rows"""
    grid = [list(line) for line in hunk]
    rotated = [[""] * len(grid) for _ in range(len(grid[0]))]

    for r, line in enumerate(grid):
        for c, char in enumerate(line):
            rotated[c][r] = char

    return ["".join(lst) for lst in rotated]


def calc_deltas(matches, biggest):
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
