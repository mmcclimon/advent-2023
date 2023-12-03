from advent import input
import re


def main():
    lines = list(input.lines())
    symbols = {}

    symbols = {
        (r, c): char
        for r, line in enumerate(lines)
        for c, char in enumerate(line)
        if not char.isdigit() and char != "."
    }

    gears = {tup: [] for tup in symbols if symbols[tup] == "*"}

    sum1 = 0
    sum2 = 0

    for r, line in enumerate(lines):
        for match in re.finditer(r"\b(\d+)\b", line):
            found, gears_touched = is_part_number(symbols, r, match)
            if not found:
                continue

            sum1 += int(match.group())

            for gear in gears_touched:
                gears[gear].append(int(match.group()))

    for gear, matches in gears.items():
        if len(matches) == 2:
            sum2 += matches[0] * matches[1]

    print(f"part 1: {sum1}")
    print(f"part 2: {sum2}")


# is part, set[gears touched]
def is_part_number(symbols, r, match):
    found = False
    found_gears = set()

    for c in range(*match.span()):
        if tup := touches_symbol(symbols, r, c):
            found = True
            sym, coord = tup
            if sym == "*":
                found_gears.add(coord)

    return found, found_gears


def touches_symbol(symbols, r, c):
    for rx in [-1, 0, 1]:
        for cx in [-1, 0, 1]:
            r2, c2 = r + rx, c + cx
            try:
                if sym := symbols[(r2, c2)]:
                    # (I manually verified every number only touches 1 symbol)
                    return sym, (r2, c2)
            except KeyError:
                pass

    return


if __name__ == "__main__":
    main()
