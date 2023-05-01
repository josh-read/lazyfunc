<h1 align="center">lazyfunc</h1>

<p align="center">Operations between callables, with <a href="https://en.wikipedia.org/wiki/Lazy_evaluation">lazy evaluation</a>.</p>

<p align="center">
  <a href="https://github.com/josh-read/lazyfunc/actions/workflows/ci.yml"><img
    src="https://img.shields.io/github/actions/workflow/status/josh-read/lazyfunc/ci.yml?label=ci"
    alt="ci"
  /></a>
  <a href="https://josh-read.github.io/lazyfunc/"><img
    src="https://img.shields.io/badge/docs-mkdocs-blue"
    alt="docs"
  /></a>
  <a href="https://pypi.org/project/lazyfunc/"><img
    src="https://img.shields.io/pypi/v/lazyfunc"
    alt="pypi"
  /></a>
  <a href="https://codecov.io/gh/josh-read/lazyfunc"><img
    src="https://codecov.io/gh/josh-read/lazyfunc/branch/main/graph/badge.svg?token=NPHWZRHO4C"
    alt="codecov"
  /></a>
</p>

______________________________________________________________________

## Installation

To install lazyfunc,
use [pip](https://pip.pypa.io/)
to install the latest version from PyPI.

```commandline
$ pip install lazyfunc
```

## Usage

Below is a short demo of `lazyfunc`.
[Arbitrary operations](https://josh-read.github.io/lazyfunc/reference/)
can be applied to the functions
and even between each other.
Function evaluation is deferred
until after the final function is constructed.

```python
>>> from lazyfunc import LazyFunc

>>> @LazyFunc
... def f(x):
...     return 2 * x

>>> @LazyFunc
... def g(x):
...     return x ** 2

>>> combined_function = f * (g + 2) ** 2
>>> combined_function
LazyFunc(f * (g + 2) ** 2)

>>> combined_function(1) == 18
True

```

See the [example](https://github.com/josh-read/lazyfunc/blob/main/examples/photometrics/main.py)
for a more motivating use case.

## Contributing

All contributions are welcome!
Please raise an issue or make a pull request.
