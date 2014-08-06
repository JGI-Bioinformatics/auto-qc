import auto_qc.util.file_system as fs
import auto_qc.util.workflow    as flow
import auto_qc.printers         as prn
import auto_qc.qc               as qc
import auto_qc.util.metadata    as meta

from fn import F
from fn import iters as it

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

def check_version_number(threshold, status):
    version =  meta.major_version()
    threshold_version = str(status[threshold]['metadata']['version']['auto-qc'])

    if  version != threshold_version.split('.')[0]:
        status['error'] = """\
Incompatible threshold file syntax: {}.
Please update the syntax to version >= {}.0.0.
        """.format(threshold_version, version)

    return status

method_chain = [
    (fs.check_for_file, ['analysis_file']),
    (fs.check_for_file, ['threshold_file']),
    (fs.read_yaml_file, ['threshold_file', 'thresholds']),
    (check_version_number, ['thresholds']),

    (fs.read_yaml_file, ['analysis_file',  'analyses']),
    (evaluate,          ['evaluated_nodes', 'thresholds', 'analyses']),
    (apply_thresholds,  ['node_results', 'evaluated_nodes'])
        ]

def run(args):
    status = flow.thread_status(method_chain, args)
    flow.exit_if_error(status)

    nodes_failing = status['node_results']

    if any(nodes_failing):
        print 'FAIL'
    else:
        print 'PASS'

