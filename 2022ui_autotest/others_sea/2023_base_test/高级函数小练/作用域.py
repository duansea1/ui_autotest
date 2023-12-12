# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2022年9月月24日 16:50
# ---

# num =111
def zyy():
    # global num
    # print(num)
    num = 123
    print("num::", num)
    # num =777
    def zyy1():
        nonlocal num
        num = 200
        print("zyy1:::", num)
    zyy1()

def outer():
    num = 10
    def inner():
        nonlocal num   # nonlocal关键字声明
        num = 100
        print(num)
    inner()
    print(num)
outer()

zyy = zyy()

print("-----------------------")

a = 10
def test(a):
    print("a",a)
    # global a
    a = a + 1
    print(a)

test(a)


###  python3标准库
import os

print("返回当前的工作目录", os.getcwd())

os.system("ipconfig")
# print(ip_res.text())
print(os.listdir(os.getcwd()))


#### 文件通配符
import glob

print(glob.glob("*.py"))

# 命令行参数
import sys
print(sys.argv)

# 正则匹配
import re
re1= re.findall(r'\bf[a-z]*', 'which f  foot or hand fell fastest')
print(re1)

re_sub = re.sub(r'(\b[a-z]+) \1', r'\1', 'cat jj in the the hat')
print(re_sub)

s = "大家好， 我是一个小小。i am A D so glad to introduce myself. 18 years old."
print(re.sub(r's[a-z]', '&', s))  # 替换s开头的字母
print(re.sub(r'[A-B]', '#', s))
print(re.sub(r'[A-B2-9]', '#', s)) # 匹配A-B 区间的大写字母，并替换为# 匹配2-9之间的数字，并替换为#号

#  数学
import math

m = math.cos(math.pi / 4)
print(m)

# 随机数random
import random
rc = random.choice(['kevin', 'kobe'])
print(rc)

print(random.randrange(2,9))

# 访问互联网
from urllib.request import urlopen
#
# for line in urlopen('https://cn.bing.com/search'):
#     line = line.decode('utf-8')
#     if 'EST'  not in line or 'EDT' in line:
#         print('访问互联网：：：：', line)
#     else:
#         print("nothing return ")

# 数据压缩zlib
# 时间日期datetaime
# 性能度量 timeit
# 测试模块

def addnum(x,y):
    s = x + y
    return s
import doctest
# doctest.testmod(addnum)

# 将列表当做队列使用
from collections import deque
queue = deque(['kovie', 'kevin', 'polu', 'kobe'])
queue.append('sea')
queue.append('haiyang')
print(queue)
queue.popleft()
print(queue)

f =1
h =2

# j =f
# f =h
# h=j
f,h = h,f


print(f,h)
## 九九
for i in range(10):
    for j in range(1,i+1):
        print("{0}*{1}={2}".format(j, i, i*j), end=' ')
    print('<----')
def get_random(num):
    a = []
    i =0
    while i< num:
        a.append(random.randint(0,100))
        i += 1
    return a

m_list = [9,1,3,45,67,23,15,0]
def bubblesort1(m_list):
    """冒泡排序"""
    for i in range(0, len(m_list)):
        flag = True
        for j in range(0, len(m_list) - 1 - i):
            if m_list[j] > m_list[j + 1]:
                m_list[j], m_list[j + 1] = m_list[j + 1], m_list[j]
                flag = False
        if flag:
            break
    print(m_list)

length = len(m_list)
def bubblesort(m_list):
    """冒泡排序"""
    for j in range(length - 1, 0, -1):
        for i in range(0, j):
            if m_list[i] > m_list[i + 1]:
                tmp = m_list[i]
                m_list[i] = m_list[i + 1]
                m_list[i + 1] = tmp
            print(m_list)


bubblesort1(m_list=m_list)

ssss = "hello,every.years:188"
import re

s_re = re.match(r'hello,(\w+).years:(\d+)', ssss)
print(s_re)
print(s_re.span())
print(s_re.groups())
print(s_re.group(2))
ss2 = "2004-959-559 # 这是一个88电话号码"

num = re.sub(r'#.*$', "", ss2)  ## 移除#及后边的中文
print(num)
# 移除非数字的内容
num = re.sub(r'\D', '', ss2)
print(num)

## findall

result1 = re.findall(r'\d+', 'rubbob 123 goole 889')
print('---', result1)
pattern = re.compile(r'\d+')
result2 = pattern.findall(ss2)
result2 = pattern.findall(ss2, 0, 3)  # 从0-3之间匹配
print(result2)

reslut3 = re.split(r'(\w+)', 'rubbob 123 goole 889')
print(reslut3)
reslut4 = re.split('\W+', ' rubbob,123,goole,889', 2)
print(reslut4)