from advent import input
import copy
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

    total = 0

    analyze_flows(flows)

    for p in ps:
        match = re.match(r"{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}", p)
        assert match is not None

        part = {s: int(n) for (s, n) in zip("xmas", match.groups())}
        if should_accept(flows, part):
            total += sum(part.values())

    # print(total)


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
    # for label, rules in flows.items():
    #     outs = {r.out for r in rules}
    #     print(f"{label} -> {{{' '.join(outs)}}}")

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

    outs = {"A": set(), "R": set()}
    total = 0

    while S:
        label, ranges = S.pop()
        print(f"looking at {label}")

        if label == "R":
            # print("reject")
            continue

        if label == "A":
            result = (
                len(ranges["x"])
                * len(ranges["m"])
                * len(ranges["a"])
                * len(ranges["s"])
            )
            print("accept (TODO)", result)
            total += result
            continue

        if label not in seen:
            seen.add(label)

            for rule in flows[label]:
                rangecopy = copy.deepcopy(ranges)
                if rule.op is None:
                    S.append((rule.out, rangecopy))
                else:
                    p = rule.param
                    for num in [n for n in rangecopy[p] if not rule.apply_true(n)]:
                        # print(f"removing {p}={num}")
                        rangecopy[p].remove(num)
                    S.append((rule.out, rangecopy))

    print(total)

    # for l2 in [r.out for r in flows[label]]:
    #     if l2 == "R":
    #         continue

    #     if l2 == "A":
    #         print("found an out")
    #         break

    #     S.append((l2, list(path)))

    # start with literally everything
    ranges = {
        "x": set(range(1, 4001)),
        "m": set(range(1, 4001)),
        "a": set(range(1, 4001)),
        "s": set(range(1, 4001)),
    }

    total = 0

    for path in sorted(outs["A"]):
        # generate the set of sets for this path
        n, ranges = examine_path(flows, ranges, path)
        # print(ranges)
        total += n

    # total = len(ranges["x"]) * len(ranges["m"]) * len(ranges["a"]) * len(ranges["s"])
    print(total)

    # for every distinct path to A
    # walk from A -> in
    # construct condition chain


def examine_path(flows, _ranges, path):
    print(path)

    ranges = {
        "x": set(range(1, 4001)),
        "m": set(range(1, 4001)),
        "a": set(range(1, 4001)),
        "s": set(range(1, 4001)),
    }

    for i in range(len(path) - 1):
        label = path[i]
        to = path[i + 1]
        rules = flows[label]
        print("   ", label, flows[label])

        for rule in rules:
            if rule.out == to:
                # print(f"RULE: {rule}")
                fn = rule.apply_true
            else:
                # print(f"RULE: NOT {rule}")
                fn = rule.apply_false

            match rule.op:
                case None:
                    pass
                case operator.lt:
                    p = rule.param
                    for num in [n for n in ranges[p] if not fn(n)]:
                        # print(f"removing {p}={num}")
                        ranges[p].remove(num)
                case operator.gt:
                    p = rule.param
                    for num in [n for n in ranges[p] if not fn(n)]:
                        # print(f"removing {p}={num}")
                        ranges[p].remove(num)

            if rule.out == to:
                break

    print("   ", {k: len(ranges[k]) for k in ranges})

    total = len(ranges["x"]) * len(ranges["m"]) * len(ranges["a"]) * len(ranges["s"])
    print("   ", path, total)
    return total, ranges


# if the total range is 1-20
# for s<10: 9 numbers.
# for s>10: 10 numbers.


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

# 496534091000000
# 167409079868000
#  41256000000000
#  48571397887500

# ('in', 'px', 'A')
#    in <Rule r=[s<1351:px]>
#    px <Rule r=[m>2090:A]>
# so, after this rule you should never have x=?, m>2090, a?!, s<135, m>2090
# ('in', 'px', 'A') 41256000000000
