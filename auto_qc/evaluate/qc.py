import auto_qc.variable as var
import auto_qc.node     as node
from fn import F
import funcy

def build_qc_dict(destination, thresholds, analysis, status):
    """
    Build a dict QC containing all data about this evaluation.
    """
    f     = funcy.rpartial(build_qc_node, status[analysis])
    nodes = map(f, status[thresholds]['thresholds'])

    qc_dict = {'pass'       : all(map(lambda x: x['pass'], nodes)),
               'evaluation' : nodes}

    status[destination] = qc_dict
    return status

def create_variable_dict(input_node, analysis):
    f = lambda x: (x[1:], var.get_variable_value(analysis, x))
    return dict(map(f, var.get_variable_names(input_node)))

def does_node_pass(input_node, analysis):
    """
    Evaluates the PASS/FAIL status of a QC node.

    Args:
      node (list): An s-expression list in the form of [operator, arg1, arg2, ...].

      analysis (dict): A dictionary containing to the variables referenced in the
      given QC node

    Yields:
      True if the node passes QC, False if it fails QC.
    """
    return node.eval(node.eval_variables(analysis, input_node))

def create_qc_message(is_pass, input_node, variables):
    x = 'pass_msg' if is_pass else 'fail_msg'
    return funcy.get_in(input_node, [0, x]).format(**variables)


def build_qc_node(input_node, analysis):
    is_pass   = does_node_pass(input_node, analysis)
    variables = create_variable_dict(input_node, analysis)

    return {'variables' : variables,
            'name'      : funcy.get_in(input_node, [0, 'name']),
            'pass'      : is_pass,
            'message'   : create_qc_message(is_pass, input_node, variables)}
