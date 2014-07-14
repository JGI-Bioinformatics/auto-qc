import auto_qc.util.file_system as fs
import auto_qc.util.workflow    as flow
import auto_qc.printers         as prn
import auto_qc.node             as node
import functools                as ft

from fn import F
from fn import iters as it

def evaluate_nodes(destination, status):
    """
    Runs through a list of nodes and evaluates each one
    """
    nodes    = status['thresholds']['thresholds']
    analyses = status['analyses']
    f = F(node.resolve, analyses)
    status[destination] = map(f, nodes)
    return status

method_chain = [
    (fs.check_for_file, ['analysis_file']),
    (fs.check_for_file, ['threshold_file']),
    (fs.read_yaml_file, ['threshold_file', 'thresholds']),
    (fs.read_yaml_file, ['analysis_file',  'analyses']),
    (evaluate_nodes,    ['node_results'])
        ]

def run(args):
    status = flow.thread_status(method_chain, args)
    flow.exit_if_error(status)

    nodes_failing = status['node_results']

    if any(nodes_failing):
        print 'FAIL'
    else:
        print 'PASS'

