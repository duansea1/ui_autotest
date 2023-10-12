# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2023年9月月26日 17:54
# ---
import time
import functools

"""
7、使用偏函数与类实现装饰器
文章地址：https://zhuanlan.zhihu.com/p/269012332
"""
print("**"*10 + '7、使用偏函数与类实现装饰器' + "*"*20)
# 如下所示，DelayFunc 是一个实现了 __call__ 的类，delay 返回一个偏函数，在这里 delay 就可以做为一个装饰器。
# （以下代码摘自 Python工匠：使用装饰器的小技巧）

class DelayFunc:
    def __init__(self, duration, func):
        self.duration = duration
        self.func = func

    def __call__(self, *args, **kwargs):
        print(f'Wait for {self.duration} seconds...')
        time.sleep(self.duration)
        return self.func(*args, **kwargs)

    def eager_call(self, *args, **kwargs):
        print("Call without delay")
        return self.func(*args, **kwargs)

def delay(duration):
    """
        装饰器：推迟某个函数的执行。
        同时提供 .eager_call 方法立即执行
        """
    # 此处为了避免定义额外函数
    # 直接使用 functool.partail 帮助构造Delayfunc实例
    return functools.partial(DelayFunc, duration)

@delay(duration=0.5)
def add(a, b):
    return a+b

print(add)  # 直接打印函数
print(add(2, 3))  # 直接调用实例，进入__call__
print(add.func)  # 实现实例方法

print("**"*10 + '8、如何写能装饰类的装饰器?' + "*"*20)
instances = {}

def singleton(cls):
    def get_instance(*args, **kwargs):
        cls_name = cls.__name__
        print('========1=======')
        if not cls_name in instances:
            print('=========2=========')
            instance = cls(*args, **kwargs)
            instances[cls_name] = instance
        return instances[cls_name]
    return get_instance

@singleton
class User:
    _instance = None  # 私有变量

    def __init__(self, name):
        print('========3=========')
        self.name = name

u1 = User('sea')
u1.age = 20
u2 = User('sea2')
print(u2)

print("**"*10 + '9、wraps装饰器有啥用?' + "*"*20)

def wrapper(func):
    def inner_fnction():
        pass
    return inner_fnction

@wrapper
def wrapped():
    pass

print(wrapped.__name__)
print(wrapper(wrapped).__name__)

from functools import wraps

""" 那如何避免不返回inner_function？方法 是使用functoolswraps装饰器，它的作用就是将被装饰的函数（wrapped）的一些属性值赋值给修饰函数wrapper
最终让属性的显示更符合我们的直觉
"""
def wrapper2(func):
    @wraps(func)    # --------wraps其实就是一个偏函数对象（partial）
    def inner_function():
        pass
    return inner_function

@wrapper2
def wrapped2():
    pass

print(wrapped2.__name__)
# wrapped2
