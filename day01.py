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


def digit_from(s, include_words=False):
    if s[0].isdigit():
        return int(s[0])

    if not include_words:
        return

    for digit in digits:
        if s.startswith(digit):
            return digits[digit]

    return


def find_first(line, include_words=False):
    for i in range(len(line)):
        if digit := digit_from(line[i:], include_words):
            return digit

    assert False


def find_last(line, include_words=False):
    for i in range(len(line) - 1, -1, -1):
        if digit := digit_from(line[i:], include_words):
            return digit

    assert False


sum1 = 0
sum2 = 0

for line in input.lines():
    f1 = find_first(line)
    l1 = find_last(line)

    f2 = find_first(line, True)
    l2 = find_last(line, True)

    sum1 += f1*10 + l1
    sum2 += f2*10 + l2

print(f"part 1: {sum1}")
print(f"part 2: {sum2}")
