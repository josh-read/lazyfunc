class MathFunc:

    def __init__(self, func, *args, description=None, **kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        self._description = description

    @property
    def description(self):
        if self._description is None:
            try:
                return self.func.__name__
            except AttributeError:
                return self.func.__class__.__name__
        else:
            return self._description

    def __repr__(self):
        return f"{self.__class__.__name__}({self.description})"

    def __call__(self, *x):
        return self.func(*x, *self.args, **self.kwargs)
