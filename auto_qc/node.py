import operator      as op
from fn import iters as it
from fn import F

import auto_qc.variable        as var
import auto_qc.util.functional as fn

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
    Replace all variables in a node s-expression with their referenced literal
    value.

    Args:
      analysis (dict): A dictionary corresponding to the values referenced in the
      given s-expression.

      node (list): An s-expression list in the form of [operator, arg1, arg2, ...].

    Yields:
      A node expression with referenced values replaced with their literal values.

    Examples:
      >>> eval_variables({a: 1}, [>, :a, 2])
      [>, 1, 2]
    """
    def _eval(n):
        if var.is_variable(n):
            return var.variable(analyses, n)
        else:
            return n

    return map(fn.recursive_apply(F(eval_variables, analyses), _eval), node)

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
    if isinstance(it.head(node), dict):
        return eval(list(it.tail(node)))
    else:
        args = map(fn.recursive_apply(eval), it.tail(node))
        f = operator(it.head(node))
        return apply(f, args)
