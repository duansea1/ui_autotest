# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2022年10月月04日 8:39
# ---

class Fuction():
    # counts = "123"
    def __init__(self, weight, height, color):
        self.weight = weight
        self.height = height
        self.__color = color

    def mybox(self):
        return self.weight, self.height, self.__color


mybo = Fuction(22, 23, "red")
print(mybo.mybox())
mybo.counts ="999"
print(mybo.counts)
del mybo.counts

print(mybo.counts)