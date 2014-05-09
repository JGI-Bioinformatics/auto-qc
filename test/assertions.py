def assert_diff(str1,str2):
    from difflib    import Differ
    from string     import join
    from nose.tools import assert_equal, assert_is_instance

    assert_is_string(str1)
    assert_is_string(str2)

    diff = Differ().compare(str1.split("\n"), str2.split("\n"))
    str_diff = "\n" + join(diff,"\n")
    assert_equal(str1, str2, str_diff)



def assert_permission(file_,expected):
    import os
    from os         import stat
    from nose.tools import assert_equal

    observed = oct(os.stat(file_).st_mode & 0777)
    assert_equal(expected, observed,
        "File '{}' has permission {} not {}.".format(file_, observed, expected))



def assert_is_dictionary(x):
    from types      import DictType
    from nose.tools import assert_is_instance
    assert_is_instance(x, DictType, "Should be a dictionary: {}".format(x))



def assert_is_list(x):
    from types      import ListType
    from nose.tools import assert_is_instance
    assert_is_instance(x, ListType)



def assert_is_string(x):
    from nose.tools import assert_is_instance
    assert_is_instance(x, basestring)



def assert_not_empty(x, message = "Should not be empty"):
    from nose.tools import assert_not_equal
    assert_not_equal(len(x), 0, message)



def assert_empty(xs):
    from nose.tools import assert_equal
    assert_equal(0, len(xs),
            "{} is not empty".format(str(xs)))
