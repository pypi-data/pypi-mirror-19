from manipulator.query import treat_query

def get(data, query):
    """traverses data based on the query.

     - params:
       - data: the input to traverse
       - query: the rules for traversal
     - complexity: determined by the complexity of the query
     - returns: the data found at the leaves of the traversal"""
    selectors = treat_query(query)

    for selector in selectors:
        _, data = selector(data)

    return data
