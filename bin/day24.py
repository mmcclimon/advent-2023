from advent import input
from collections import namedtuple


Stone = namedtuple("Stone", ["pos", "vec"])


def main():
    stones = []
    for line in input.lines():
        location, velocity = line.split(" @ ")
        pos = tuple(map(int, location.split(", ")))
        vec = tuple(map(int, velocity.split(", ")))

        stones.append(Stone(pos, vec))

    limit = (200000000000000, 400000000000000)
    total = 0

    for i in range(len(stones)):
        for j in range(i+1, len(stones)):
            xy = calc_intersection(stones[i], stones[j])
            if xy is None:
                continue

            x, y = xy

            if limit[0] <= x <= limit[1] and limit[0] <= y <= limit[1]:
                total += 1

    print(f"part 1: {total}")


def calc_intersection(s1, s2):
    x1, y1, _ = s1.pos
    a = s1.vec[1] / s1.vec[0]
    c = y1 - (a * x1)

    x2, y2, _ = s2.pos
    b = s2.vec[1] / s2.vec[0]
    d = y2 - (b * x2)

    # parallel lines
    if a == b:
        return

    x = (d - c) / (a - b)
    y = a*x + c

    if x1 < x and s1.vec[0] < 0 or x1 > x and s1.vec[0] > 0:
        # print("in the past for a")
        return

    if x2 < x and s2.vec[0] < 0 or x2 > x and s2.vec[0] > 0:
        # print("in the past for b")
        return

    return (x, y)


# def rearrange(pos, vec):


if __name__ == '__main__':
    main()
