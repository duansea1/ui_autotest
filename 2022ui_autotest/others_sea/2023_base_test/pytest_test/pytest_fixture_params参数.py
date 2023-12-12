# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023年11月月14日 15:40
# ---
"""
fixture详解：https://zhuanlan.zhihu.com/p/443523226
params:表示fixture的参数化功能。

"""

import pytest
data = ['sea', 'kevin', (1, 2, 3)]
@pytest.fixture(params=data, ids=['sea-sea-sea', 'user=kevin', 'user=admin'])  # ids是执行的参数的别名
def login(request):
    print('登录操作')
    yield request.param   #
    print("login out !")


class Test_Login:
    def test_01(self, login):
        print('用例1-')
        print(f"登录的用户名{login}")    # 此处的login是执行login函数的返回值

    def test_02(self):
        print('----用例02----')


if __name__ == '__main__':
    """
    在命令行参数上加上--setuo-show进行详细打印出fixture在具体那条用例上进行生效。
    多个fixture同时使用
　　fixture不仅仅能单个使用，还能一起使用。使用的执行顺序取决于你传入的顺序决定，意思就是，先传的先执行。
    """
    # 在命令行参数上加上--setuo-show进行详细打印
    pytest.main(['-vs', ])
    
