import auto_qc.util.file_system as fs
import auto_qc.util.workflow    as flow
import auto_qc.printers         as prn
import operator                 as op
import functools                as ft

from fn import F
from fn import iters as it

OPERATORS = {
    'greater_than': op.gt,
    'less_than'   : op.lt,
        }

def check_node_metric_paths(analyses, n):
    metric    = n['node']['metric']
    namespace = n['node']['analysis']
    id_       = n['node']['id']

    analysis = filter(lambda x: x['analysis'] == namespace, analyses)
    if len(analysis) == 0:
        return "No matching analysis '{}' found for node '{}.'".\
                format(namespace, id_)

    for a in analysis:
        try:
            reduce(lambda a, k: a[k], metric.split('/'), a['outputs'])
        except KeyError, _:
            return "No matching metric '{}' found for node '{}.'".\
                    format(metric, id_)

def evaluate_threshold_node(analyses, node):
    n = node['node']
    metric          = n['metric']
    threshold       = n['threshold']
    namespace       = n['analysis']
    value           = find_analysis_value(analyses, namespace, metric)
    f               = OPERATORS[n['operator']]
    return f(value, threshold)

def find_analysis_value(analyses, namespace, metric_path):
    analysis = filter(lambda x: x['analysis'] == namespace, analyses)[0]
    outputs = analysis['outputs']
    return reduce(lambda k, v: k[v], metric_path.split('/'), outputs)

def check_nodes(analyses, thresholds, status):
    nodes    = status['thresholds']['thresholds']
    analyses = status['analyses']
    errors = filter(lambda i: i is not None,
            map(F(check_node_metric_paths, analyses), nodes))
    if len(errors) > 0:
        status['error'] = "\n".join(errors)
    return status

def evaluate_nodes(destination, status):
    nodes    = status['thresholds']['thresholds']
    analyses = status['analyses']
    def update_node(n):
         n['node']['fail'] = evaluate_threshold_node(analyses, n)
         return n
    status[destination] = map(update_node, nodes)
    return status

method_chain = [
    (fs.check_for_file, ['analysis_file']),
    (fs.check_for_file, ['threshold_file']),
    (fs.read_yaml_file, ['threshold_file', 'thresholds']),
    (fs.read_yaml_file, ['analysis_file',  'analyses']),
    (check_nodes,       ['analyses', 'thresholds']),
    (evaluate_nodes,    ['node_results']),
        ]

def run(args):
    status = flow.thread_status(method_chain, args)
    flow.exit_if_error(status)

    if not args['yaml']:
        msg = prn.simple(status)
    else:
        msg = prn.yaml(status)

    print msg
