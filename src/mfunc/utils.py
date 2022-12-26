def callable_name(func):
    """Return the name of any callable, regardless of whether it is a function or class."""
    try:
        return func.__name__
    except AttributeError:
        return func.__class__.__name__


def add_parentheses(s):
    """Add parentheses around the string s."""
    return ''.join(['(', s, ')'])
