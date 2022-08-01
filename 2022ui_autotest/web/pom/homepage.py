# -- coding: utf-8 --
# @time :
# @author : xxxx
# @file : .py
# @desp : xxxx
from selenium import webdriver

from time import sleep
from web.basecore.BasePage import Base


class HomePage(Base):

    home_url = r"http://www.baidu.com"

    def go_to_homepage(self, url=home_url):
        self.driver.get(url)
        sleep(2)
        print('进入页面：', self.driver.title)

    def go_to_userpage(self):
        "到个人中心"
        print("进到个人中心页面")



