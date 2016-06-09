import auto_qc.util.metadata as meta
import funcy

def simple(qc_dict):
    return 'PASS' if qc_dict['pass'] else 'FAIL'

def generate_text_qc_list(qc_dict):
    f = lambda x: "  * " + x['message']
    return "\n".join(map(f, qc_dict['evaluation']))

def text(qc_dict):
    return """\
{0}

{1}

Auto QC Version: {2}
""".format(simple(qc_dict), generate_text_qc_list(qc_dict), meta.version()).strip()
