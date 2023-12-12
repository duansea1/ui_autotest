# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023年11月月14日 15:40
# ---
"""
fixture详解：https://zhuanlan.zhihu.com/p/443523226
name: @pytest.fixture(name="sea") def login(log):-----则调用login需要传递修改后的function名称sea
scope: 用于控制fixture的作用范围（
                session：主要作用于会话级别
                nodule：作用于模块级别
                class：作用于class中，表示每个前置和后置都会执行一次
                package：主要应用于每个包下的fixture
）

"""

import pytest

"""当设置为True的时候表示该fixture在当前作用范围内(fixture默认是function)，全部执行。
@pytest.fixture(scope='class', autouse=True)--作用域是class、autouse为true，则默认class执行一次
"""
@pytest.fixture(scope='class', autouse=True)
def login():
    print('登录操作')
    yield
    print("login out !")


class Test_Login(object):
    def test_01(self):
        print('需要用到登录！')
        assert 1 == 1

    def test_02(self):
        print('不需要登录！')

    def test_03(self):   # fixture还能一起多个使用。使用的执行顺序取决于传入的顺序：先传的先执行！
        print('这里需要用到登录03！')
        assert 1 == 1
        print('断言失败')

if __name__ == '__main__':
    """
    在命令行参数上加上--setuo-show进行详细打印出fixture在具体那条用例上进行生效。
    多个fixture同时使用
　　fixture不仅仅能单个使用，还能一起使用。使用的执行顺序取决于你传入的顺序决定，意思就是，先传的先执行。
    """
    # 在命令行参数上加上--setuo-show进行详细打印
    pytest.main(['-vs', ])

