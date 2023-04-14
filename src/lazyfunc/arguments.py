import inspect


def new_diadic_function(operator, *instances):

    f, g = instances

    f_params = inspect.signature(f).parameters
    g_params = inspect.signature(g).parameters

    # build new function
    def h(*args, **kwargs):
        f_kwargs = {}
        g_kwargs = {}
        for key in kwargs:
            if key in f_params:
                f_kwargs[key] = kwargs[key]
            if key in g_params:
                g_kwargs[key] = kwargs[key]
        return operator.func(f(*args, **f_kwargs), g(*args, **g_kwargs))

    # build new signature
    combined_params = {}

    argument_order = [
        inspect.Parameter.POSITIONAL_ONLY,
        inspect.Parameter.POSITIONAL_OR_KEYWORD,
        inspect.Parameter.VAR_POSITIONAL,
        inspect.Parameter.KEYWORD_ONLY,
        inspect.Parameter.VAR_KEYWORD,
    ]

    for kind in argument_order:
        for name, param in f_params.items():
            if param.kind == kind and name not in combined_params:
                combined_params[name] = param
        for name, param in g_params.items():
            if param.kind == kind and name not in combined_params:
                combined_params[name] = param
    h.__signature__ = inspect.Signature(parameters=combined_params.values())
    return h
