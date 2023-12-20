from advent import input
from collections import deque


def main():
    modules = {}
    for line in input.lines():
        m = make_module(line)
        modules[m.label] = m

    modules["output"] = Sink("output", [])
    modules["rx"] = Sink("rx", [])  # goofy

    for m in modules.values():
        for out in m.outs:
            modules[out].add_input(m)

    low, high = 0, 0
    for i in range(1000):
        l, h = push_button(modules)
        low += l
        high += h

    print("part 1:", low * high)


def push_button(mods):
    todo = deque()
    todo.append(("button", 0, "broadcaster"))

    sent = [0, 0]

    while todo:
        src, pulse, dst = todo.popleft()
        mod = mods[dst]

        sent[pulse] += 1

        # s = "high" if pulse else "low"
        # print(f"{src} -{s}-> {dst}")

        for signal in mod.handle_pulse(src, pulse):
            todo.append(signal)

    return sent[0], sent[1]


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


class Sink(Module):
    pass


if __name__ == "__main__":
    main()
