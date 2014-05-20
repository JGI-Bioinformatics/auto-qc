from nose.tools import *
import auto_qc.printers as prn
import assertions       as asrt

def test_text_threshold_table_with_single_value():
    node = {'node' : {
        'id'           : 'test',
        'operator'     : 'greater_than',
        'metric_value' : 2,
        'analysis'     : None,
        'metric'       : None,
        'threshold'    : 1,
        'fail'         : False
        }}
    expected = """\
               Failure At   Actual

test:                 > 1        2
    """
    asrt.assert_diff(prn.text_threshold_table([node]),
                     expected.rstrip())

def test_text_threshold_table_with_large_number():
    node = {'node' : {
        'id'           : 'test',
        'operator'     : 'greater_than',
        'metric_value' : 2000,
        'analysis'     : None,
        'metric'       : None,
        'threshold'    : 1000,
        'fail'         : True
        }}
    expected = """\
               Failure At   Actual

test:             > 1,000    2,000   FAIL
    """
    asrt.assert_diff(prn.text_threshold_table([node]),
                     expected.rstrip())

def test_text_threshold_table_with_float():
    node = {'node' : {
        'id'           : 'test',
        'operator'     : 'greater_than',
        'metric_value' : 2,
        'analysis'     : None,
        'metric'       : None,
        'threshold'    : 1.5,
        'fail'         : False
        }}
    expected = """\
               Failure At   Actual

test:               > 1.5        2
    """
    asrt.assert_diff(prn.text_threshold_table([node]),
                     expected.rstrip())
