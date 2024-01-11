# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2023年10月月12日 9:59
# ---
import pytest

@pytest.fixture(autouse=True)
def fixture_for_function():
    print('这是用在函数上的fixture')

def test_1():
    print("执行了test1")

def test_2():
    print("执行了test2")

if __name__ == "__main__":
    pytest.main(["-s", "-q", "./pytest_fixture_demo.py"])
