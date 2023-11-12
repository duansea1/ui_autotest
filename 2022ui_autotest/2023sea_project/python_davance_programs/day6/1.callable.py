# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-11-09 20:01
# ---
def add(x, y):
    return x + y

class Myclass(object):
    pass

class Myclass2(object):
    def __call__(self, *args, **kwargs):
        pass

print(callable(add))
print(callable(Myclass()))  # 加（）代表对象有没有callable
print(callable(Myclass2()))