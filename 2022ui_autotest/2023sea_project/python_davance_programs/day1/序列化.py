# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2023年10月月23日 19:06
# ---
import pickle

l = [1,2,4]
# 写入数据
pickle.dump(l, open('xuliehua.txt', 'wb'))

# 读取序列化的数据
data = pickle.load(open("xuliehua.txt", "rb"))
print(data)


# 练习练习
with open("xuliehua.txt", "rb") as f:
    data2 = f.readline()
    print(data2)
    # print(pickle.load(open("序列化.py", 'rb')))
