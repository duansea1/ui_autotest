# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-11-08 12:28
# ---
from Grass import Grass

app = Grass()

@app.router('/home')
def home():
    return "home"

@app.router('/index')
def index():
    return "index"

@app.router('/ucenter')
def index():
    return "ucenter"

def run():
    url = input("请输入url：")
    try:
        print(app.url_map[url]())
    except Exception as e:
        print(e)
if __name__ == "__main__":
    run()