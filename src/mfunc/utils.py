def callable_name(func):
    try:
        return func.__name__
    except AttributeError:
        return func.__class__.__name__


def add_parentheses(s):
    return ''.join(['(', s, ')'])
