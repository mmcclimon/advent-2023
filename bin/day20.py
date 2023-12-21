from advent import input
from collections import deque
import math


def main():
    lines = list(input.lines())

    print("part 1:", part_one(lines))
    print("part 2:", part_two(lines))


def part_one(lines):
    modules = make_modules(lines)

    low, high = 0, 0
    for i in range(1000):
        l, h = push_button(modules)
        low += l
        high += h

    return low * high


def part_two(lines):
    # Ok so. This is extremely specific to my input, obviously. I generated a
    # dot file (in the repo) that prints out the structure of the graph as a
    # picture. This made clear that there are 4 subgraphs; all we need to do
    # is to determine how many button presses cause the tail end of each
    # subgraph to output a 0, and then multiply them together. This is silly,
    # but I have no idea how to do this in the general case.

    g1 = do_subgraph(
        lines,
        "sr vl fj zd ln qq qm gm tj lc fn pr gf xn".split(),
    )

    g2 = do_subgraph(
        lines,
        "ch mc ds cc nn ff pl sf bp jz qj xm db xf".split(),
    )

    g3 = do_subgraph(
        lines,
        "hd nh hv lr sb ks vz cr gx cd pm qk vc qn".split(),
    )

    g4 = do_subgraph(
        lines,
        "bx qp cb kt rz cv xz jd vm cl bf pf qx zl".split(),
    )

    return math.lcm(g1, g2, g3, g4)


def do_subgraph(lines, include):
    sink = include.pop()
    include.append("broadcaster")

    mods = make_modules(lines)
    sub = {}
    for label in include:
        sub[label] = mods[label]

    sub[sink] = Sink(sink, [])  # goofy

    for mod in sub.values():
        mod.outs = [m for m in mod.outs if m in sub]

    pressed = 0
    while True:
        pressed += 1
        try:
            push_button(sub)
        except Exception:
            return pressed


def push_button(mods):
    todo = deque()
    todo.append(("button", 0, "broadcaster"))

    sent = [0, 0]

    while todo:
        src, pulse, dst = todo.popleft()
        sent[pulse] += 1

        for signal in mods[dst].handle_pulse(src, pulse):
            todo.append(signal)

    return sent[0], sent[1]


def make_modules(lines):
    modules = {}
    for line in lines:
        m = make_module(line)
        modules[m.label] = m

    # silly
    modules["rx"] = Sink("rx", [])
    modules["output"] = Sink("output", [])

    for m in modules.values():
        for out in m.outs:
            modules[out].add_input(m)

    return modules


def make_module(line):
    left, right = line.split(" -> ")
    outs = right.split(", ")

    if left == "broadcaster":
        return Broadcaster(left, outs)

    if left[0] == "%":
        return FlipFlop(left[1:], outs)

    if left[0] == "&":
        return Conjunction(left[1:], outs)

    assert False, line


class Module:
    def __init__(self, label, outs):
        self.label = label
        self.outs = outs
        self.ins = set()  # post-processed

    def add_input(self, module):
        self.ins.add(module)

    def handle_pulse(self, src, pulse):
        return []

    def reset(self):
        pass


class Broadcaster(Module):
    def __repr__(self):
        return f"<Broadcaster outs={self.outs}>"

    def handle_pulse(self, _, pulse):
        for out in self.outs:
            yield (self.label, pulse, out)


class FlipFlop(Module):
    On = True
    Off = False

    def __init__(self, label, outs):
        super().__init__(label, outs)
        self.state = self.Off

    def __repr__(self):
        return f"<FlipFlop {self.label} on={self.state}>"

    def handle_pulse(self, _, pulse):
        if pulse:
            return []

        self.state = not self.state
        for out in self.outs:
            yield (self.label, int(self.state), out)

    def reset(self):
        self.state = self.Off


class Conjunction(Module):
    def __init__(self, label, outs):
        super().__init__(label, outs)
        self.memory = {}

    def __repr__(self):
        return f"<Conj {self.label} state={self.memory}>"

    def add_input(self, module):
        self.ins.add(module)
        self.memory[module.label] = 0

    def handle_pulse(self, src, pulse):
        self.memory[src] = pulse
        signal = 0 if all(self.memory.values()) else 1

        for out in self.outs:
            yield (self.label, signal, out)

    def reset(self):
        for k in self.memory:
            self.memory[k] = 0


class Sink(Module):
    def handle_pulse(self, src, pulse):
        if pulse == 0:
            raise Exception(f"sink {self.label} received 0")

        return []


if __name__ == "__main__":
    main()
