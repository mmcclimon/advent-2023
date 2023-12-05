from advent import input
import collections
import math
import re


def main():
    seeds, *hunks = input.hunks()
    seeds = [int(n) for n in seeds[0].removeprefix("seeds: ").split()]

    transformer = make_transformer(hunks)
    print(min(transformer(seed) for seed in seeds))


def make_transformer(hunks):
    lookups = []

    Val = collections.namedtuple('Key', ['dst', 'src', 'range'])

    for hunk in hunks:
        match = re.match(r"[a-z]+-to-(\w+) map", hunk[0])
        assert match is not None
        kind = match.group(1)
        _ = kind

        lookup = {}

        for line in hunk[1:]:
            dst, src, range = (int(n) for n in line.split())
            lookup[src] = Val(dst, src, range)

        lookups.append(lookup)

    def fn(item):
        for lookup in lookups:
            for k, val in lookup.items():
                if k <= item < k + val.range:
                    delta = item - val.src
                    item = val.dst + delta
                    break

        return item

    return fn


if __name__ == "__main__":
    main()
