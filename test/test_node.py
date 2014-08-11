from nose.tools import *
import auto_qc.node as node

def test_apply_operator_greater_than_with_two_literals():
    n = ['greater_than', 2, 1]
    assert_true(node.apply_operator(n))

def test_apply_operator_less_than_with_two_literals():
    n = ['less_than', 2, 1]
    assert_false(node.apply_operator(n))

def test_apply_operator_true_with_nested_lists():
    n = ['and', ['greater_than', 2, 1],['greater_than', 2, 1]]
    assert_true(node.apply_operator(n))

def test_apply_operator_false_with_nested_lists():
    n = ['and', ['greater_than', 1, 2],['greater_than', 1, 2]]
    assert_false(node.apply_operator(n))


def test_eval_variable_with_literal_and_variable():
    n = ['less_than', ':ref/metric_1', 1]
    a = [{'analysis' : 'ref',
          'outputs'  : {
            'metric_1' : 2 }}]
    assert_equal(['less_than', 2, 1], node.eval_variables(a, n))

def test_eval_variable_with_nested_list():
    n = ['and', ['less_than', ':ref/metric_1', 1], ['less_than', ':ref/metric_1', 1]]
    a = [{'analysis' : 'ref',
          'outputs'  : {
            'metric_1' : 2 }}]

    assert_equal(['and', ['less_than', 2, 1], ['less_than', 2, 1]], node.eval_variables(a, n))
