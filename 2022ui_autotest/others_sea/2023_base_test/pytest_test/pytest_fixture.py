# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023年10月月20日 9:40
# ---
"""
fixture详解：https://zhuanlan.zhihu.com/p/443523226

1、fixture可以处理用例的前置操作、后置操作--可以通过yield进行区分。
yield前的代码是前置操作，yield后边的代码是用例的后置操作
2、前置操作和后置操作也可以只进行前置操作后后置操作
3、fixture如果有后置内容，无论遇到什么问题，都会进行执行后置的代码。

"""

import pytest

@pytest.fixture()
def login(log):
    print('登录操作')
    token = "new_token"
    yield token
    print("login out !")

@pytest.fixture()
def log():
    print('打开日志功能！')
    yield
    print('关闭日志功能！')

class Test_Login(object):
    def test_01(self, login):
        print('需要用到登录和token！')
        assert login == 'new_token'
        print('token断言结束！\n')

    def test_02(self):
        print('不需要登录！')

    def test_03(self, login):   # fixture还能一起多个使用。使用的执行顺序取决于传入的顺序：先传的先执行！
        print('这里需要用到登录03！')
        assert 1 == login
        print('断言失败')


"""
fixture-参数详解：
1、name参数表示可以对fixture的名称进行重命名

"""


if __name__ == '__main__':
    """
    在命令行参数上加上--setuo-show进行详细打印出fixture在具体那条用例上进行生效。
    多个fixture同时使用
　　fixture不仅仅能单个使用，还能一起使用。使用的执行顺序取决于你传入的顺序决定，意思就是，先传的先执行。
    """
    # 在命令行参数上加上--setuo-show进行详细打印
    pytest.main(['-vs', ])
