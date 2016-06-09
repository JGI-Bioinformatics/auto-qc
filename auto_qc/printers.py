import auto_qc.util.metadata as meta
import funcy

def simple(qc_dict):
    return 'PASS' if qc_dict['pass'] else 'FAIL'

def json(qc_dict):
    import json as jsn
    qc_dict['qc'] = qc_dict['evaluation']
    del qc_dict['evaluation']
    for node in qc_dict['qc']:
        del node['variables']
    qc_dict['auto_qc_version'] = meta.version()
    output = jsn.dumps(qc_dict, indent=4, sort_keys=True)
    return "\n".join(map(lambda x: x.rstrip(), output.split("\n")))

def generate_text_qc_list(qc_dict):
    f = lambda x: "  * " + x['message']
    return "\n".join(map(f, qc_dict['evaluation']))

def text(qc_dict):
    return """\
{0}

{1}

Auto QC Version: {2}
""".format(simple(qc_dict), generate_text_qc_list(qc_dict), meta.version()).strip()
