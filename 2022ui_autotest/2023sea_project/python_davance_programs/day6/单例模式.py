# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-11-11 12:45
# ---
"""
单例模式:
方法1：import
方法2：
方法3：装饰器
"""

class Person(object):
    obj = None

    def __init__(self):
        pass

    def __new__(cls, *args, **kwargs):
        if cls.obj is None:
            cls.obj = super(Person).__new__(cls)  # 分配内存
        return cls.obj
