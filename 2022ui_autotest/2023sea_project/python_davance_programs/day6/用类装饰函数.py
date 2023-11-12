# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-11-09 12:18
# ---


class A(object):
    def __init__(self, func):   # 返回一个对象，__init__ 方法首先会初始化对象，把对象返回
        self.func = func
        print("打印A")

    def __call__(self, *args, **kwargs):  # 当对一个对象加（）时，此方法会自动执行
        """被装饰的函数写到这里
        self.func 是被传入的装饰函数
        """
        pass

@A   # 类，会把f传给类，然后返回一个A的实例
def f(a, b):
    """
    """

nums = [1, 2, 3]
print(hasattr(nums, "__call__"))


if __name__ == "__main__":
    print(hasattr(f, "__class__"))
    print(type(f))
    print(type(A(f)))
    f(1, 2)
