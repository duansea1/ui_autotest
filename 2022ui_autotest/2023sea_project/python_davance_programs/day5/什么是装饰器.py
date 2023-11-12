# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-11-06 23:50
# --
"""
装饰器的作用：
需求：实现类似flask的框架，Grass 小草
解决路由问题 ：
"http://localhost/hello": "hello"函数
"http://localhost/home": "home"函数

解决方案：
1、怎么才能让使用者更方便？
"""
def hello():
    print("hello")
def home():
    print("home")
url_map = {
    "http://localhost/hello": hello,
    "http://localhost/home": home
}

while True:
    url = input("请输入url：")
    if url == "exit":
        break
    try:
        url_map[url]()  # url_map[url] 返回的是func_name
    except KeyError as e:
        print(404)


