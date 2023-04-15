import inspect


ARGUMENT_ORDER = [
    inspect.Parameter.POSITIONAL_ONLY,
    inspect.Parameter.POSITIONAL_OR_KEYWORD,
    inspect.Parameter.VAR_POSITIONAL,
    inspect.Parameter.KEYWORD_ONLY,
    inspect.Parameter.VAR_KEYWORD,
]
