# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2023年9月月27日 10:06
# ---
"""
内置装饰器：property
"""
print("**"*10 + '样例1-不能对属性值做合法性校验的情况' + "*"*20)
class Student:
    def __init__(self, name, age=None):
        self.name = name
        self.age = age

# 实例化
xiaoming = Student('xiaoming')
# 添加属性
xiaoming.age = 26
# 查询属性
xiaoming.age
# 删除属性
del xiaoming.age

print("**"*10 + '优化样例1' + "*"*20)

class Student2(object):
    def __init__(self, name):
        self.name = name
        self.nam = None

    def set_age(self, age):
        if not isinstance(age, int):
            raise ValueError('年龄必须为整数')
        if not 0 < age <100:
            raise ValueError(' age: between:1~99')
        self._age = age

    def get_age(self):
        return self._age

    def del_age(self):
        self._age = None

xiaoming2 = Student2('小了')

# 添加属性
xiaoming2.set_age(27)
# 查询属性
print(xiaoming2.get_age())
# 删除属性
xiaoming2.del_age()
print(xiaoming2.get_age())

print("**"*10 + '优化样例2--使用装饰器' + "*"*20)

class Student3(object):
    _age = 1

    def __init__(self, name ):
        self.name = name
        self.name = None

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, value):
        if not isinstance(value, int):
            raise ValueError('请输入整数')
        if not 0 < value < 100:
            raise ValueError('value:between 1~99')
        self._age = value

    @age.deleter
    def age(self):
        del self._age

xiaoming3 = Student3('xiaoming3')
# 设置属性
xiaoming3.age = 28
# 查询属性
print(xiaoming3.age)
# 删除属性
del xiaoming3.age

print(xiaoming3.age)


class Student4:
    def __init__(self, name):
        self.name = name

    @property
    def math(self):
        self._math

    @math.setter
    def math(self,value):
        if 0 <= value <= 100:
            self._math = value
        else:
            raise ValueError('between 1-100')

class TestProperty(object):
    def __init__(self, fget=None, fset=None, fdel=None, doc=None):
        self.fget = fget
        self.fset = fset
        self.fdel = fdel
        self.__doc__ = doc

    def __get__(self, obj, objtype=None):
        print("in __get__")
        if obj is None:
            return self
        if self.fget is None:
            raise AttributeError
        return self.fget(obj)

    def __set__(self, obj, value):
        print("in __set__")
        if self.fset is None:
            raise AttributeError
        self.fset(obj, value)

    def __delete__(self, obj):
        print("in __delete__")
        if self.fdel is None:
            raise AttributeError
        self.fdel(obj)

    def getter(self, fget):
        print("in getter")
        return type(self)(fget, self.fset, self.fdel, self.__doc__)

    def setter(self, fset):
        print("in setter")
        return type(self)(self.fget, fset, self.fdel, self.__doc__)

    def deleter(self, fdel):
        print("in deleter")
        return type(self)(self.fget, self.fset, fdel, self.__doc__)

print("**"*10 + '装饰器实战' + "*"*20)

import signal
class TimeoutException(Exception):
    def __init__(self, error='Timeout waiting for response from Cloud'):
        Exception.__init__(self, error)

def timeout_limit(timeout_time):
    def wrapper(func):
        def handler(signum, frame):
            raise TimeoutException()

        def deco(*args, **kwargs):
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(timeout_time)
            func(*args, **kwargs)
            signal.alarm(0)
        return deco
    return wrapper

print(timeout_limit(12))