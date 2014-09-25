import auto_qc.util.file_system as fs
import auto_qc.util.workflow    as flow

import auto_qc.evaluate.error   as er
import auto_qc.evaluate.qc      as qc

method_chain = [
    (fs.check_for_file, ['analysis_file']),
    (fs.check_for_file, ['threshold_file']),
    (fs.read_yaml_file, ['threshold_file', 'thresholds']),
    (er.check_version_number, ['thresholds']),

    (fs.read_yaml_file,    ['analysis_file',  'analyses']),
    (er.check_node_paths,  ['thresholds', 'analyses']),
    (er.check_operators,   ['thresholds']),
    (qc.evaluate,          ['evaluated_nodes', 'thresholds', 'analyses']),
    (qc.apply_thresholds,  ['node_results', 'evaluated_nodes']),
    (qc.build_qc_dict,     ['qc_dict', 'thresholds', 'evaluated_nodes', 'node_results'])
        ]

def yaml(qc_dict):
    import yaml
    return yaml.dump(qc_dict, default_flow_style=False).strip()

def run(args):
    status = flow.thread_status(method_chain, args)
    flow.exit_if_error(status)
    print yaml(status['qc_dict'])
