import operator      as op
from fn import iters as it

OPERATORS = {
    'greater_than': op.gt,
    'less_than'   : op.lt,
        }

def literal(v):
    return v

def operator(v):
    return OPERATORS[v]

def variable(analyses, v):
    path = v.split('/')
    namespace = it.head(path)
    rest      = it.tail(path)
    analysis = it.head(filter(lambda x: x['analysis'] == namespace, analyses))
    return reduce(lambda a, k: a[k], rest, analysis['outputs'])

def resolve(analyses, node):

    def _resolve(n):
        type_ = n['node']
        value = n['value']
        if type_ == 'literal':
            return literal(value)
        elif type_ == 'operator':
            return operator(value)
        elif type_ == 'variable':
            return variable(analyses, value)

    expr = map(_resolve, node)
    f    = it.head(expr)
    args = it.tail(expr)
    return f(*args)
