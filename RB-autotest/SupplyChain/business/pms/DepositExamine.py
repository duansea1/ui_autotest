#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/14
# @Author  : wanghui
from time import sleep

from selenium import webdriver

from business.pms import BasePage
from business.pms.HomePage import Home
from business.pms.Resource import R


class DepositExamine(BasePage.Base):
    """homepage 对象"""

    def search_all(self):
        """
        查询全部
        :return:
        """
        self.click(R.deposit_examine.search)
        sleep(3)

    def search_by_supplierName(self,supplier_name):
        """根据供应商名称查询"""
        self.send_keys(R.deposit_examine.supplier_name,supplier_name)
        self.click(R.deposit_examine.search)
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