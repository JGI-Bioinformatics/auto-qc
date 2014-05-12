import auto_qc.util.file_system as fs
import auto_qc.util.workflow    as flow
import operator                 as op
import functools                as ft
import yaml

method_chain = [
    (fs.check_for_file, ['analysis_file']),
    (fs.check_for_file, ['threshold_file']),
    (fs.read_file_contents, ['threshold_file', 'thresholds']),
    (fs.read_file_contents, ['analysis_file',  'analyses']),
        ]

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

def run(args):
    status = flow.thread_status(method_chain, args)
    flow.exit_if_error(status)

    thresholds = yaml.load(status['thresholds'])
    analyses   = yaml.load(status['analyses'])
    nodes      = thresholds['thresholds']

    f          = ft.partial(evaluate_threshold_node, analyses)
    failing    = map(f, nodes)

    if any(failing):
        print 'FAIL'
    else:
        print 'PASS'
