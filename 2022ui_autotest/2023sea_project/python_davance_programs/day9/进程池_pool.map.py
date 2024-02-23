# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-11-19 17:10
# ---
import time
from multiprocessing import Pool

def square(x):
    print("_____________________", x * x)
    return x * x


if __name__ == '__main__':
    start = time.time()
    pool = Pool(5)  # 创建一个包含5个进程的进程池
    result = pool.map(square, [1, 2, 3, 4, 5, 6, 7])   # []中的 分别取给square --map会阻塞主程序
    print(result)
    pool.close()  # 关闭进程池，不再接受新的任务
    end = time.time()  # 记录结束的时间
    print(f"总共用了{(end - start):.3f}时间")


