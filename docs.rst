No inplace operators.
---------------------

The two lines marked with arrows lead to an infinite loop of creating a function that depends on self,
which is then assigned to self. This is a problem because the wrapped functions are passed by reference rather
than by value. One solution would be to create a copy of the old self, however this uses the same amount of
memory as the non-inplace operation defeating the point. An alternative would be to simply call the non-inplace
operation with the inplace syntax, however this would then be misleading. As a result inplace operations are not
implemented for LazyFunc objects.
