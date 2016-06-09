from nose.tools import *
import auto_qc.printers               as prn
import more_assertive_nose.assertions as asrt

def test_text_printer_with_single_failing_result():
    qc_dict = {
        'evaluation' : [{'variables' : {'ref/metric_1' : 2},
                         'pass'      : False,
                         'message'   : 'fails' }],
        'pass'       : False }
    expected ="""\
FAIL

  * fails

Auto QC Version: 2.0.0
"""
    asrt.assert_diff(expected.strip(), prn.text(qc_dict))
