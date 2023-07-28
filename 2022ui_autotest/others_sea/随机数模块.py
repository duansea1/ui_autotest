# -*- coding: utf-8 -*-
# ---
# 掌握 随机数模块（random 随机数）
# @Author: duansea
# @Time: 2022年12月月25日 16:47
# ---
import random

print(random.random())
# 生成指定范围内的整数【】
print(random.randint(8, 12))

#随机选取一个元素
names = ['leiyu', 'xiaohu']
print(random.choice(names))

#随机打乱
li = list(range(10))
random.shuffle(li)
print(li)

code = ""
for i in range(4):  #循环4次取值
    li = list(range(10))
    random.shuffle(li)
    code += str(li[0])
print(code)

#
# #播下随机种子
# random.seed(10)


def randomess(): #未设置随机数种子
    num = random.randint(1, 100)
    print("未设置随机数种子:{0}".format(num))


def randomseed(seed=1): #设置随机数种子
    random.seed(seed)
    num = random.randint(1, 100)
    print('设置了随机数种子：{0}'.format(num))


def strpinjie(l=[]):
    '''列表-拼接字符串'''
    newstr = "".join(l)
    return newstr

randomess()
randomseed()

re= strpinjie(l=[ '12', 'dhk', '中国'])
print(re)
