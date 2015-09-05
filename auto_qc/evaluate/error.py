import fn.iters as it
import string   as st
from fn import F, _

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


def check_node_paths(nodes, analyses, status):
    """
    Set an error message in the status if node variable paths are not valid.
    """

    def f(node):
        paths  = reduce(fetch_paths, node, [])
        errors = list(it.compact(map(eval_path, paths)))
        if len(errors) > 0:
            return errors

    def fetch_paths(acc, n):
        if var.is_variable(n):
            return acc + [n]
        elif isinstance(n, list):
            return reduce(fetch_paths, n, acc)
        else:
            return acc

    def eval_path(p):
        namespace, path = var.split_into_namespace_and_path(p)
        analysis = var.get_analysis(status[analyses], p)
        if analysis is None:
            return "No matching analysis called '{}' found.".format(namespace)
        try:
            variable = var.get_variable_value(analysis, p)
        except KeyError as e:
            msg = "No matching metric '{}' found in ':{}.'"
            return msg.format(st.join(path, "/"), namespace)

    errors = list(it.compact(it.flatten(map(f, status[nodes]['thresholds']))))

    if len(errors) > 0:
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
