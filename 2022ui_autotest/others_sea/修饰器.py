# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2022年9月月02日 12:11
# ---
import time


class me():

    content = "默认身体结构1111"
    content2 = "默认身体结构222222"

    def eye(self):
        print('eye')
        return self.arm()

    @classmethod
    def arm(cls):
        print("arm:", cls.content)
        return time.time()

    @staticmethod
    def finter():
        print("finter:", me.content2)
        return 2222


if __name__ == "__main__":
    M = me()
    print(M.eye())
    # print(me.finter())
