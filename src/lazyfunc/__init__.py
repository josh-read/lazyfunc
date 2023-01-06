from importlib.metadata import version

from .lazy_func import LazyFunc


__version__ = version("lazyfunc")
__all__ = ["__version__", "LazyFunc"]
