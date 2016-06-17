from nose.tools import *
import auto_qc.version as ver

def test_fetch_version():
    assert_not_equal(ver.fetch_version(), None)
