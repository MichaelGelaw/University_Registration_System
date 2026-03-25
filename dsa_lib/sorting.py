def merge_sort_students(student_list, key_func, reverse=True):
    """
    Sorts a list of Student objects using MergeSort (O(n log n)).
    key_func: lambda to determine sorting criteria (e.g., lambda s: s.gpa)
    reverse: if True, sort descending (default for GPA); if False, sort ascending (for names)
    """
    if len(student_list) <= 1:
        return student_list

    mid = len(student_list) // 2
    left = merge_sort_students(student_list[:mid], key_func, reverse)
    right = merge_sort_students(student_list[mid:], key_func, reverse)

    return _merge(left, right, key_func, reverse)


def _merge(left, right, key_func, reverse):
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if reverse:
            # Descending: pick the larger value first
            if key_func(left[i]) >= key_func(right[j]):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        else:
            # Ascending: pick the smaller value first
            if key_func(left[i]) <= key_func(right[j]):
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result


def linear_search(items, query, key_func):
    """
    Linear search with partial-match filtering.
    Scans every item and returns all whose key_func(item) contains `query` (case-insensitive).
    
    items: list of objects
    query: search string
    key_func: function that returns the searchable string from an item
    Returns: list of matching items
    """
    if not query:
        return list(items)
    query_lower = query.lower()
    results = []
    for item in items:
        value = key_func(item).lower()
        if query_lower in value:
            results.append(item)
    return results