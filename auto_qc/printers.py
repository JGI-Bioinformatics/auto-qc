import auto_qc.util.metadata as meta
import auto_qc.node as node
from fn import iters as it
from fn import F

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
               text_table(row_array(zip(qc_dict['thresholds'], qc_dict['evaluation']))),
               meta.version()).strip()

def row_array(n):

    def format_node((threshold, evaluation)):
        operator = it.head(evaluation)
        fail     = node.apply_operator(evaluation)

        if operator in ["or", "and"]:
            return {'name'     : OPERATORS[operator],
                    'fail'     : fail,
                    'children' : row_array(zip(it.tail(threshold), it.tail(evaluation)))
            }
        else:
            _, variable_value, threshold_value = evaluation
            _, variable_name, _ = threshold
            return {'name'     : str(variable_name),
                    'expected' : OPERATORS[operator] + ' ' + str(threshold_value),
                    'actual'   : str(variable_value),
                    'fail'     : fail}

    return reduce(lambda acc, i: acc + [format_node(i)], n, [])

def _threshold_row_array(thresholds, evaluations):

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

    values = [['', 'Failure At', 'Actual', ''], ['', '', '', '']]

    def f(indent, row):
        values.append([
             indent + row['name'],
             row.get('expected', ''),
             row.get('actual', ''),
             "FAIL" if row['fail'] else ""])
        map(F(f, indent + "  "), row.get('children', []))

    map(F(f, ""), rows)

    max_col_1 = max([12] + map(lambda i: len(i[0]), values))
    max_col_2 = max(map(lambda i: len(i[1]), values))
    max_col_3 = max(map(lambda i: len(i[2]), values))

    def padd((col_1, col_2, col_3, col_4)):
        return (col_1.ljust(max_col_1, ' ') + "   " +\
                col_2.rjust(max_col_2, ' ') + "   " +\
                col_3.rjust(max_col_3, ' ') + "   " +\
                col_4).rstrip()

    return "\n".join(map(padd, values)).rstrip()

