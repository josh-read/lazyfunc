import inspect
import operator
from functools import cached_property


class Operator:

    def __init__(self, name):
        self.name = name

    @cached_property
    def func(self):
        return getattr(operator, self.name)

    @cached_property
    def number_of_operands(self):
        sig = inspect.signature(self.func)
        return len(sig.parameters)

    @cached_property
    def operation_format_template(self):
        operation_doc = (self.func.__doc__
                         .removeprefix('Same as ')
                         .removesuffix('.')
                         .removesuffix(', for a and b sequences')  # concat
                         .removesuffix(' (note reversed operands)'))  # contains
        return operation_doc.replace('a', '{}').replace('b', '{}').replace('c', '{}')


operators = []


for func_name, _ in inspect.getmembers(operator, inspect.isbuiltin):
    if func_name.startswith('__') and func_name.endswith('__'):
        operators.append(Operator(name=func_name))


if __name__ == '__main__':
    for op in operators:
        print(f'{op.name}, {op.func}, {op.number_of_operands}, {op.operation_format_template}')
