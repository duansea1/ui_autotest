# -- coding: utf-8 --
import pytest

from pytest_assume.plugin import assume


def test_assume():
    a, b = 1, 2
    pytest.assume(1 == 3)
    with assume: assert a == b
    with assume: assert a > b
    with assume: assert a < b
    print("done")


@pytest.mark.slow
def test_assume_01():
    a, b = 1, 2
    pytest.assume(1 == 3)
    with assume: assert a+b == b

    print("done")

if __name__ == "__main__":
    pytest.main(["-vrA", "-vs"])