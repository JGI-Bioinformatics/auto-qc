from nose.tools import *
import auto_qc.printers as prn
import assertions       as asrt

def test_single_passing_threshold():
    threshold  = [['greater_than', ':var_1', 2]]
    evaluation = [['greater_than',       1,  2]]
    expected   = [{'name'     : ':var_1',
                   'expected' : '> 2',
                   'actual'   : '1',
                   'fail'     : False}]
    assert_equal(expected, prn.row_array(zip(threshold, evaluation)))

def test_single_failing_threshold():
    threshold  = [['less_than', ':var_1', 2]]
    evaluation = [['less_than',       1,  2]]
    expected   = [{'name'     : ':var_1',
                   'expected' : '< 2',
                   'actual'   : '1',
                   'fail'     : True}]
    assert_equal(expected, prn.row_array(zip(threshold, evaluation)))

def test_multiple_passing_threshold():
    threshold  = [['greater_than', ':var_1', 2], ['greater_than', ':var_1', 2]]
    evaluation = [['greater_than',       1,  2], ['greater_than',       1,  2]]
    expected   = [{'name' : ':var_1', 'expected' : '> 2', 'actual' : '1', 'fail' : False},
                  {'name' : ':var_1', 'expected' : '> 2', 'actual' : '1', 'fail' : False}]
    assert_equal(expected, prn.row_array(zip(threshold, evaluation)))

def test_nested_failing_and_threshold():
    threshold  = [['and', ['less_than', ':var_1', 2]]]
    evaluation = [['and', ['less_than', 1, 2]]]
    expected   = [{'name' : 'AND:', 'fail': True, 'children' : [
        {'name' : ':var_1', 'expected' : '< 2', 'actual' : '1', 'fail' : True}]}]
    assert_equal(expected, prn.row_array(zip(threshold, evaluation)))

def test_multiple_nested_failing_and_threshold():
    threshold  = [['and', ['less_than', ':var_1', 2], ['less_than', ':var_1', 2]]]
    evaluation = [['and', ['less_than', 1, 2], ['less_than', 1, 2]]]
    expected   = [{'name' : 'AND:', 'fail': True, 'children' : [
        {'name' : ':var_1', 'expected' : '< 2', 'actual' : '1', 'fail' : True},
        {'name' : ':var_1', 'expected' : '< 2', 'actual' : '1', 'fail' : True},
        ]}]
    assert_equal(expected, prn.row_array(zip(threshold, evaluation)))



def test_text_table_with_single_failing_metric():
    row = [{'name'     : ':object_1/metric_1/value',
            'expected' : '< 2',
            'actual'   : '1',
            'fail'     : True}]
    expected = """\
                           Failure At   Actual

:object_1/metric_1/value          < 2        1   FAIL
""".rstrip()
    asrt.assert_diff(expected, prn.text_table(row))

def test_text_table_with_single_passing_metric():
    row = [{'name'     : ':object_1/metric_1/value',
            'expected' : '< 2',
            'actual'   : '1',
            'fail'     : False}]
    expected = """\
                           Failure At   Actual

:object_1/metric_1/value          < 2        1
""".rstrip()
    asrt.assert_diff(expected, prn.text_table(row))


def test_text_table_with_single_nested_failing_metric():
    row = [{'name' : 'AND:', 'fail': True, 'children' : [
        {'name' : ':object_1/metric_1/value', 'expected' : '< 2', 'actual' : '1', 'fail' : True}]}]

    expected = """\
                             Failure At   Actual

AND:                                               FAIL
  :object_1/metric_1/value          < 2        1   FAIL
""".rstrip()
    asrt.assert_diff(expected, prn.text_table(row))

