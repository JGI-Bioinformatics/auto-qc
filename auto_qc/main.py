import auto_qc.util.file_system as fs
import auto_qc.util.workflow    as flow
import operator                 as op

method_chain = [
    (fs.check_for_file, ['analysis_file']),
    (fs.check_for_file, ['threshold_file']),
        ]

OPERATORS = {
    'greater_than': op.gt,
        }

def evaluate_threshold_node(node, analyses):
    path, threshold = node['args']
    namespace       = node['analysis']
    value           = find_analysis_value(analyses, namespace, path)
    f               = OPERATORS[node['operator']]
    return f(value, threshold)

def find_analysis_value(analyses, namespace, path):
    analysis = filter(lambda x: x['analysis'] == namespace, analyses)[0]
    outputs = analysis['outputs']
    return reduce(lambda k, v: k[v], path.split('/'), outputs)

def run(args):
    status = flow.thread_status(method_chain, args)
    flow.exit_status(status)
