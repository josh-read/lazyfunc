<h1 align="center">lazyfunc</h1>

<p align="center">Wrapper for callables in Python, enabling many operations between them, with lazy evaluation.</p>

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
</p>

---

**Table of Contents**

- [Documentation](#documentation)
- [Usage](#usage)
- [Installation](#installation)

## Documentation

For documentation, visit [https://josh-read.github.io/lazyfunc/](https://josh-read.github.io/lazyfunc/).

## Usage

Below is an example using `lazyfunc`. While not the most motivating example, it illustrates how function evaluation can
be deferred until after the final function is constructed. A real example of when this can be advantageous is for
performing operations between interpolated functions without losing precision.

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

## Installation

```console
pip install lazyfunc
```
