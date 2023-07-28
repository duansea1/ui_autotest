#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/18
# @Author  : wanghui
import datetime
from time import sleep

from selenium import webdriver

from business.pms import BasePage
from business.pms.HomePage import Home
from business.pms.Resource import R


class InnerPoManagement(BasePage.Base):
    """homepage 对象"""

    def get_search_all(self):
        """
        查询全部
        :return:
        """
        self.click(R.inner_po_management.search)
        sleep(3)

    def get_search_by_poCodes(self,po_codes):
        """
        根据单据号查询
        :return:
        """
        self.send_keys(R.inner_po_management.po_codes,po_codes)
        self.click(R.inner_po_management.search)
        sleep(3)