import nose.tools       as nt
import auto_qc.variable as var

def test_is_variable_path_valid_with_valid_path():
    path = ':ref/metric_1'
    analysis = {
      'metadata' : {},
      'data' : {
        'ref' : {
        'metric_1' : 2 }}}
    nt.assert_true(var.is_variable_path_valid(analysis, path))

def test_is_variable_path_valid_with_invalid_path():
    path = ':unknown/metric_1'
    analysis = {
      'metadata' : {},
      'data' : {
        'ref' : {
        'metric_1' : 2 }}}
    nt.assert_false(var.is_variable_path_valid(analysis, path))
