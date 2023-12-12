# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2022年9月月30日 11:03
# ---
import time
class StrFangFa():
    def __int__(self, name, age, county):
        self.name = name
        self.age = age
        self.county = county

    def Fangfa(self):
        ti = time.time()
        print("----", ti)

    def __str__(self):
        # 按照什么类型进行输出信息
        print(f"your name-{self.name}\n your age--{self.age}\n your county--{self.county}")
        # print("__str__")

    def __del__(self):
        print("消除")
        print(1+2)

if __name__ == "__main__":
    StrFangFa().Fangfa()
