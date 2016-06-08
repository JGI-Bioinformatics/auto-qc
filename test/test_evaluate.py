from nose.tools import *
import auto_qc.evaluate.qc as qc

def test_build_qc_node_with_two_literals():
    n = [{}, '>', 2, 1]
    expected = {'variables' : {}}
    assert_equal(qc.build_qc_node(n, {}), expected)

def test_build_qc_node_with_literal_and_variable():
    n = [{}, '<', ':ref/metric_1', 1]
    a = {'metadata' : {},
         'data' : {
           'ref' : {
             'metric_1' : 2 }}}
    expected = {'variables' : {':ref/metric_1' : 2}}
    assert_equal(qc.build_qc_node(n, a), expected)
