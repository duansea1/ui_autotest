# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2023年10月月20日 9:40
# ---
import pytest

@pytest.fixture()
def login(log):
    print('登录操作')
    yield
    print("login out !")

@pytest.fixture()
def log():
    print('打开日志功能！')
    yield
    print('关闭日志功能！')


class Test_Login():
    def test_01(self, login, log):
        print('需要用到登录！')
        assert 1==1

    def test_02(self):
        print('不需要登录！')

    def test_03(self, login):
        print('这里需要用到登录！')
        assert 1 == 2
        print('断言失败')


if __name__ == '__main__':
    """
    在命令行参数上加上--setuo-show进行详细打印出fixture在具体那条用例上进行生效。
    多个fixture同时使用
　　fixture不仅仅能单个使用，还能一起使用。使用的执行顺序取决于你传入的顺序决定，意思就是，先传的先执行。
    """
    pytest.main(['-vs', '--setuo-show'])
