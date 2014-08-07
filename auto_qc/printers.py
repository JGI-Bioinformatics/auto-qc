import auto_qc.util.metadata as meta
import auto_qc.node as node

OPERATORS = {
        'greater_than' : '>',
        'less_than'    : '<',
        'and'          : 'AND:',
        'or'           : 'OR:'
        }

def simple(qc_dict):
    return 'FAIL' if qc_dict['state']['fail'] else 'PASS'

def yaml(qc_dict):
    import yaml
    return yaml.dump(qc_dict, default_flow_style=False).strip()

def text(qc_dict):
    return """\
Status: {0}

{1}

Auto QC Version: {2}
    """.format(simple(qc_dict),
               text_table(threshold_row_array(qc_dict['thresholds'], qc_dict['evaluation'])),
               meta.version()).strip()

def threshold_row_array(thresholds, evaluations):

    def eval_result(n):
        return 'FAIL' if node.apply_operator(n) else ''

    def format_branch(evaluation):
        operator = evaluation[0]
        return [OPERATORS[operator], '', '', eval_result(evaluation)]

    def format_node(evaluation, threshold):
        operator, variable_value, threshold_value = evaluation
        _, variable_name, _ = threshold
        return [str(variable_name),
                OPERATORS[operator] + ' ' + str(threshold_value),
                str(variable_value),
                eval_result((evaluation)) ]

    def f(accum, (evaluation, threshold)):

        operator, _, _ = evaluation
        _, variable_name, _ = threshold

        if operator in ["and", "or"]:
            return accum + \
                [format_branch(evaluation)] + \
                reduce(f, zip(evaluation, threshold)[1:], [])
        else:
            return accum + [format_node(evaluation, threshold)]

    return reduce(f, zip(evaluations, thresholds), [])


def text_table(rows):
    header = [['', 'Failure At', 'Actual', ''], ['', '', '', '']]
    values = header + rows

    max_col_1 = max([12] + map(lambda i: len(i[0]), values))
    max_col_2 = max(map(lambda i: len(i[1]), values))
    max_col_3 = max(map(lambda i: len(i[2]), values))

    def padd((col_1, col_2, col_3, col_4)):
        return (col_1.ljust(max_col_1, ' ') + "   " +\
                col_2.rjust(max_col_2, ' ') + "   " +\
                col_3.rjust(max_col_3, ' ') + "   " +\
                col_4).rstrip()

    return "\n".join(map(padd, values)).rstrip()
