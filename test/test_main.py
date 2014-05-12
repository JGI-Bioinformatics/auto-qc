from nose.tools     import *
import auto_qc.main as aq

def test_evaluate_threshold_node_with_gt():
    node = {'node': {
      'analysis': 'object_1',
      'operator': 'greater_than',
      'args':     ['metric_1/value', 0]
            }}
    analyses = [{
      'analysis': 'object_1',
      'outputs': {
          'metric_1': {'value': 1}
          }
      }]
    assert_true(aq.evaluate_threshold_node(analyses, node))

def test_find_analysis_value():
    analyses = [{
      'analysis': 'object_1',
      'outputs' : { 'metric_1': {'value': 1} }
      },{
      'analysis': 'object_2',
      'outputs' : { 'metric_2': {'value': 2} }
      }]
    assert_equal(
        aq.find_analysis_value(analyses, 'object_1', 'metric_1/value'),
        1)
    assert_equal(
        aq.find_analysis_value(analyses, 'object_2', 'metric_2/value'),
        2)
