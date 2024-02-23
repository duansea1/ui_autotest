# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-11-20 19:09
# ---
import asyncio  # 异步IO库 非阻塞io
import time
# async 关键字 await 关键字

async def work1():  # 声明 任务work1 是异步的
    for i in range(2):
        print(f"work1 廷议月")
        await asyncio.sleep(1)

async def work2():  # 声明 任务work2 是异步的
    for i in range(1):
        print(f"work2 打游戏")
        await asyncio.sleep(1)

def calc_time(func):
    def wrap(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        end = time.time()
        print(f"执行时间{(end - start_time):.2f}")
        return end - start_time
    return wrap
# @calc_time
async def main():
    task1 = asyncio.create_task(work1())  # 创建一个异步任务
    task2 = asyncio.create_task(work2())
    await task1  # 把当前任务挂起，去执行别的任务
    await task2

if __name__ == '__main__':
    asyncio.run(main())

