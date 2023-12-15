from advent import input


def main():
    [line] = input.lines()

    p1 = sum(hash(bit) for bit in line.split(","))
    print(p1)


def hash(s):
    cur = 0

    for c in s:
        cur = ((cur + ord(c)) * 17) % 256
        # print(f"after {c}: {cur}")

    return cur


if __name__ == "__main__":
    main()
