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

if __name__ == "__main__":
    a = A()
