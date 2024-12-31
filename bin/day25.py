from advent import input
from collections import defaultdict


def main():
    nodes = defaultdict(list)
    for line in input.lines():
        left, rest = line.split(": ")
        for right in rest.split(" "):
            nodes[left].append(right)
            nodes[right].append(left)

    # print_dot(nodes)

    # Now, we know what we need to remove
    # thx-frl, lhg-llm, ccp-fvm

    nodes["thx"].remove("frl")
    nodes["frl"].remove("thx")

    nodes["lhg"].remove("llm")
    nodes["llm"].remove("lhg")

    nodes["ccp"].remove("fvm")
    nodes["fvm"].remove("ccp")

    solve(nodes)


def print_dot(nodes):
    print("graph {")
    for n, lst in nodes.items():
        for other in lst:
            print(f"{n} -- {other}")
    print("}")


def solve(nodes):
    n1 = dfs(nodes, "thx")
    n2 = dfs(nodes, "frl")

    print("part 2:", n1 * n2)


def dfs(nodes, start):
    todo = [start]
    seen = set()

    while todo:
        v = todo.pop()
        if v in seen:
            continue

        seen.add(v)
        for w in nodes[v]:
            todo.append(w)

    return len(seen)


if __name__ == '__main__':
    main()
