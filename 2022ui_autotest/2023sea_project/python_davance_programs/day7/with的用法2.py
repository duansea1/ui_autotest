# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2024-01-09 16:31
# ---

# 1、文件操作
with open('filename') as file:
    contents = file.read()
    print(contents)

# 2、网络连接
import socket
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect(('example.com', 80))
    s.sendall(b'hello!! server!') # 这行代码发送一个字符串到服务器。字符串被编码为字节（使用b前缀），并发送到服务器。
    data = s.recv(1024)
    print(data.decode())

#  3、线程锁

import threading
lock = threading.Lock()
with lock:
    print('打开lock，关闭lock')

# 4、进程锁
import multiprocessing
proc = multiprocessing.Lock()
with proc:
    # 执行进程安全的操作
    pass


# 5、数据库连接
# import sqlite3
#
# with sqlite3.connect('database.db') as conn:
#     cursor = conn.cursor()
#     cursor.execute('select * from users')
#     rows = cursor.fetchall()
#     for row in rows:
#         print(row)


# 6、网络请求会话
# import requests
#
# with requests.Session() as session:
#     response = session.get(r'http://www.baidu.com')
#     print(response.content)

# 7、图像界面资源
# import tkinter as tk
#
# rt = tk.Tk()
# with rt:  # TODO 报错了，rt没有 __enter__ 对象
#     # 执行图像界面操作
#     rt.title('sea-title')

# 8、串口通信---fail example
# import serial
#
# with serial.Serial('/dev/ttyUSB0',9600) as ser:
#     ser.write(b'hello,sea. today is 2024-1-10')
#     res = ser.readline()
#     print(res)

# 9、临时目录
# import tempfile
# with tempfile.TemporaryDirectory() as tem_dir:
#     # 在临时目录中执行操作
#     pass

# 10、图像处理
# from PIL import Image
# with Image.open('scenery.jpg') as img:
#     img.show(title='scenery-1')  # 图像的展示

