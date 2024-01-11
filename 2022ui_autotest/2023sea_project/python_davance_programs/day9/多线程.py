# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-11-19 18:18
# ---

import threading
import time


def music(user):
    print(f"{user}正在听音乐--")
    print(f"{threading.current_thread().name}正在运行")
    time.sleep(3)
    print(f"{threading.current_thread().name}即将结束")

def lol(user):
    time.sleep(2)

if __name__ == '__main__':
    t1 = threading.Thread(target=music, args=('sea', ), name="mysea线程1")
    t2 = threading.Thread(target=lol, args=('无极', ), name='线程2')
    t1.start()
    t2.start()
    t1.join()  # 阻塞的主程序，但不会阻塞线程2（因县城已经执行）
    t2.join()
    print('主程序结束')
