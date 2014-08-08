import operator      as op
from fn import iters as it

OPERATORS = {
    'greater_than': op.gt,
    'less_than'   : op.lt,
    'and'         : lambda *args: all(args),
    'or'          : lambda *args: any(args),
        }

def operator(v):
    return OPERATORS[v]

def variable(analyses, v):
    path = v[1:].split('/')

    namespace = it.head(path)
    analysis  = it.head(filter(lambda x: x['analysis'] == namespace, analyses))
    rest      = it.tail(path)
    return reduce(lambda a, k: a[k], rest, analysis['outputs'])

def eval_variables(analyses, node):
    """
    Replace all variables in a node with their referenced literal value.
    """
    def _eval(n):
        if isinstance(n, basestring) and it.head(n) == ':':
            return variable(analyses, n)
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
