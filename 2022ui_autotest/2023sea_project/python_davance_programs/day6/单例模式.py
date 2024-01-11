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
    _obj = None

    def __init__(self):
        # print(super(Person).__new__())
        pass

    def __new__(cls, *args, **kwargs):
        print(f'kaishi分配内存{cls._obj} ')
        if not cls._obj:
            print('开始分配内存', super().__new__(cls))
            # cls._obj = True
            cls._obj = super().__new__(cls)  # 分配内存
        else:
            print('已存在实例')
        return cls._obj

    def p(self):
        print('ppppp')


class MyClass:
    instances = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls.instances:
            cls.instances[cls] = super().__new__(cls)
        return cls.instances[cls]

    # 使用示例

if __name__ == '__main__':
    # print(Person)
    a = Person()
    print(id(a))
    b = Person()
    print(id(b))


    # obj1 = MyClass()
    # print(obj1)
    # obj2 = MyClass()  # obj1 和 obj2 实际上是同一个对象
    # print(obj2)

