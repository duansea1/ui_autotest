# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2024-05-28 17:03
# ---
import threading
class ThreadSafeSingleton:
    __instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        with cls._lock:
            if not cls.__instance:
                cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance
s1 = ThreadSafeSingleton()
s2 = ThreadSafeSingleton()

print(s1 is s2)  # 输出 True，且在多线程环境下也安全