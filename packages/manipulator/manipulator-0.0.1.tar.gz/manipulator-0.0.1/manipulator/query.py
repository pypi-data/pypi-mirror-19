from functools import wraps

def manipulate_all(name, data):
    def manipulate_internal(fn):
        for elem in data:
            k, v = select_id(name, elem)
            elem[k] = fn(v)
        return data
    return manipulate_internal


def curry(fn):
    @wraps(fn)
    def wrapped(x):
        return lambda y: fn(x, y)
    return wrapped


def select_id(name, data):
    if isinstance(data, list):
        name = int(name)

    return name, data[name]


def select_class(name, data):
    if isinstance(data, list):
        return manipulate_all(name, data), [select_id(name, elem)[1] for elem in data]
    return name, [data[name]]


def lookup_selector(start):
    if start == "#":
        return curry(select_id)
    elif start == ".":
        return curry(select_class)
    raise ValueError("Unknown selector: {}".format(start))


def treat_query(query):
    selectors = []

    for elem in query.split(" "):
        elem = elem.strip()

        if not elem:
            continue

        selector = lookup_selector(elem[0])

        selectors.append(selector(elem[1:]))

    return selectors
