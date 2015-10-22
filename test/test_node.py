from nose.tools import *
import auto_qc.node as node

def test_eval_greater_than_with_two_literals():
    n = ['>', 2, 1]
    assert_true(node.eval(n))

def test_eval_less_than_with_two_literals():
    n = ['<', 2, 1]
    assert_false(node.eval(n))

def test_eval_true_with_nested_lists():
    n = ['and', ['>', 2, 1],['>', 2, 1]]
    assert_true(node.eval(n))

def test_eval_false_with_nested_lists():
    n = ['and', ['>', 1, 2],['>', 1, 2]]
    assert_false(node.eval(n))

def test_eval_with_list():
    n = ['list', 2, 1]
    assert_equal([2, 1], node.eval(n))

def test_eval_with_in():
    n = ['in', 2, ['list', 2, 1]]
    assert_true(node.eval(n))

def test_eval_with_not_in():
    n = ['not_in', 2, ['list', 2, 1]]
    assert_false(node.eval(n))

def test_eval_variable_with_literal_and_variable():
    n = ['<', ':ref/metric_1', 1]
    a = {'metadata' : {},
         'data' : {
           'ref' : {
             'metric_1' : 2 }}}
    assert_equal(['<', 2, 1], node.eval_variables(a, n))

def test_eval_variable_with_nested_list():
    n = ['and', ['<', ':ref/metric_1', 1], ['<', ':ref/metric_1', 1]]
    a = {'metadata' : {},
         'data' : {
           'ref' : {
             'metric_1' : 2 }}}

    assert_equal(['and', ['<', 2, 1], ['<', 2, 1]], node.eval_variables(a, n))

def test_eval_with_doc_string():
    n = [{'name': 'my threshold'}, '>', 2, 1]
    assert_true(node.eval(n))
