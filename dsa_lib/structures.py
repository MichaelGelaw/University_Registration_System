class Node:
    """Node for linked-list-based data structures."""
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedQueue:
    """Custom FIFO Queue for FCFS Registration — built from scratch using linked nodes."""

    def __init__(self):
        self.front = self.rear = None
        self.size = 0

    def enqueue(self, item):
        new_node = Node(item)
        if self.rear is None:
            self.front = self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node
        self.size += 1

    def dequeue(self):
        if self.is_empty():
            return None
        temp = self.front
        self.front = temp.next
        if self.front is None:
            self.rear = None
        self.size -= 1
        return temp.data

    def peek(self):
        """Returns the front element without removing it."""
        if self.is_empty():
            return None
        return self.front.data

    def is_empty(self):
        return self.front is None

    def __len__(self):
        return self.size

    def to_list(self):
        """Helper for JSON serialization and UI display."""
        result = []
        curr = self.front
        while curr:
            result.append(curr.data)
            curr = curr.next
        return result

    def __contains__(self, item):
        """Support 'in' operator for checking membership."""
        curr = self.front
        while curr:
            if curr.data == item:
                return True
            curr = curr.next
        return False

    def remove(self, item):
        """Remove a specific item from the queue (for cancelling waitlist)."""
        if self.is_empty():
            return False
        # If it's the front node
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

    def position_of(self, item):
        """Returns 1-based position in queue, or -1 if not found."""
        pos = 1
        curr = self.front
        while curr:
            if curr.data == item:
                return pos
            pos += 1
            curr = curr.next
        return -1


class BSTNode:
    """Node for Binary Search Tree storing Course objects."""
    def __init__(self, course):
        self.course = course
        self.key = course.name.lower()
        self.left = None
        self.right = None


class CourseBST:
    """Binary Search Tree to organize course records — O(log n) search by name."""

    def __init__(self):
        self.root = None
        self._size = 0

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
            # Duplicate key — update the course data
            node.course = course

    def search(self, course_name):
        """O(log n) search by course name. Returns Course object or None."""
        return self._search_recursive(self.root, course_name.lower())

    def _search_recursive(self, node, key):
        if node is None:
            return None
        if node.key == key:
            return node.course
        if key < node.key:
            return self._search_recursive(node.left, key)
        return self._search_recursive(node.right, key)

    def delete(self, course_name):
        """Delete a course from the BST by name."""
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
            # Node found
            if node.left is None:
                return node.right, True
            elif node.right is None:
                return node.left, True
            # Two children — find inorder successor
            succ = self._min_node(node.right)
            node.course = succ.course
            node.key = succ.key
            node.right, _ = self._delete_recursive(node.right, succ.key)
            return node, True

    def _min_node(self, node):
        current = node
        while current.left:
            current = current.left
        return current

    def inorder(self):
        """Returns list of Course objects sorted alphabetically (inorder traversal)."""
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