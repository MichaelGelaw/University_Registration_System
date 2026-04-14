"""
dsa_lib — Custom Data Structures & Algorithms
==============================================
Re-exports every public name so existing import statements
(``from dsa_lib import LinkedQueue``, etc.) keep working unchanged.

Module breakdown
----------------
linked_queue.py   — Node + LinkedQueue  (FIFO, linked-list-based)
course_bst.py     — BSTNode + CourseBST  (O(log n) course catalog)
merge_sort.py     — merge_sort_students  (O(n log n), stable)
linear_search.py  — linear_search        (O(n), partial-match)
"""

from .linked_queue  import Node, LinkedQueue
from .course_bst    import BSTNode, CourseBST
from .merge_sort    import merge_sort_students
from .linear_search import linear_search

__all__ = [
    "Node", "LinkedQueue",
    "BSTNode", "CourseBST",
    "merge_sort_students",
    "linear_search",
]
