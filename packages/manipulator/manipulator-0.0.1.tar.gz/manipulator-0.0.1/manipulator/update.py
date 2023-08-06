import copy

from manipulator.query import treat_query

def update(inpt, query, fn, in_place=True):
    """transforms data based on the query dynamically.

     - params:
       - data: the input to transform
       - query: the rules for traversal
       - fn: a transformation function for the leaves
       - in_place: determines whether we should perform the transformations in place (True per default)
     - complexity: determined by the complexity of the query
     - returns: the transformed data"""
    if in_place:
        data = inpt
    else:
        data = copy.deepcopy(inpt)

    selectors = treat_query(query)

    if not selectors:
        return data

    d = data
    last_key = None
    last_d = data
    for selector in selectors:
        last_d = d
        last_key, d = selector(d)

    if callable(last_key):
        last_d = last_key(fn)
    elif isinstance(d, list) or isinstance(d, dict):
        d = fn(d)
    else:
        last_d[last_key] = fn(d)

    return data


def set(inpt, query, val, in_place=True):
    """transforms data based on the query statically.

     - params:
       - data: the input to transform
       - query: the rules for traversal
       - val: the value to which the leaves should be set
       - in_place: determines whether we should perform the transformations in place (True per default)
     - complexity: determined by the complexity of the query
     - returns: the transformed data"""
    return update(inpt, query, lambda _: val, in_place)
