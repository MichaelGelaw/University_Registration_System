"""CourseBST implementation for alphabetically sorted course storage."""


class BSTNode:
    """A single node in the Course BST."""

    def __init__(self, course):
        self.course = course
        self.key = course.name.lower()   # comparison key
        self.left = None
        self.right = None


class CourseBST:
    """
    Binary Search Tree keyed on course name (case-insensitive).

    Supports insert, search, delete, and in-order traversal.
    Duplicate inserts (same name) update the stored course in place.
    """

    def __init__(self):
        self.root = None
        self._size = 0

    # ── Insertion ─────────────────────────────────────────────────────

    def insert(self, course):
        if not self.root:
            self.root = BSTNode(course)
            self._size += 1
        else:
            self._insert_recursive(self.root, course)

    def _insert_recursive(self, node, course):
        key = course.name.lower()
        if key < node.key:
            if node.left is None:
                node.left = BSTNode(course)
                self._size += 1
            else:
                self._insert_recursive(node.left, course)
        elif key > node.key:
            if node.right is None:
                node.right = BSTNode(course)
                self._size += 1
            else:
                self._insert_recursive(node.right, course)
        else:
            # Duplicate key — update course data in place
            node.course = course

    # ── Search ────────────────────────────────────────────────────────

    def search(self, course_name):
        """O(log n) lookup by name. Returns the Course object or None."""
        return self._search_recursive(self.root, course_name.lower())

    def _search_recursive(self, node, key):
        if node is None:
            return None
        if node.key == key:
            return node.course
        if key < node.key:
            return self._search_recursive(node.left, key)
        return self._search_recursive(node.right, key)

    # ── Deletion ──────────────────────────────────────────────────────

    def delete(self, course_name):
        """Remove a course by name. Returns True if it was found."""
        self.root, deleted = self._delete_recursive(self.root, course_name.lower())
        if deleted:
            self._size -= 1
        return deleted

    def _delete_recursive(self, node, key):
        if node is None:
            return node, False

        if key < node.key:
            node.left, deleted = self._delete_recursive(node.left, key)
            return node, deleted
        elif key > node.key:
            node.right, deleted = self._delete_recursive(node.right, key)
            return node, deleted
        else:
            # Node found — three deletion cases
            if node.left is None:
                return node.right, True
            elif node.right is None:
                return node.left, True
            # Two children: replace with in-order successor
            succ = self._min_node(node.right)
            node.course = succ.course
            node.key = succ.key
            node.right, _ = self._delete_recursive(node.right, succ.key)
            return node, True

    def _min_node(self, node):
        """Find the leftmost (minimum) node in a subtree."""
        current = node
        while current.left:
            current = current.left
        return current

    # ── Traversal ─────────────────────────────────────────────────────

    def inorder(self):
        """Return all Course objects sorted alphabetically (in-order traversal)."""
        courses = []
        self._inorder_recursive(self.root, courses)
        return courses

    def _inorder_recursive(self, node, courses):
        if node:
            self._inorder_recursive(node.left, courses)
            courses.append(node.course)
            self._inorder_recursive(node.right, courses)

    def __len__(self):
        return self._size
