#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/21
# @Author  : wanghui
from time import sleep

from selenium import webdriver

from business.pms import BasePage
from business.pms.HomePage import Home
from business.pms.Resource import R


class ProductMapper(BasePage.Base):
    """homepage 对象"""

    def search_all(self):
        """
        查询全部
        :return:
        """
        self.click(R.product_mapper.search)
        sleep(3)

    def search_by_product_name(self,product_name):
        """
        根据产品名称查询
        :return:
        """
        self.send_keys(R.product_mapper.product_name,product_name)
        self.click(R.product_mapper.search)
        sleep(3)

    def search_by_product_code(self,product_code):
        """
        根据产品编码查询
        :param product_code:
        :return:
        """
        self.send_keys(R.product_mapper.product_code,product_code)
        self.click(R.product_mapper.search)
        sleep(3)

    def search_by_customer_product_code(self,customer_product_code):
        """
        根据客户产品编码查询
        :param customer_product_code:
        :return:
        """
        self.send_keys(R.product_mapper.customer_product_code,customer_product_code)
        self.click(R.product_mapper.search)
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
