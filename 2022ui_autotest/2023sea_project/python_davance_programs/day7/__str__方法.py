# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-11-12 11:04
# ---

print(hasattr(list, '__str__'))  # True

class Mylist(list):
    def __str__(self):    # print 对象时，输出的样子。返回的一定是字符串
        return "list:" + str(self[0])

nums = Mylist([1,2,3])
print(nums)