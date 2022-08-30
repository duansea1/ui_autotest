# -- coding: utf-8 --
# @time :
# @author : xxxx
# @file : .py
# @desp : 统一封装、统计用例数、日志监控、发送请求的代码很相似

import requests


class RequestUtil:
    sess = requests.session()

    def all_send_request(self, method, url, **kwargs):
        """封装接口请求方法"""
        print("----------------------------")
        res = RequestUtil.sess.request(method, url, **kwargs)
        return res
