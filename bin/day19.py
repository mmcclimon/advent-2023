from advent import input
import copy
from functools import reduce
import operator
import re


def main():
    fs, ps = input.hunks()

    flows = {}
    for f in fs:
        m = re.match(r"(.*?){(.*)}", f)
        assert m is not None

        rules = [Rule(r) for r in m.group(2).split(",")]
        flows[m.group(1)] = rules

    print("part 1:", part_one(flows, ps))
    print("part 2:", analyze_flows(flows))


def part_one(flows, ps):
    total = 0

    for p in ps:
        match = re.match(r"{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}", p)
        assert match is not None

        part = {s: int(n) for (s, n) in zip("xmas", match.groups())}
        if should_accept(flows, part):
            total += sum(part.values())

    return total


def should_accept(flows, part) -> bool:
    flow = flows["in"]
    while True:
        for rule in flow:
            match res := rule(part):
                case None:
                    continue
                case "R":
                    return False
                case "A":
                    return True
                case _:
                    flow = flows[res]
                    break  # next rule

    assert False, "unreachable"


def analyze_flows(flows):
    # This is obviously stupid, but works because n is small.
    ranges = {
        "x": set(range(1, 4001)),
        "m": set(range(1, 4001)),
        "a": set(range(1, 4001)),
        "s": set(range(1, 4001)),
    }

    # in which I DFS again.
    S = []
    seen = set()
    S.append(("in", ranges))

    total = 0

    while S:
        label, ranges = S.pop()

        if label in seen:
            continue

        if label == "R":  # reject
            continue

        if label == "A":
            total += reduce(operator.mul, (len(ranges[k]) for k in "xmas"))
            continue

        seen.add(label)

        for rule in flows[label]:
            if rule.op is None:
                S.append((rule.out, ranges))
            else:
                p = rule.param

                # for the path we're taking: remove all the false bits
                rangecopy = copy.deepcopy(ranges)
                for num in (n for n in ranges[p] if rule.apply_false(n)):
                    rangecopy[p].discard(num)
                S.append((rule.out, rangecopy))

                # for everything else: remove everything else
                for num in [n for n in ranges[p] if rule.apply_true(n)]:
                    ranges[p].discard(num)

    return total


class Rule:
    def __init__(self, text):
        self.text = text
        self.op = None
        self.param = None
        self.compare: int | None = None
        self.out = None

        if m := re.match(r"(\w+)(<|>)(\d+):(\w+)", text):
            param, op, val, out = m.groups()
            self.param = param
            self.op = operator.lt if op == "<" else operator.gt
            self.compare = int(val)
            self.out = out
        else:
            self.out = text

    def __repr__(self):
        return f"<Rule r=[{self.text}]>"

    def __call__(self, part):
        if self.op is None:
            return self.out

        if self.op(part[self.param], self.compare):  # type: ignore
            return self.out

        return None

    def apply_true(self, num):
        return self.op(num, self.compare)

    def apply_false(self, num):
        return not self.apply_true(num)


if __name__ == "__main__":
    main()
