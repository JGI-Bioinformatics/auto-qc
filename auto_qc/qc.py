import auto_qc.node as node
from fn import F

def evaluate(destination, thresholds, analyses, status):
    """
    Map variables to their analysis file values.
    """
    nodes    = status[thresholds]['thresholds']
    analyses = status[analyses]
    f = F(node.eval_variables, analyses)
    status[destination] = map(f, nodes)
    return status

def apply_thresholds(destination, nodes, status):
    """
    Apply operations to nodes
    """
    nodes = status[nodes]
    status[destination] = map(node.apply_operator, nodes)
    return status

