from advent import input
import re


def main():
    lines = list(input.lines())

    symbols = {
        (r, c): char
        for r, line in enumerate(lines)
        for c, char in enumerate(line)
        if not char.isdigit() and char != "."
    }

    gears = {coords: [] for coords, sym in symbols.items() if sym == "*"}

    sum1 = 0

    for r, line in enumerate(lines):
        for match in re.finditer(r"\b(\d+)\b", line):
            coord = is_part_number(symbols, r, match)
            if not coord:
                continue

            part_num = int(match.group())
            sum1 += part_num

            if coord in gears:
                gears[coord].append(part_num)

    sum2 = sum(parts[0] * parts[1] for parts in gears.values() if len(parts) == 2)

    print(f"part 1: {sum1}")
    print(f"part 2: {sum2}")


# returns coordinates of symbol it touches, if any
def is_part_number(symbols, r, match):
    for c in range(*match.span()):
        if coord := touches_symbol(symbols, r, c):
            return coord

    return


# returns the coordinates of the thing it touches
def touches_symbol(symbols, r, c):
    for rx in [-1, 0, 1]:
        for cx in [-1, 0, 1]:
            r2, c2 = r + rx, c + cx
            try:
                # (I manually verified every number only touches 1 symbol)
                if symbols[(r2, c2)]:
                    return r2, c2
            except KeyError:
                pass

    return


if __name__ == "__main__":
    main()
