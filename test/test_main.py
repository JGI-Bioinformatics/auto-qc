from nose.tools import *
import auto_qc.main as aq

def test_evaluate_threshold_node_with_gt():
    node = {'node': {
      'id'        : 'id',
      'analysis'  : 'object_1',
      'operator'  : 'greater_than',
      'metric'    : 'metric_1/value',
      'threshold' : 0
            }}
    analyses = [{
      'analysis': 'object_1',
      'outputs': {
          'metric_1': {'value': 1}
          }
      }]
    resolved = aq.resolve_node(analyses, node)
    assert_true(resolved['node']['fail'])
    assert_equal(resolved['node']['metric_value'], 1)

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

def test_check_node_paths_valid_node():
    node = {'node': {
      'analysis' : 'object_1',
      'id'       : 'test_node',
      'operator' : 'greater_than',
      'metric'   : 'metric_1/value',
      'threshold': 0 }}
    analyses = [{
      'analysis': 'object_1',
      'outputs' : { 'metric_1': {'value': 1} } }]
    assert_equal(aq.check_node_metric_paths(analyses, node), None)

def test_check_node_paths_with_missing_analysis():
    node = {'node': {
      'analysis': 'missing_object',
      'id':       'test_node',
      'operator': 'greater_than',
      'metric':   'metric_1/value',
      'threshold': 0 }}
    analyses = [{
      'analysis': 'object_1',
      'outputs' : { 'metric_1': {'value': 1} } }]
    assert_equal(aq.check_node_metric_paths(analyses, node),
        "No matching analysis 'missing_object' found for node 'test_node.'")

def test_check_node_paths_with_missing_path():
    node = {'node': {
      'analysis': 'object_1',
      'id':       'test_node',
      'operator': 'greater_than',
      'metric':   'metric_1/no_path',
      'threshold' : 0 }}
    analyses = [{
      'analysis': 'object_1',
      'outputs' : { 'metric_1': {'value': 1} } }]
    assert_equal(aq.check_node_metric_paths(analyses, node),
        "No matching metric 'metric_1/no_path' found for node 'test_node.'")

