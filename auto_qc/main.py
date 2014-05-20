import auto_qc.util.file_system as fs
import auto_qc.util.workflow    as flow
import auto_qc.util.workflow    as flow
import operator                 as op
import functools                as ft
import yaml

from fn import F
from fn import iters as it

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

def check_node_metric_paths(analyses, n):
    id_, namespace, metric, _, _ = destructure_node(n)

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

def resolve_node(analyses, n):
    _, namespace, metric, threshold, f = destructure_node(n)
    value = find_analysis_value(analyses, namespace, metric)
    n['node']['metric_value'] = value
    n['node']['fail']         = f(value, threshold)
    return n

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
    f = F(resolve_node, analyses)
    status[destination] = map(f, nodes)
    return status

def metadata():
    return {'version': {'auto-qc': version()}}

def version():
    import os
    path = os.path.join(os.path.dirname(__file__), '../VERSION')
    with open(path, 'r') as f:
        return f.read().strip()

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

    failing = map(lambda n: n['node']['fail'], status['node_results'])

    if not args['yaml']:
        msg = 'FAIL' if any(failing) else 'PASS'
    else:
        output = {
            'fail'      : any(failing),
            'metadata'  : metadata(),
            'thresholds': status['node_results']
        }
        msg = yaml.dump(output, default_flow_style=False)

    print msg

