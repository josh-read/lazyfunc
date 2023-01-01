def callable_name(func):
    """Return the name of any callable, regardless of whether it is a function or class."""
    try:
        return func.__name__
    except AttributeError:
        return func.__class__.__name__


def add_parentheses(s):
    """Add parentheses around the string s."""
    return ''.join(['(', s, ')'])


def insert(original_string, inserted_string, index):
    return original_string[:index] + inserted_string + original_string[index:]
