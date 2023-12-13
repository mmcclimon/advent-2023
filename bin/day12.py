from advent import input
import functools


def main():
    p1, p2 = 0, 0
    for line in input.lines():
        p1 += process_line(line)
        p2 += process_line(expand(line))

    print(f"part 1: {p1}")
    print(f"part 2: {p2}")


def process_line(line):
    springs, dir_str = line.split()
    dirs = tuple(int(n) for n in dir_str.split(","))
    return compute(springs, dirs)


# This solution mostly stolen from Diderikdm on reddit
@functools.cache
def compute(springs, counts):
    if not counts:
        return 1 if "#" not in springs else 0

    hunk_len, counts = counts[0], counts[1:]
    hashes_remaining = sum(counts)
    dots_remaining = len(counts)

    result = 0

    for i in range(1 + len(springs) - hashes_remaining - dots_remaining - hunk_len):
        if "#" in springs[:i]:
            break

        mid = i + hunk_len
        nxt = mid + 1

        if (
            mid <= len(springs)  # not off the end
            and "." not in springs[i:mid]  # no spacers in this hunk
            and springs[mid:nxt] != "#"  # last char of hunk isn't #
        ):
            result += compute(springs[nxt:], counts)

    return result


def expand(line):
    springs, dirs = line.split()
    return " ".join(
        [
            "?".join([springs] * 5),
            ",".join([dirs] * 5),
        ]
    )


if __name__ == "__main__":
    main()
