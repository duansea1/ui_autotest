# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-11-15 16:08
# ---
import pytest
import time

# 原文链接：https://blog.csdn.net/wy_hhxx/article/details/126576341

class TestAPI:
    a = 5

    def test01set(self):
        print("Test-03 ------set function.")
        time.sleep(0.5)

    @pytest.mark.skip(reason="跳过case4")
    def test02four(self):
        print("Test-04 ------four function.")
        time.sleep(0.5)

    @pytest.mark.skipif(a == 5, reason="休息")
    @pytest.mark.run(order=2)
    def test03get(self):
        print("Test-1 get function.")
        time.sleep(1)
        assert 1 == 1

    # @pytest.mark.run(order=1)
    @pytest.mark.xfail(False, reason="预期失败")
    def test04set(self):
        print("Test-2 set function.")
        time.sleep(0.5)

if __name__ == "__main__":

    pytest.main('-vsk')  # '-q','-reruns=2'
    """
    # pytest \pytest_test\test_api01.py -q -v --html 1.html    输出html的报告
    # pytest.mark.skip() ---跳过用例
    # Pytest.mark.ifskip(a=5, reason='跳过'） ---如果a=5，则跳过该用例
    
    """

