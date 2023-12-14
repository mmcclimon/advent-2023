from advent import input


def main():
    grid = {}
    rows, cols = 0, 0
    for r, line in enumerate(input.lines()):
        rows += 1
        col_count = 0
        for c, char in enumerate(line):
            grid[(r, c)] = char
            col_count += 1

        cols = col_count

    # pg(grid)

    for r in range(1, rows):
        for c in range(cols):
            if grid[(r, c)] != "O":
                continue

            cur = r
            while cur >= 1:
                if grid[(cur - 1, c)] != ".":
                    break

                # print(f"moving from {(cur, c)} to {(cur-1, c)}")

                grid[(cur - 1, c)] = "O"
                grid[(cur, c)] = "."
                cur -= 1

    # pg(grid)

    total = 0

    for r in range(rows):
        for c in range(cols):
            if grid[(r, c)] != "O":
                continue

            total += rows - r

    print(total)


def pg(grid):
    row = max(r for r, _ in grid)
    col = max(c for _, c in grid)

    for r in range(row + 1):
        line = []
        for c in range(col + 1):
            line.append(grid[(r, c)])

        print("".join(line))


if __name__ == "__main__":
    main()
