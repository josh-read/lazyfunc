from importlib.metadata import version, PackageNotFoundError

__version__ = version("lazyfunc")

# __all__ = ["__version__"]

from .lazy_func import LazyFunc
