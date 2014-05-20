import operator as op

OPERATORS = {
    'greater_than': op.gt,
    'less_than'   : op.lt,
        }

def destructure_node(n):
    id_       = n['node']['id']
    namespace = n['node']['analysis']
    metric    = n['node']['metric']
    threshold = n['node']['threshold']
    operator  = OPERATORS[n['node']['operator']]
    return [id_, namespace, metric, threshold, operator]

def node_fail(n):
    return n['node']['fail']

def metric_value(n):
    return n['node']['metric_value']
