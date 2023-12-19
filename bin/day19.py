from advent import input
import re
import operator


def main():
    fs, ps = input.hunks()

    flows = {}
    for f in fs:
        m = re.match(r"(.*?){(.*)}", f)
        assert m is not None

        rules = [Rule(r) for r in m.group(2).split(",")]
        flows[m.group(1)] = rules

    total = 0

    for p in ps:
        match = re.match(r"{x=(\d+),m=(\d+),a=(\d+),s=(\d+)}", p)
        assert match is not None

        part = {s: int(n) for (s, n) in zip("xmas", match.groups())}
        if should_accept(flows, part):
            total += sum(part.values())

    print(total)


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


class Rule:
    def __init__(self, text):
        self.text = text
        self.op = None
        self.param = None
        self.compare = None
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


if __name__ == "__main__":
    main()
