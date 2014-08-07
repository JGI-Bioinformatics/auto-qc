from nose.tools import *
import auto_qc.printers as prn
import assertions       as asrt

def test_single_passing_threshold():
    threshold  = [['greater_than', ':var_1', 2]]
    evaluation = [['greater_than',       1,  2]]
    expected   = [[':var_1', '> 2', '1', '']]
    assert_equal(expected, prn.threshold_row_array(threshold, evaluation))

def test_single_failing_threshold():
    threshold  = [['less_than', ':var_1', 2]]
    evaluation = [['less_than',       1,  2]]
    expected   = [[':var_1', '< 2', '1', 'FAIL']]
    assert_equal(expected, prn.threshold_row_array(threshold, evaluation))

def test_nested_passing_and_threshold():
    threshold  = [['and', ['less_than', ':var_1', 2], ['greater_than', ':var_1', 2]]]
    evaluation = [['and', ['less_than', 1, 2], ['greater_than', 1, 2]]]
    expected   = [['AND:', '', '', ''], [':var_1', '< 2', '1', 'FAIL'], [':var_1', '> 2', '1', '']]
    assert_equal(expected, prn.threshold_row_array(threshold, evaluation))
