import auto_qc.util.file_system as fs
import auto_qc.util.workflow    as flow

method_chain = [
    (fs.check_for_file, ['analysis_file']),
    (fs.check_for_file, ['threshold_file']),
        ]

def run(args):
    status = flow.thread_status(method_chain, args)
    flow.exit_status(status)
