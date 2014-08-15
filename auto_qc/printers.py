import auto_qc.util.metadata as meta
import auto_qc.node as node
from fn import iters as it
from fn import F, _
from re import sub

OPERATORS = {
        'greater_than' : '>',
        'less_than'    : '<',
        'and'          : 'AND:',
        'or'           : 'OR:',
        'equals'       : '==',
        'not_equals'   : '=/=',
        'is_in'        : 'is in',
        'is_not_in'    : 'is not in'
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

def format_threshold(thr):
    f = F() << str
    if isinstance(thr, list):
        f = f << F(sub, "'", "") << str << list << it.tail
        if len(thr) > 4:
            f = f << F(_ + ['...']) << list << F(it.take, 4)

    return f(thr)

def row_array(n):
    """
    Map thresholds and evaluations into rows
    """

    def format_node((threshold, evaluation)):
        operator = it.head(evaluation)
        value    = node.apply_operator(evaluation)

        if operator in ["or", "and"]:
            return {'name'     : OPERATORS[operator],
                    'value'    : value,
                    'children' : row_array(zip(it.tail(threshold), it.tail(evaluation)))}
        else:
            _, variable_value, threshold_value = evaluation
            _, variable_name, _ = threshold
            return {'name'     : str(variable_name),
                    'expected' : OPERATORS[operator] + ' ' + format_threshold(threshold_value),
                    'actual'   : str(variable_value),
                    'value'    : value}

    return reduce(lambda acc, i: acc + [format_node(i)], n, [])


def text_table(rows):
    """
    Convert array of nested rows to a human readable text format
    """

    values = [['', 'Failure At', 'Actual', ''], ['', '', '', '']]

    def f(indent, row):
        values.append([
             indent + row['name'],
             row.get('expected', ''),
             row.get('actual', ''),
             "FAIL" if row['value'] else ""])
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

