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

    sum1 = 0
    sum2 = 0
    scale = 1_000_000

    for left, right in itertools.combinations(galaxies, 2):
        # goofy
        minr = min(left[0], right[0])
        maxr = max(left[0], right[0])
        minc = min(left[1], right[1])
        maxc = max(left[1], right[1])

        rows_passed = len([r for r in empty_rows if minr < r < maxr])
        cols_passed = len([c for c in empty_cols if minc < c < maxc])

        sum1 += (
            abs(left[0] - right[0])
            + rows_passed
            + abs(left[1] - right[1])
            + cols_passed
        )

        sum2 += (
            abs(left[0] - right[0])
            + (rows_passed * (scale - 1))
            + abs(left[1] - right[1])
            + (cols_passed * (scale - 1))
        )

    print(sum1)
    print(sum2)


if __name__ == "__main__":
    main()
