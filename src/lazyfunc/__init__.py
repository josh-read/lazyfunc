from importlib.metadata import version

__version__ = version("lazyfunc")

# avoids unused variable warning
__all__ = ["__version__"]

from .lazy_func import LazyFunc
