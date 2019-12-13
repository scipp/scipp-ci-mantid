import scipp as sc
import mantid.simpleapi as mantid


def test_dummy_pass():
    print("hello world!")
    assert True


def test_dummy_fail():
    print("hello world!")
    assert False
