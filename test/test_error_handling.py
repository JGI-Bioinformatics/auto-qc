from nose.tools import *
import auto_qc.error_handling as er

def test_check_version_number():

    def version(v):
        return {'threshold' : {'metadata': {'version': {'auto-qc' : v}}}}

    status = er.check_version_number('threshold', version('1.0.0'))
    assert_not_in('error', status)

    status = er.check_version_number('threshold', version(1.0))
    assert_not_in('error', status)

    status = er.check_version_number('threshold', version('0.1.0'))
    assert_in('error', status)


def test_check_node_paths_with_valid_node():
    n = [['less_than', ':ref/metric_1', 1]]
    a = [{'analysis' : 'ref',
          'outputs'  : {
            'metric_1' : 2 }}]

    status = {'nodes' : {'thresholds' : n}, 'analyses' : a}
    assert_not_in('error', er.check_node_paths('nodes', 'analyses', status))

def test_check_node_paths_with_unknown_namespace():
    n = [['less_than', ':unknown/metric_1', 1]]
    a = [{'analysis' : 'ref',
          'outputs'  : {
            'metric_1' : 2 }}]

    status = {'nodes' : {'thresholds' : n}, 'analyses' : a}
    assert_in('error', er.check_node_paths('nodes', 'analyses', status))
    assert_equal(status['error'], "No matching analysis called 'unknown' found.")

def test_check_node_paths_with_unknown_path():
    n = [['less_than', ':ref/unknown', 1]]
    a = [{'analysis' : 'ref',
          'outputs'  : {
            'metric_1' : 2 }}]

    status = {'nodes' : {'thresholds' : n}, 'analyses' : a}
    assert_in('error', er.check_node_paths('nodes', 'analyses', status))
    assert_equal(status['error'], "No matching metric 'unknown' found in ':ref.'")
