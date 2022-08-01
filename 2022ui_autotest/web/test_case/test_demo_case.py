
import pytest


def test_fail():
    a, b = 1, 2
    assert a == b


def test_error():
    pass


@pytest.mark.xfail(reason='always xpass')
def test_xpass():
    pass


@pytest.mark.xfail(reason='always xfail')
def test_xfail():
    assert False


@pytest.mark.skip(reason="skip the case")
def test_skip():
    pass


pytest.main(["-vrA", "-s"])
