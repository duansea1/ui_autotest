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


class PoSet(BasePage.Base):
    """homepage 对象"""

    def get_search_by_productCode(self,productCode):
        """
        根据产品编码查询
        :param productCode:
        :return:
        """
        #self.click(R.po_set.search)
        self.send_keys(R.po_set.product_code,productCode)
        self.click(R.po_set.search)
        sleep(3)

