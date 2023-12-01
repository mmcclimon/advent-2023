import fileinput


def lines():
    yield from (line.rstrip("\n") for line in fileinput.input(encoding="utf-8"))


def ints():
    yield from map(int, lines())


def hunks():
    """
    Split file into hunks separated by runs of whitespace.
    """

    buf = []

    for line in lines():
        if line == "":
            yield buf
            buf = []
            continue

        buf.append(line)

    if len(buf):
        yield buf
