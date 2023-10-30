# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2023年9月月27日 20:14
# ---
import time
from functools import wraps
class TimeTool:

    def snap_time(self, func):  # 如果装饰器带参数，则需要多一层方法嵌套
        @wraps(func)
        def wrapper(*args, **kwargs):
            now = time.time()
            timearray = time.localtime(now)
            otherstyleTime = time.strftime("%Y-%m-%d %H:%M:%S",timearray)
            print(func.__name__ + '==========开始执行时间为：' + str(otherstyleTime) + '==============')
            func(*args, **kwargs)
            end = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
            print(func.__name__ + '==========执行完成时间：' + str(end) + '==============')
        return wrapper

    def current_time(self):
        """获取当前执行时间"""
        current_Time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        return current_Time

    def strftime_time(self, shift_value):
        """将时间戳转为日期格式
        @:param shift_value--可以输入time.time()-时间戳
        2023-09-27 20:28:57"""
        if shift_value:
            timearray = time.localtime(shift_value)
            return time.strftime("%Y-%m-%d %H:%M:%S", timearray)


@TimeTool().snap_time
def sum(a, b):
    return a +b

# sum(1111111111111,333333)

# print(TimeTool().strftime_time(shift_value=time.time()))

# 记录方法执行次数
def counter(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        wrapper.count = wrapper.count + 1   # 累计执行次数
        print('method: %s, count: %s' % (func.func_name, wrapper.count))
        return func(*args, **kwargs)
    wrapper.count = 0
    return wrapper

# 本地缓存
def localcache(func):
    cached = {}
    miss = object()
    @wraps(func)
    def wrapper(*args):
        result = cached.get(args, miss)   # ????????
        if result is miss:
            result = func(*args)
            cached[args] = result
        return result
    return wrapper

# 路由映射
class Router(object):

    def __init__(self):
        self.url_map = {}

    def register(self, url):
        def wrapper(func):
            self.url_map[url] = func
        return wrapper

    def call(self, url):
        func = self.url_map.get(url)
        if not func:
            raise ValueError('No url function: %s', url)
        return func()

router = Router()

@router.register('/page1')
def page1():
    return 'this is page1'

@router.register('/page2')
def page2():
    return 'this is page2'

# print(router.call('/page1'))
# print(router.call('/page2'))