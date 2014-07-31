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

def check_version_number(threshold, status):
    import os
    version_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'VERSION'))
    with open(version_file, 'r') as f:
        version = f.read().split('.')[0]

    threshold_version = str(status[threshold]['metadata']['version']['auto-qc'])

    if  version != threshold_version.split('.')[0]:
        status['error'] = """\
Incompatible threshold file syntax: {}.
Please update the syntax to match version {}.
        """.format(threshold_version, version)

    return status

method_chain = [
    (fs.check_for_file, ['analysis_file']),
    (fs.check_for_file, ['threshold_file']),
    (fs.read_yaml_file, ['threshold_file', 'thresholds']),
    (check_version_number, ['thresholds']),

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

