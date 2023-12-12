# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-11-13 18:35
# ---

"""
单任务：单任务的应用程序（cmd.exe）
多任务：多任务的应用 window操作系统，迅雷
多任务的实现方式：多进程、多线程、协程
串行运行：在linux中串行执行多条命令用&，
并行运行：在linux中执行多条命令用&&：
并发：同时下载（单核CPU）
并行：多台分别按照一个mysql8.0，然后组成mysql集群（同时运行）


进程：静态的（软件、程序、代码、函数） 动态的进程是动态的
    程序是怎么运行的？操作系统创建一个进程（加载代码到代码内存，为变量分配内存，建档process is PID）

"""
from multiprocessing import Process, Queue
import requests
"""
需求：使用多线程实现并发下载图片
--多进程会独享内存
- 如何共享资源？队列Queue ,内存数据库redis
"""
def init_task():
    tasks = Queue()  # 队列
    tasks.put('http://pic1.win4000.com/wallpaper/5/58cf4009ba10a.jpg')
    tasks.put('https://lmg.jj20.com/up/allimg/811/112014113244/141120113244-5-1200.jpg')
def download(q: Queue):
    while True:
        url = q.get()
        r = requests.get(url, verify=False)
        img_name = url.split('/')[-1]
        with open(img_name, 'wb') as f:
            f.write(r.content)      # 把图片信息保存到文件中
        if q.empty():
            break

if __name__ == "__main__":
    tasks = Queue()  # 不能共享list、Queue和list不同点
    tasks.put('http://pic1.win4000.com/wallpaper/5/58cf4009ba10a.jpg')
    tasks.put('https://lmg.jj20.com/up/allimg/811/112014113244/141120113244-5-1200.jpg')
    p1 = Process(target=download, args=(tasks,))  # 创建一个用来执行downlod函数的进程1
    p2 = Process(target=download, args=(tasks,))  # 创建一个用来执行downlod函数的进程2
    p1.start()  # 启动进程1
    # p2.start()
