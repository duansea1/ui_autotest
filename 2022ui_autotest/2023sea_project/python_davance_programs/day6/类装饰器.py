# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-11-09 12:15
# ---


def some_func(cls):
    return cls


@some_func
class A(object):
    """

    """
    pass


class Counter:
    def __init__(self, func):
        self.func = func
        self.count = 0

    def __call__(self, *args, **kwargs):
        self.count += 1
        return self.func(*args, **kwargs)


def counter(func):
    return Counter(func)


@counter
class TestClass:
    def test_method(self):
        print("This is a test method.")


if __name__ == "__main__":
    # a = A()

    # 创建一个 TestClass 的实例并调用其方法
    tc = TestClass()
    tc.test_method()  # 输出 "This is a test method."，并且计数器加一
    print(tc.test_method)  # 输出 1，因为我们调用了 test_method 方法一次