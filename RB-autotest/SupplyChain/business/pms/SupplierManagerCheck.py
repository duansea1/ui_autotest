#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/23
# @Author  : wanghui
from time import sleep
from business.pms import BasePage
from business.pms.Resource import R
from selenium.webdriver.support.select import Select

class SupplierManageCheck(BasePage.Base):
    """homepage 对象"""

    def get_search_result(self):
        """
        查询全部结果
        :return:
        """
        self.click(R.supplier_manager_check.reset_button)
        sleep(1)
        self.click(R.supplier_manager_check.search)
        sleep(6)
        result=self.driver.find_element_by_css_selector('.l-bar-message>span')
        print(result.text)

    def get_search_by_supplierName(self,supplier_name):
        """
        根据供应商名称查询
        :param supplier_name:
        :return:
        """
        self.click ( R.supplier_manager_check.reset_button )
        self.send_keys(R.supplier_manager_check.supplier_name,supplier_name)
        self.click(R.supplier_manager_check.search)
        sleep(3)

    def get_search_by_supplierCode(self,supplier_code):
        """
        根据供应商编号查询
        :param supplier_code:
        :return:
        """
        self.click ( R.supplier_manager_check.reset_button )
        self.send_keys(R.supplier_manager_check.supplier_code,supplier_code)
        self.click(R.supplier_manager_check.search)
        sleep(3)

    def get_search_by_supplierStatus(self,j):
        """
        根据供应商状态查询
        :param j:
        :return:
        """
        self.click ( R.supplier_manager_check.reset_button )
        sleep(1)
        Select(self.driver.find_element_by_id("supplierStatus")).select_by_value(j)
        #self.click(R.supplier_manager_check.supplier_status)
        #self.driver.find_element_by_xpath('/html/body/div[4]/div[1]/table/tbody/tr['+str(j)+']/td').click()
        self.click(R.supplier_manager_check.search)
        sleep(3)