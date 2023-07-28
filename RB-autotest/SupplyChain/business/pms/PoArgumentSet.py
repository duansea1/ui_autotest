#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/22
# @Author  : wanghui
from time import sleep

from selenium import webdriver

from business.pms import BasePage
from business.pms.HomePage import Home
from business.pms.Resource import R


class PoArgumentSet(BasePage.Base):
    """homepage 对象"""

    def search_all(self):
        """
        查询全部
        :return:
        """
        self.click(R.po_argument_set.search)
        sleep(10)


    def get_search_by_product_code(self,product_code):
        """
        根据产品编码查询
        :return:
        """
        self.click(R.po_argument_set.search)
        self.send_keys(R.po_argument_set.product_code,product_code)
        self.click(R.po_argument_set.search)
        sleep(3)

    def get_search_by_warehourse(self,j):
        """
        根据仓库查询
        :param j:
        :return:
        """
        #self.click(R.po_argument_set.search)
        self.driver.find_element_by_xpath('//*[@id="warehouseId"]/option['+str(j)+']').click()
        self.click(R.po_argument_set.search)
        sleep(3)

    def edit_argument(self,product_code,warehourse_day,safe_stock):
        """
        编辑采购优化参数，
        :param warehourse_day: 目标仓库天数T
        :param safe_stock: 安全库存波动参数K
        :return:
        """
        self.get_search_by_product_code(product_code)
        self.click(R.po_argument_set.edit_button)
        #self.driver.find_element_by_xpath()
        #R.po_argument_set.warehourse_day.clear()
        sleep(10)
        self.driver.find_element_by_id('autopoT').clear()
        self.send_keys(R.po_argument_set.warehourse_day,warehourse_day)
        self.driver.find_element_by_id('autopoK').clear()
        self.send_keys(R.po_argument_set.safe_stock,safe_stock)
        self.click(R.po_argument_set.submit_button)
        sleep(5)


if __name__ == '__main__':
    drive = webdriver.Chrome()
    drive.maximize_window()
    h= Home(drive)
    h.open_login_page(drive)
    h.login()
    h.enter_pms_platform()
    h.go_po_argument_set()
    t=PoArgumentSet(drive)
    product_code = t.driver.find_element_by_xpath ( '//*[@id="autopopmp"]/tbody/tr[1]/td[2]' ).text
    t.edit_argument(product_code,2,1)