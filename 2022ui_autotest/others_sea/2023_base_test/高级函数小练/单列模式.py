# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2022年10月月11日 19:37
# ---

class Singleton(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance

# 使用
S1 = Singleton()
S2 = Singleton()
print(id(S1), id(S2))  # 打印两个实例的id，相同说明是单例模式