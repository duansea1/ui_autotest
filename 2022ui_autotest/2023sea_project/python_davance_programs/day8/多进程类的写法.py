# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-11-15 18:12
# ---
from multiprocessing import Process
class MyProcess(Process):
    def __init__(self):
        super().__init__()  # 实例化继承的类Process的init方法
        pass

    def run(self):
        print('running....', self.name, self.daemon)

if __name__ == "__main__":
    p1 = MyProcess()
    p2 = MyProcess()
    p1.start()   # 会调用process中的run
    p2.start()
