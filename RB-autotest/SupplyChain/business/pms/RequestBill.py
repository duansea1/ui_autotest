#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/21
# @Author  : wanghui
from time import sleep

from selenium import webdriver

from business.pms import BasePage
from business.pms.HomePage import Home
from business.pms.Resource import R


class RequestBill(BasePage.Base):
    """homepage 对象"""

    def search_all(self):
        """
        查询全部
        :return:
        """
        self.click(R.request_bill.search)
        sleep(3)

    def search_by_store_code(self,store_code):
        """
        根据门店编码查询
        :return:
        """
        self.send_keys(R.request_bill.store_code,store_code)
        self.click(R.request_bill.search)
        sleep(3)

    def search_by_bill_no(self,bill_no):
        """
        根据请货单编码查询
        :param bill_no:
        :return:
        """
        self.send_keys(R.request_bill.bill_no,bill_no)
        self.click(R.request_bill.search)
        sleep(3)

    def search_by_store_name(self,store_name):
        """
        根据门店名称查询
        :param store_name:
        :return:
        """
        self.send_keys(R.request_bill.store_name,store_name)
        self.click(R.request_bill.search)
        sleep(3)


# if __name__ == '__main__':
#     driver = webdriver.Chrome()
#     driver.maximize_window()
#     h = Home(driver)
#     h.open_login_page(driver)
#     h.login()
#     h.enter_pms_platform()
#     h.go_qualification_check_kunshan()
#     t = qualification_check_guangzhou(driver)
#     t.search_all()
