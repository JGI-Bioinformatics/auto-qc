import auto_qc.node as nd
import operator     as op

OPERATOR_STRING = {
        op.gt : '>',
        op.lt : '<'
        }

def simple(qc_dict):
    return 'FAIL' if qc_dict['state']['fail'] else 'PASS'

def yaml(qc_dict):
    import yaml
    return yaml.dump(qc_dict, default_flow_style=False).strip()

def text(status):
    return """\
Status: {0}

{1}

Auto QC Version: {2}
    """.format(simple(status),
               text_threshold_table(status['node_results']),
               version()).strip()

def text_threshold_table(nodes):
    header = [['', 'Failure At', 'Actual', ''], ['', '', '', '']]

    def f(node):
        id_, _, _, threshold, oper = nd.destructure_node(node)
        pass_fail = 'FAIL' if nd.node_fail(node) else ''
        value = nd.metric_value(node)
        return [id_ + ':',
                OPERATOR_STRING[oper] + ' ' + "{:,}".format(threshold),
                "{:,}".format(value),
                pass_fail]

    values = header + map(f, nodes)

    max_col_1 = max([12] + map(lambda i: len(i[0]), values))
    max_col_2 = max(map(lambda i: len(i[1]), values))
    max_col_3 = max(map(lambda i: len(i[2]), values))

    def padd((col_1, col_2, col_3, col_4)):
        return (col_1.ljust(max_col_1, ' ') + "   " +\
                col_2.rjust(max_col_2, ' ') + "   " +\
                col_3.rjust(max_col_3, ' ') + "   " +\
                col_4).rstrip()


    return "\n".join(map(padd, values)).rstrip()
