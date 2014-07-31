from nose.tools import *
import auto_qc.main as aq

def test_check_version_number():

    def version(v):
        return {'threshold' : {'metadata': {'version': {'auto-qc' : v}}}}

    status = aq.check_version_number('threshold', version('1.0.0'))
    assert_not_in('error', status)

    status = aq.check_version_number('threshold', version(1.0))
    assert_not_in('error', status)

    status = aq.check_version_number('threshold', version('0.1.0'))
    assert_in('error', status)
