# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2022年10月月13日 9:25
# ---
import pytest
@pytest.mark.eval
@pytest.mark.parametrize(
    "test_input,expected",
    [("3+5", 8), pytest.param("6*9", 42, marks=pytest.mark.xfail)])
def test_eval(test_input, expected):
    print('---1:', test_input)
    print('---2:', expected)
    assert eval(test_input) == expected


pytest.main(["-vrA", "-vs", '-m=eval'])