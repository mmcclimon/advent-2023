from advent import input
from collections import defaultdict

def maybe_print(*args):
    print(*args)


def main():
    p1, p2 = 0, 0
    for i, hunk in enumerate(input.hunks()):
        # if i != 6:
        #     continue

        # print("\n".join(hunk))
        p1 += process_hunk(hunk)
        p2 += process_hunk_smudge(hunk)


    print(f"part 1: {p1}")
    print(f"part 2: {p2}")


def process_hunk(hunk) -> int:
    maybe_print("HUNK:\n" + "\n".join(hunk))

    if rv := compute(hunk):
        maybe_print(f"  {100*rv}\n")
        return 100 * rv

    cv = compute(rotate(hunk))
    if cv is None:
        maybe_print("NONE")
        return 0
    # assert cv is not None

    maybe_print(f"  {cv}\n")
    return cv


def compute(hunk) -> int | None:
    rows = defaultdict(list)
    big = 0

    for r, row in enumerate(hunk):
        rows[row].append(r)
        big = r

    return calc_deltas(list(rows.values()), big)


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

    return 0


def process_hunk_smudge(hunk):
    orig = process_hunk(hunk)
    maybe_print(f"{orig=}")

    if (rv := compute_bis(hunk))   and rv * 100 != orig:
        maybe_print(f"hey, {rv=}")
        return 100 * rv

    cv = compute_bis(rotate(hunk))

    if cv is None:
        print(f"\nProblem!\n{"\n".join(hunk)}\n")
        return 0

    return cv


def compute_bis(hunk):
    # print(f"\nHUNK:\n{"\n".join(hunk)}\n")

    rows = defaultdict(list)

    for r, row in enumerate(hunk):
        rows[row].append(r)

    for s1 in rows:
        for s2 in rows:
            if s1 == s2:
                continue

            if nearly_matches(s1, s2):
                for idx in rows[s1]:
                    maybe_print(f"interesting: {s1=}, {s2=}, {idx=}")
                    new = list(hunk)
                    new[idx] = s2
                    if val := compute(new):
                        print("NEW:")
                        print("\n".join(new))
                        maybe_print(f"hrm, {val=}")
                        # return val

    return 0


def nearly_matches(s1, s2):
    n_diff = 0

    for i in range(len(s1)):
        if s1[i] != s2[i]:
            n_diff += 1

        if n_diff > 1:
            return False

    return n_diff == 1


def make_grid_with(hunk, idx, repl):
    new = list(hunk)
    new[idx] = repl
    print(hunk)
    print(new)
    # new[idx]


if __name__ == "__main__":
    main()
