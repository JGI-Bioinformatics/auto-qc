import fn.iters as it
import string   as st
from fn import F, _

import funcy

import auto_qc.util.metadata   as meta
import auto_qc.variable        as var
import auto_qc.node            as nd
import auto_qc.util.functional as fn

def check_version_number(threshold, status):
    version =  meta.major_version()
    threshold_version = str(status[threshold]['metadata']['version']['auto-qc'])

    if  version != threshold_version.split('.')[0]:
        status['error'] = """\
Incompatible threshold file syntax: {}.
Please update the syntax to version >= {}.0.0.
        """.format(threshold_version, version)

    return status

def variable_error_message(variable):
    msg = "No matching metric '{}' found."
    return msg.format(variable)


def check_node_paths(nodes, analyses, status):
    """
    Checks all variable paths listed in the QC file are valid. Sets an error
    message in the status if not.
    """
    variables = var.get_variable_names(status[nodes]['thresholds'])
    f = funcy.partial(var.is_variable_path_valid, status[analyses])
    invalid_variables = set(funcy.remove(f, variables))

    if len(invalid_variables) > 0:
        errors = map(variable_error_message, invalid_variables)
        status['error'] = st.join(errors, "\n")

    return status


def check_operators(node_ref, status):
    nodes = status[node_ref]['thresholds']

    def _f(x):
      return map(fn.recursive_apply(_parse_list, fn.empty_list), x)

    def _parse_list(node):
        if isinstance(it.head(node), dict):
            return _parse_list(list(it.tail(node)))
        else:
            operator = it.head(node)
            rest     = it.tail(node)
            return [operator] + _f(rest)

    operators = fn.flatten(_f(nodes))

    f = F(it.map, lambda x: "Unknown operator '{}.'".format(x)) << F(it.filterfalse, nd.is_operator)

    errors = list(f(operators))
    if len(errors) > 0:
        status['error'] = st.join(errors, "\n")

    return status
