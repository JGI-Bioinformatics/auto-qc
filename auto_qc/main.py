import auto_qc.util.file_system as fs
import auto_qc.util.workflow    as flow
import auto_qc.printers         as prn
import auto_qc.qc               as qc
import auto_qc.util.metadata    as meta


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

    (fs.read_yaml_file,    ['analysis_file',  'analyses']),
    (qc.evaluate,          ['evaluated_nodes', 'thresholds', 'analyses']),
    (qc.apply_thresholds,  ['node_results', 'evaluated_nodes']),
    (qc.build_qc_dict,     ['qc_dict', 'thresholds', 'evaluated_nodes', 'node_results'])
        ]

def run(args):
    status = flow.thread_status(method_chain, args)
    flow.exit_if_error(status)

    if args['yaml']:
        f = prn.yaml
    else:
        f = prn.simple

    print f(status['qc_dict'])
