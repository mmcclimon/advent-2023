from advent import input
import itertools


def main():
    galaxies = [
        (r, c)
        for r, line in enumerate(input.lines())
        for c, char in enumerate(line)
        if char == "#"
    ]

    rows = {r for r, _ in galaxies}
    cols = {c for _, c in galaxies}

    empty_rows = {r for r in range(0, max(rows) + 1) if r not in rows}
    empty_cols = {c for c in range(0, max(cols) + 1) if c not in cols}

    print("part 1:", compute(galaxies, empty_rows, empty_cols, 2))
    print("part 2:", compute(galaxies, empty_rows, empty_cols, 1_000_000))


def compute(galaxies, empty_rows, empty_cols, scale):
    sum = 0
    for left, right in itertools.combinations(galaxies, 2):
        rows_passed = len([r for r in empty_rows if between(left[0], r, right[0])])
        cols_passed = len([c for c in empty_cols if between(left[1], c, right[1])])

        sum += (
            abs(left[0] - right[0])
            + (rows_passed * (scale - 1))
            + abs(left[1] - right[1])
            + (cols_passed * (scale - 1))
        )

    return sum


def between(start, mid, end):
    if start < end:
        return start < mid < end

    return start > mid > end


if __name__ == "__main__":
    main()
