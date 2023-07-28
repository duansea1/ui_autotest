#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/27
# @Author  : wanghui
from time import sleep

from selenium import webdriver

from business.pms import BasePage
from business.pms.HomePage import Home
from business.pms.Resource import R


class MerchantComsManagement(BasePage.Base):
    """homepage 对象"""

    def get_search_result(self):
        """
        查询全部结果
        :return:
        """
        self.click ( R.merchant_coms_management.search )
        sleep(5)

    def get_search_by_product_code(self,product_code):
        """
        根据产品编码查询
        :return:
        """
        self.send_keys(R.merchant_coms_management.product_code,product_code)
        self.click(R.merchant_coms_management.search)
        sleep ( 5 )

    def get_search_by_apply_code(self,apply_code):
        """
        根据申请编码查询
        :param apply_code:
        :return:
        """
        self.send_keys(R.merchant_coms_management.apply_code,apply_code)
        self.click(R.merchant_coms_management.search)
        sleep ( 5 )

# if __name__ == '__main__':
#     driver = webdriver.Chrome()
#     driver.maximize_window()
#     login = Home(driver)
#     login.open_login_page(driver)
#     login.login()
#     login.enter_pms_platform ()
#     login.go_supplier_tianjin ()
#


