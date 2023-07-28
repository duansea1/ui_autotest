#-*- coding: utf-8 -*-
'''
Created on 2019年1月14日

@author: geqiuli
'''

from time import sleep
from selenium.webdriver.support.select import Select
from business.BasePage import Base
from business.warehouse_sys import Resource as R


class WMSLogin(Base):
    
    def login(self, warehouse_id):
        """登陆仓库管理系统"""
        print('打开仓储管理系统')
        self.driver.get('http://10.6.80.248:8080/login.xhtml')
        self.wait_until_display(R.Login.login_button)
        sleep(2)
        print('输入用户名' + R.username)
        self.send_keys(R.Login.username, R.username)
        print('输入密码' + R.password)
        self.send_keys(R.Login.password, R.password)
        sleep(2)
        print('选择仓库id=' + str(warehouse_id))
        # sel = self.driver.find_element_by_id('loginForm:warehouse')
        # Select(sel).select_by_value(warehouse_value)
        selector = Select(self.find_element(R.Login.warehouse))
        selector.select_by_value(str(warehouse_id))
        sleep(2)
        print('已选择的仓库' + selector.first_selected_option.text)
        print('点击登录按钮，进入仓储管理系统')
        self.find_element(R.Login.login_button).click()
        sleep(2)
        login_info=self.find_element(R.Login.login_info)
        print(login_info.text.strip())