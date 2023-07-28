#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/16
# @Author  : wanghui
from time import sleep
from business.pms import BasePage
from business.pms.Resource import R
from selenium.webdriver.support.select import Select


class Supplier(BasePage.Base):
    """homepage 对象"""

    def get_search_result(self):
        """
        查询全部结果
        :return:
        """
        self.click(R.supplier.reset_button)
        self.click ( R.supplier.search )
        sleep ( 3 )

    def get_result_by_supplierName(self,supplier_name):
        """
        根据供应商名称查询
        :return:
        """
        self.click(R.supplier.reset_button)
        self.send_keys(R.supplier.supplier_name,supplier_name)
        self.click(R.supplier.search)
        sleep(3)

    def get_result_by_supplierCode(self,supplier_code):
        """
         根据供应商编号查询
         :return：
        """
        self.click ( R.supplier.reset_button )
        self.send_keys(R.supplier.supplier_code,supplier_code)
        self.click(R.supplier.search)
        sleep(3)

    def get_result_by_supplierStatus(self,j):
        """
        根据供应商状态查询
        :return:
        """
        self.click ( R.supplier.reset_button )
        sleep(1)
        Select(self.driver.find_element_by_id("supplierStatus")).select_by_value(j)
        sleep(2)
        self.click(R.supplier.search)
        sleep(3)
