# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2023年10月月09日 9:34
# https://blog.csdn.net/apex_eixl/article/details/130244722?spm=1001.2101.3001.6650.2&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-2-130244722-blog-78383898.235%5Ev38%5Epc_relevant_anti_t3&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-2-130244722-blog-78383898.235%5Ev38%5Epc_relevant_anti_t3&utm_relevant_index=2
# ---https://zhuanlan.zhihu.com/p/339718510#1.%20%E4%BB%80%E4%B9%88%E6%98%AFHook


class ContentStash(object):

    def __init__(self):
        self.input_filter_fn = None
        self.broker = []

    def register_input_filter_hook(self, input_filter_fn):
        """

        :param input_filter_fn: 传入函数
        :return:
        """
        self.input_filter_fn = input_filter_fn

    def insert_queue(self, content):
        """

        :param content:
        :return:
        """
        self.broker.append(content)

    def input_pipeline(self, content, use=False):
        if not use:
            return
        # input filter
        if self.input_filter_fn:
            _filter = self.input_filter_fn(content)

        # insert to   queue
        if not _filter:
            self.insert_queue(content)

# test
# #  实现一个你所需要的钩子实现：比如如果content 包含time就过滤掉，否则插入队列

def input_filter_hook(content):
    if content.get('time') is None:
        return
    else:
        return content

# 原有程序
content = {'filename': 'test.jpg', 'b64_file': "#test", 'data': {"result": "cat", "probility": 0.9}}
content_stash = ContentStash()

# 挂上钩子函数， 可以有各种不同钩子函数的实现，但是要主要函数输入输出必须保持原有程序中一致，比如这里是content
content_stash.register_input_filter_hook(input_filter_hook)

# 执行流程
content_stash.input_pipeline(content)

