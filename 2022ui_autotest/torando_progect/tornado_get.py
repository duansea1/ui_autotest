# -*- coding: utf-8 -*-
# ---
# @Software: PyCharm
# @Author: duansea
# @Time: 2023年10月月18日 10:50
# ---

import tornado.ioloop
import tornado.web
import json

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        """get 请求"""
        a = self.get_argument('a')
        b = self.get_argument('b')
        c = int(a)+int(b)
        self.write("求和c="+str(c))

    def post(self):
        """post请求"""
        body = self.request.body
        body_decode = body.decode()
        body_json = json.loads(body_decode)
        a = body_json.get('a')
        b = body_json.get('b')
        c = int(a)+int(b)
        self.write("求和c=" + str(c))

application = tornado.web.Application([(r"/add", MainHandler), ])

if __name__ == "__main__":
    application.listen(8899)   # http://127.0.0.1:8899/add?a=1&b=2222
    tornado.ioloop.IOLoop.instance().start()
