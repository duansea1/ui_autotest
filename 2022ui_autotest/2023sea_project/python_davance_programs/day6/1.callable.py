# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-11-09 20:01
# ---
"""
_call__是一个特殊的方法，用于使一个对象可以像函数那样被调用。
当你尝试使用一个对象像函数那样调用它时（即使用圆括号），Python会查找该对象的__call__方法并执行它
"""

def add(x, y):
    return x + y

class Myclass(object):
    pass

class Myclass2(object):
    def __call__(self, *args, **kwargs):
        pass

print(callable(add))
print(callable(Myclass))  # 加（）验证对象有没有callable
print(callable(Myclass2()))


class CallableClass:
    def __call__(self, *args, **kwargs):
        print("Called with:", args, kwargs)
        if args:
            print('参数正确',[args][0][0]=='a')
        if kwargs:
            print('dayin:',kwargs['key'])
            if kwargs['key'] == 'value1':
                print('获取到可变参数', kwargs)

    def sum (self, a, b):
        return a + b


# 创建一个对象
obj = CallableClass()

# 像函数一样调用这个对象
obj('a', 2, 3, key="value1")
print(obj.sum(1,2))

print(callable(obj))