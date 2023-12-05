from advent import input
import collections
import math
import re


def main():
    seeds, *hunks = input.hunks()
    seeds = [int(n) for n in seeds[0].removeprefix("seeds: ").split()]

    lookups = []

    for hunk in hunks:
        _, m = generate_map(hunk)
        lookups.append(m)

    location = math.inf

    for seed in seeds:
        for transformer in lookups:
            seed = transformer(seed)

        location = min(location, seed)

    print(location)


def generate_map(lines):
    match = re.match(r"[a-z]+-to-(\w+) map", lines[0])
    assert match is not None
    kind = match.group(1)

    Val = collections.namedtuple('Key', ['dst', 'src', 'range'])

    lookup = {}

    for line in lines[1:]:
        dst, src, range = (int(n) for n in line.split())
        lookup[src] = Val(dst, src, range)

    def fn(source):
        for k, val in lookup.items():
            if k <= source <= k + val.range:
                delta = source - val.src
                return val.dst + delta

        return source

    return kind, fn


if __name__ == "__main__":
    main()
