from advent import input
import collections
import itertools
import re


def main():
    seeds, *hunks = input.hunks()
    seeds = [int(n) for n in seeds[0].removeprefix("seeds: ").split()]

    global transformer
    transformer = make_transformer(hunks)
    # print(min(transformer(seed) for seed in munge_seeds(seeds)))

    for seed in munge_seeds(seeds):
        v = transformer(seed)
        print(f"{seed} -> {v}")


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
                    item = val.dst + (item - val.src)
                    break

        return item

    return fn


def part_two(seeds):
    for start, span in itertools.batched(seeds, 2):
        best_for_range(start, span)


def best_for_range(start, span):
    end = start + span - 1
    print(start, end)
    have = collections.deque()

    global transformer
    have.append(transformer(start))
    have.append(transformer(end))
    print(have)

    # print("start stop:", transformer(start), transformer(end))

    # binary search over the span?
    pass


def munge_seeds(seeds):
    for start, span in itertools.batched(seeds, 2):
        print(f"starting span {start}")
        for i in range(start, start + span):
            yield i


if __name__ == "__main__":
    main()
