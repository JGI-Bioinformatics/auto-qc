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
    rest      = it.tail(path)
    analysis = it.head(filter(lambda x: x['analysis'] == namespace, analyses))
    return reduce(lambda a, k: a[k], rest, analysis['outputs'])

def resolve(analyses, node):

    def _resolve(n):
        if isinstance(n, basestring) and it.head(n) == ':':
            return variable(analyses, n)
        elif isinstance(n, list):
            return resolve(analyses, n)
        else:
            return n

    f    = operator(it.head(node))
    args = map(_resolve, it.tail(node))
    return f(*args)
