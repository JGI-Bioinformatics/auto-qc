from nose.tools import *
import auto_qc.node as node

def test_greater_than_with_two_literals():
    n = ['greater_than', 2, 1]
    assert_true(node.resolve({}, n))

def test_less_than_with_two_literals():
    n = ['less_than', 2, 1]
    assert_false(node.resolve({}, n))

def test_less_than_with_literal_and_variable():
    n = ['less_than', ':ref/metric_1', 1]
    a = [{'analysis' : 'ref',
          'outputs'  : {
            'metric_1' : 2 }}]
    assert_false(node.resolve(a, n))

def test_greater_than_with_literal_and_variable():
    n = ['greater_than', ':ref/metric_1', 1]
    a = [{'analysis' : 'ref',
          'outputs'  : {
            'metric_1' : 2 }}]
    assert_true(node.resolve(a, n))
