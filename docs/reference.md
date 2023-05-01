At the core of `lazyfunc` is the `LazyFunc` class.
It makes operations between callables and arbitrary datatypes possible,
by deferring evaluation to a later time.

The methods and properties of the `LazyFunc` class are listed below.

## LazyFunc

::: lazyfunc.LazyFunc

### No inplace operators.

Note that there are no inplace operators available.
This is because to do so
requires a new function be created that depends on `self`,
which is then assigned to `self`.
This is a problem
because functions are passed by reference
rather than by value,
hence the inplace operator calls itself leading to infinite recursion.

One solution would be to create a copy of the old `self`,
however this uses the same amount of memory as the non-inplace operation,
therefore defeating the point.
An alternative would be to simply call the non-inplace operation behind the scenes,
however this would be misleading.
As a result,
no inplace operations are not implemented for LazyFunc objects.
