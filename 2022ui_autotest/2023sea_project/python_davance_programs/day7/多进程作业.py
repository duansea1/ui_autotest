# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-11-13 19:13
# ---
"""
多进程和多线程的区别？
应用场景:
进程拥有独立的内存空间，而线程共享进程的内存空间。这意味着多进程之间的数据隔离性好，而多线程之间数据共享性强。

创建新进程需要对其父进程进行一次克隆，开销较大，而创建新线程则相对简单，开销较小。
在多进程中，同一个变量，各自有一份拷贝存在于每个进程中，互不影响，而多线程中，所有变量都由所有线程共享，存在数据一致性问题。
同一个进程的线程之间可以直接交流，而两个进程想通信，必须通过一个中间代理来实现。
一个线程可以控制和操作同一进程里的其他线程，但是进程只能操作子进程。

"""