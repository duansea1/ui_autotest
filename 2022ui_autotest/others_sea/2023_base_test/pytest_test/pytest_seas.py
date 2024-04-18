# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2024-03-15 9:11
# ---

import pytest

@pytest.mark.parametrize('a, b', [(1, 2), (2, 3)])
def test_addnums(a, b):
    assert a+1 ==b

def addOne(x:int)->int:
    return x +2

from hypothesis import given, strategies as st
@given(st.integers())
def test_addsub(_input):
    assert addOne(_input) == _input +1

if __name__ == '__main__':
    pytest.main('-vs')