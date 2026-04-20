"""Linear search utility for admin student filtering."""


def linear_search(items, query, key_func):
    """
    Scan every item and return those whose key contains the query string.

    Parameters
    ----------
    items    : iterable of objects to search through
    query    : str — the search term (case-insensitive, partial match)
    key_func : callable — extracts the searchable string from each item
               e.g. ``lambda s: f"{s.first} {s.last} {s.username}"``

    Returns a list of matching items (preserves original order).

    Complexity: O(n) regardless of input ordering
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
