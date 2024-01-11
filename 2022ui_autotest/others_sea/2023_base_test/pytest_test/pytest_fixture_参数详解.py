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
                module：作用于模块级别
                class：作用于class中，表示每个前置和后置都会执行一次
                package：主要应用于每个包下的fixture
）

"""

import pytest

@pytest.fixture(scope='session')
def fix_session():
    print('\n这是属于session')
    yield
    print("\nsession")

@pytest.fixture(scope='class')
def fix_class():
    print('\n这是属于class')
    yield
    print('\nclass！')

@pytest.fixture(scope='function')
def fix_function():
    print('\n这是属于function')
    yield
    print('\nfunction！')

@pytest.fixture(scope='module')
def fix_module():
    print('\n这是属于module')
    yield
    print('\nmodule！')

class Test_Login(object):
    def test_01(self, fix_function, fix_class, fix_session, fix_module):
        print('用例1--用例1--')
        assert 1 == 1

if __name__ == '__main__':
    """
    在命令行参数上加上--setuo-show进行详细打印出fixture在具体那条用例上进行生效。
    多个fixture同时使用
　　fixture不仅仅能单个使用，还能一起使用。使用的执行顺序取决于你传入的顺序决定，意思就是，先传的先执行。
    """
    # 在命令行参数上加上--setuo-show进行详细打印
    pytest.main(['-vs', ])
