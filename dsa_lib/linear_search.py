def linear_search(items, query, key_func):
    """
    Scan every item and return those whose key contains the query string.
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