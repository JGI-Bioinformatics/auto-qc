import auto_qc.util.file_system as fs
import auto_qc.util.workflow    as flow
import auto_qc.util.workflow    as flow
import operator                 as op
import functools                as ft
import yaml

from fn import iters as it

OPERATORS = {
    'greater_than': op.gt,
        }

def evaluate_threshold_node(analyses, node):
    n = node['node']
    path, threshold = n['args']
    namespace       = n['analysis']
    value           = find_analysis_value(analyses, namespace, path)
    f               = OPERATORS[n['operator']]
    return f(value, threshold)

def find_analysis_value(analyses, namespace, path):
    analysis = filter(lambda x: x['analysis'] == namespace, analyses)[0]
    outputs = analysis['outputs']
    return reduce(lambda k, v: k[v], path.split('/'), outputs)

def evaluate_nodes(destination, status):
    nodes    = status['thresholds']['thresholds']
    analyses = status['analyses']
    def update_node(n):
         n['node']['fail'] = evaluate_threshold_node(analyses, n)
         return n
    status[destination] = map(update_node, nodes)
    return status

def metadata():
    return {'version': {'auto-qc': '0.0.0'}}



method_chain = [
    (fs.check_for_file, ['analysis_file']),
    (fs.check_for_file, ['threshold_file']),
    (fs.read_yaml_file, ['threshold_file', 'thresholds']),
    (fs.read_yaml_file, ['analysis_file',  'analyses']),
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


