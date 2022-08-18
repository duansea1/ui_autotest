# -- coding: utf-8 --
# @time :
# @author : xxxx
# @file : .py
# @desp : xxxx

import requests


class RequestUtil:
    sess = requests.session()

    def all_send_request(self, method, url, **kwargs):
        """封装接口请求方法"""
        print("----------------------------")
        res = RequestUtil.sess.request(method, url, **kwargs)
        return res
