"""MergeSort utility for sorting student lists."""


def merge_sort_students(student_list, key_func, reverse=True):
    """
    Sort a list of Student objects using MergeSort.

    Parameters
    ----------
    student_list : list[Student]
    key_func     : callable — extracts the comparison value from a Student
                   e.g. ``lambda s: s.gpa``  or  ``lambda s: s.last.lower()``
    reverse      : bool — True for descending order (default, used for GPA),
                   False for ascending (used for names)

    Returns a new sorted list; the original is not modified.

    Complexity: O(n log n) time, O(n) space
    """
    if len(student_list) <= 1:
        return student_list

    mid = len(student_list) // 2
    left  = merge_sort_students(student_list[:mid],  key_func, reverse)
    right = merge_sort_students(student_list[mid:], key_func, reverse)

    return _merge(left, right, key_func, reverse)


def _merge(left, right, key_func, reverse):
    """Merge two already-sorted halves into one sorted list."""
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        left_val  = key_func(left[i])
        right_val = key_func(right[j])

        # Pick the 'winning' element based on sort direction
        pick_left = (left_val >= right_val) if reverse else (left_val <= right_val)

        if pick_left:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    # Append any remaining elements from either half
    result.extend(left[i:])
    result.extend(right[j:])
    return result
