# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2023年10月月23日 19:06
# ---
import pickle

l = [1,2,4]
pickle.dump(l, open('xuliehua.txt', 'wb'))

data = pickle.load(open("xuliehua.txt", "rb"))
print(data)