import auto_qc.variable as var
import auto_qc.node     as node
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
    status[destination] = map(node.eval, nodes)
    return status

def build_qc_dict(destination, thresholds, nodes, results, status):
    """
    Build a dict QC containing all data about this evaluation.
    """
    qc_dict = status[thresholds].copy()
    qc_dict['state'] = {'fail': not all(status[results])}
    qc_dict['evaluation'] = status[nodes]

    status[destination] = qc_dict
    return status

def create_variable_dict(input_node, analysis):
    f = lambda x: (x, var.get_variable_value(analysis, x))
    return dict(map(f, var.get_variable_names(input_node)))

def build_qc_node(input_node, analysis):
    return {'variables' : create_variable_dict(input_node, analysis)}
