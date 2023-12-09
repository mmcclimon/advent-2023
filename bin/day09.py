from advent import input


def main():
    lines = [[int(n) for n in line.split()] for line in input.lines()]
    part1 = sum(extrapolate(line) for line in lines)
    print(f"part 1: {part1}")

    part2 = sum(extrapolate(line, reverse=True) for line in lines)
    print(f"part 2: {part2}")


def extrapolate(line, reverse=False):
    if not line or all(n == 0 for n in line):
        return 0

    diffs = [line[i] - line[i-1] for i in range(1, len(line))]
    if reverse:
        return line[0] - extrapolate(diffs, reverse)

    return line[-1] + extrapolate(diffs, reverse)


if __name__ == "__main__":
    main()
