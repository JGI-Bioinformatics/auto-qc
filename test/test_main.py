from nose.tools                import *
from auto_qc.main import *

def test_add_two():
    assert_equal(4, add_two(2))
    assert_equal(5, add_two(3))

def test_times_three():
    assert_equal(6, times_three(2))
    assert_equal(9, times_three(3))

