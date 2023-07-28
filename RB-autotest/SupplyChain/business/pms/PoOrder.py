#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/22
# @Author  : wanghui
import datetime
from time import sleep

from selenium import webdriver

from business.pms import BasePage
from business.pms.HomePage import Home
from business.pms.Resource import R


class PoOrder(BasePage.Base):
    """homepage 对象"""

    def get_search_all(self):
        """查询全部订单"""
        self.click(R.po_order.reset_button)
        sleep(4)
        self.click(R.po_order.search)
        sleep(4)

    def get_search_by_POTime(self):
        """查询当天PO订单"""
        self.click(R.po_order.reset_button)
        # begin_time = self.getDatetimeToday().strftime('%Y-%m-%d')
        # end_time = self.getDatetimeSub(1).strftime('%Y-%m-%d')
        begin_time = '2017-12-13'
        end_time = '2017-12-14'
        self.send_keys(R.po_order.po_begin_time,begin_time)
        self.send_keys(R.po_order.po_end_time,end_time)
        self.click(R.po_order.search)
        #table_item=self.find_element(R.po_order.table_items)
        #table_items_rows = table_item.find_elements_by_tag_name('tr')
        #print(len(table_items_rows))
        sleep(3)

    def get_search_by_supplierName(self,supplier_name):
        """
        根据供应商注册名称查询
        :param supplier_name:
        :return:
        """
        self.click(R.po_order.reset_button)
        self.send_keys(R.po_order.supplier_name,supplier_name)
        self.click(R.po_order.search)
        sleep(1)

    def get_search_by_supplierCode(self,supplier_code):
        """
        根据供应商编码查询
        :param supplier_code:
        :return:
        """
        self.click(R.po_order.reset_button)
        self.send_keys(R.po_order.supplier_code,supplier_code)
        self.click(R.po_order.search)
        sleep(1)

    def get_search_by_PoCode(self,po_code):
        """
        根据PO编码查询
        :param po_code:
        :return:
        """
        self.click(R.po_order.reset_button)
        self.send_keys(R.po_order.po_code,po_code)
        self.click(R.po_order.search)
        sleep(1)

if __name__ == '__main__':
    driver = webdriver.Chrome()
    driver.maximize_window()
    h = Home(driver)
    h.open_login_page(driver)
    h.login()
    h.enter_pms_platform()
    h.go_po_order()
    test = PoOrder(driver)
    test.get_search_by_POTime()
