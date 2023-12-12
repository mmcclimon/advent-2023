from advent import input
import itertools
import re


def main():
    sum = 0
    for line in input.lines():
        sum += process_line(line)

    print(sum)


def process_line(line):
    springs, dir_str = line.split()
    springs = list(springs)
    dirs = tuple(int(n) for n in dir_str.split(","))

    questions = [i for i, c in enumerate(springs) if c == "?"]

    sum = 0

    for prod in itertools.product([".", "#"], repeat=len(questions)):
        new = springs.copy()
        i = 0
        for idx in questions:
            new[idx] = prod[i]
            i += 1

        if is_valid("".join(new), dirs):
            sum += 1

    return sum


def is_valid(line, dirs):
    bits = re.findall(r"(#+)", line)
    if len(bits) != len(dirs):
        return False

    for bit, wantlen in zip(bits, dirs):
        if len(bit) != wantlen:
            return False

    return True


if __name__ == "__main__":
    main()
