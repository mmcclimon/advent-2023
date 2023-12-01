from advent import input

digits = {
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9,
}


def find(line, indexes, include_words):
    for i in indexes:
        if line[i].isdigit():
            return int(line[i])

        if not include_words:
            continue

        for digit in digits:
            if line[i:].startswith(digit):
                return digits[digit]

    assert False


def find_first(line, include_words=False):
    return find(line, range(len(line)), include_words)


def find_last(line, include_words=False):
    return find(line, range(len(line) - 1, -1, -1), include_words)


sum1 = 0
sum2 = 0

for line in input.lines():
    f1 = find_first(line)
    l1 = find_last(line)
    sum1 += f1 * 10 + l1

    f2 = find_first(line, True)
    l2 = find_last(line, True)
    sum2 += f2 * 10 + l2

print(f"part 1: {sum1}")
print(f"part 2: {sum2}")
