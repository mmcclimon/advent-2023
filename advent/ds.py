"""
Data structures useful for advent problems
"""

from dataclasses import dataclass
from typing import Any, Self


@dataclass
class Node:
    data: Any
    next: Self | None = None
    prev: Self | None = None

    def __repr__(self):
        return f"<Node data={self.data}>"


# actually doubly linked, because it makes some things less tedious
class LinkedList:
    def __init__(self, lst=None):
        self.root = None

        if lst is None:
            return

        self.root = Node(lst[0], None)
        prev = self.root

        for item in lst[1:]:
            node = Node(item, None)
            prev.next = node
            prev = node

    def __repr__(self):
        return f"<LinkedList root={self.root}>"

    def __iter__(self):
        cur = self.root
        while cur is not None:
            yield cur
            cur = cur.next

    def is_empty(self) -> bool:
        return self.root is None

    def cons(self, value):
        node = Node(value, next=self.root)

        if self.is_empty():
            self.root = node
            return

        assert self.root is not None
        self.root.prev = node
        self.root = node

    def append(self, value):
        node = Node(value)

        if self.is_empty():
            self.root = node
            return

        cur = self.root
        while cur is not None:
            node.prev = cur
            cur = cur.next

        assert node.prev is not None
        node.prev.next = node

    def remove(self, doomed: Node):
        if doomed.prev is not None:
            doomed.prev.next = doomed.next

        if doomed.next is not None:
            doomed.next.prev = doomed.prev

        if doomed == self.root:
            self.root = doomed.next
