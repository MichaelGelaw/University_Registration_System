"""
linked_queue.py
---------------
Singly-linked-list Node and the LinkedQueue built on top of it.

LinkedQueue provides O(1) enqueue / dequeue and is used as the
FCFS (First-Come-First-Served) waitlist for every CourseOffering.
"""


class Node:
    """A single link in the linked list — holds one piece of data."""

    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedQueue:
    """
    FIFO Queue implemented with linked nodes (no Python collections used).

    Complexity
    ----------
    enqueue  → O(1)
    dequeue  → O(1)
    peek     → O(1)
    __contains__ / position_of / remove → O(n)  (linear scan)
    """

    def __init__(self):
        self.front = self.rear = None
        self.size = 0

    # ── Core operations ───────────────────────────────────────────────

    def enqueue(self, item):
        """Add item to the rear of the queue."""
        new_node = Node(item)
        if self.rear is None:
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node
        self.size += 1

    def dequeue(self):
        """Remove and return the front item, or None if empty."""
        if self.is_empty():
            return None
        temp = self.front
        self.front = temp.next
        if self.front is None:
            self.rear = None
        self.size -= 1
        return temp.data

    def peek(self):
        """Return the front item without removing it."""
        if self.is_empty():
            return None
        return self.front.data

    def is_empty(self):
        return self.front is None

    def __len__(self):
        return self.size

    # ── Membership & position ─────────────────────────────────────────

    def __contains__(self, item):
        """Support the 'in' operator — O(n) scan."""
        curr = self.front
        while curr:
            if curr.data == item:
                return True
            curr = curr.next
        return False

    def position_of(self, item):
        """Return the 1-based queue position of item, or -1 if absent."""
        pos = 1
        curr = self.front
        while curr:
            if curr.data == item:
                return pos
            pos += 1
            curr = curr.next
        return -1

    # ── Mutation ──────────────────────────────────────────────────────

    def remove(self, item):
        """
        Remove a specific item anywhere in the queue (for cancelling a waitlist spot).
        Returns True if the item was found and removed, False otherwise.
        """
        if self.is_empty():
            return False

        # Special case: item is at the front
        if self.front.data == item:
            self.dequeue()
            return True

        prev = self.front
        curr = self.front.next
        while curr:
            if curr.data == item:
                prev.next = curr.next
                if curr == self.rear:
                    self.rear = prev
                self.size -= 1
                return True
            prev = curr
            curr = curr.next
        return False

    # ── Serialization ─────────────────────────────────────────────────

    def to_list(self):
        """Return a plain list of items in FIFO order (for JSON serialization / UI display)."""
        result = []
        curr = self.front
        while curr:
            result.append(curr.data)
            curr = curr.next
        return result
