import operator      as op
from fn import iters as it

import auto_qc.variable as var

OPERATORS = {
    'greater_than': op.gt,
    'less_than'   : op.lt,
    'and'         : lambda *args: all(args),
    'or'          : lambda *args: any(args),
        }

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

def apply_operator(node):
    """
    Resolve node value by applying the operator to arguments.
    """

    def _apply(n):
        if isinstance(n, list):
            return apply_operator(n)
        else:
            return n

    args = map(_apply, it.tail(node))
    f    = operator(it.head(node))
    return apply(f, args)
