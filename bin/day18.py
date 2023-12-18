from advent import input


def main():
    lines = []

    for line in input.lines():
        dir, n, color = line.split()
        lines.append((dir, int(n), color[2:-1]))

    print("part 1:", area((dir, n) for dir, n, _ in lines))
    print("part 2:", area(correct(color) for _, _, color in lines))


def correct(color):
    return "RDLU"[int(color[-1])], int(color[:-1], 16)


def area(pairs):
    vertices = [(0, 0)]
    perim = 0

    dirs = {"U": (-1, 0), "D": (1, 0), "R": (0, 1), "L": (0, -1)}

    for dir, n in pairs:
        r, c = vertices[-1]
        dr, dc = dirs[dir]

        vertices.append((r + dr * n, c + dc * n))
        perim += n

    return shoelace(vertices, perim)


def shoelace(vertices, perim):
    n = len(vertices) - 1
    s1, s2 = 0, 0

    for i in range(n):
        j = i + 1
        s1 += vertices[i][0] * vertices[j][1]
        s2 += vertices[i][1] * vertices[j][0]

    # catch the ends
    s1 += vertices[n][0] * vertices[0][1]
    s2 += vertices[0][0] * vertices[n][1]

    return int((abs(s1 - s2) / 2) + (perim / 2) + 1)


if __name__ == "__main__":
    main()
