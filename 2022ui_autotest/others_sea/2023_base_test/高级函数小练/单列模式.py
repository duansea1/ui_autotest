# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2022年10月月11日 19:37
# ---

class Signale(object):

    def __new__(cls, *args, **kwargs):
        flag = False

        if flag == False:
            flag = True
            return super().__new__(cls)
    pass


s = Signale()
print(s)
s1 = Signale()
print(s1)

