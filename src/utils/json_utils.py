def json_structure_types_match(data1, data2, path=None):
    """
    Checks if the top-level keys of two dictionaries match.
    Args:
        data1: Reference JSON-like object (dict).
        data2: Test JSON-like object to check against data1.
        path: Used internally to track the path to the current key (not used here).
    Returns:
        (bool, list): Tuple of (True if top-level keys match, False otherwise, list of mismatched key paths)
    """
    if not (isinstance(data1, dict) and isinstance(data2, dict)):
        return (False, [["Both inputs must be dictionaries at the top level."]])
    keys1 = set(data1.keys())
    keys2 = set(data2.keys())
    mismatches = []
    for k in keys1 - keys2:
        mismatches.append([f"key '{k}' missing"])
    for k in keys2 - keys1:
        mismatches.append([f"extra key '{k}'"])
    return (len(mismatches) == 0, mismatches) 