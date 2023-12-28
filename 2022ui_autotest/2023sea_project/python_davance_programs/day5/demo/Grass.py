# -*- coding: utf-8 -*-
# ---
# @Author: duansea
# @Time: 2023-11-08 12:27
# ---
"""

"""
class Grass(object):
    url_map = {}

    def router(self, url):
        def decorator(func):
            # 将路径和对应的方法存储到url_map中
            self.add_url_to_map(url, func)
            # print(f.__name__)
            print('func方法名称:', func.__name__, self.url_map)  # 打印func的方法名称及
            return func
        return decorator

    def add_url_to_map(self, url, func):
        """
        将路径和方法存入到字典中=====>{“/home:func”}
        :param url:路径
        :param func: 方法
        :return:
        """
        self.url_map[url] = func
        return self.url_map
