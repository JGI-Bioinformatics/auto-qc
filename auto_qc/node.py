import operator      as op
from fn import iters as it
from fn import F

import auto_qc.variable as var

OPERATORS = {
    'greater_than': op.gt,
    'less_than'   : op.lt,
    'equals'      : op.eq,
    'not_equals'  : op.ne,
    'and'         : lambda *args: all(args),
    'or'          : lambda *args: any(args),
    'is_in'       : lambda x, y: x in y,
    'is_not_in'   : lambda x, y: x not in y,
    'list'        : lambda *args: list(args)
        }

def is_operator(v):
    return op.contains(OPERATORS.keys(), v)

def operator(v):
    return OPERATORS[v]

def eval_variables(analyses, node):
    """
    Replace all variables in a node with their referenced literal value.
    """
    def _eval(n):
        if var.is_variable(n):
            return var.variable(analyses, n)
        elif isinstance(n, list):
            return eval_variables(analyses, n)
        else:
            return n

    return map(_eval, node)

def eval(node):
    """
    Evaluate an s-expression by applying the operator to the rest of the arguments.

    Args:
      node (list): An s-expression list in the form of [operator, arg1, arg2, ...]

    Yields:
      The result of "applying" the operator to the arugments. Will evaluate
      recursively if any of the args are a list.

    Examples:
      >>> eval([>, 0, 1])
      FALSE
    """

    def _eval(n):
        if isinstance(n, list):
            return eval(n)
        else:
            return n

    args = map(_eval, it.tail(node))
    f    = operator(it.head(node))
    return apply(f, args)
