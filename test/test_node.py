from nose.tools import *
import auto_qc.node as node

def operator(v):
    return {'node': 'operator', 'value': v}

def literal(v):
    return {'node': 'literal', 'value': v}

def variable(v):
    return {'node': 'variable', 'value': v}


def test_greater_than_with_two_literals():
    n = [operator('greater_than'),
         literal(2),
         literal(1)]
    assert_true(node.resolve({}, n))

def test_less_than_with_two_literals():
    n = [operator('less_than'),
         literal(2),
         literal(1)]
    assert_false(node.resolve({}, n))

def test_less_than_with_literal_and_variable():
    n = [operator('less_than'),
         variable('ref/metric_1'),
         literal(1)]
    a = [{'analysis' : 'ref',
          'outputs'  : {
            'metric_1' : 2 }}]
    assert_false(node.resolve(a, n))

def test_greater_than_with_literal_and_variable():
    n = [operator('greater_than'),
         variable('ref/metric_1'),
         literal(1)]
    a = [{'analysis' : 'ref',
          'outputs'  : {
            'metric_1' : 2 }}]
    assert_true(node.resolve(a, n))
