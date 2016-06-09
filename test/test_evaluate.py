from nose.tools import *
import auto_qc.evaluate.qc as qc
import funcy

METADATA = {
        'name'     : 'Example test',
        'pass_msg' : 'passes',
        'fail_msg' : 'fails' }


def test_build_passing_qc_node_with_two_literals():
    n = [METADATA, '>', 2, 1]
    expected = {'variables' : {},
                'pass'      : True,
                'message'   : 'passes' }
    assert_equal(qc.build_qc_node(n, {}), expected)

def test_build_failing_qc_node_with_literal_and_variable():
    n = [METADATA, '<', ':ref/metric_1', 1]
    a = {'metadata' : {},
         'data' : {
           'ref' : {
             'metric_1' : 2 }}}
    expected = {'variables' : {'ref/metric_1' : 2},
                'pass'      : False,
                'message'   : 'fails' }
    assert_equal(qc.build_qc_node(n, a), expected)


def test_build_passing_qc_node_with_interpolated_msg():
    metadata = funcy.merge(METADATA, {'fail_msg' : 'Metric is {ref/metric_1}'})
    n = [metadata, '<', ':ref/metric_1', 1]
    a = {'metadata' : {},
         'data' : {
           'ref' : {
             'metric_1' : 2 }}}
    node = qc.build_qc_node(n, a)
    assert_equal(node['message'], 'Metric is 2')
