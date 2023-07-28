#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/15
# @Author  : wanghui
import datetime
from time import sleep

from selenium import webdriver

from business.pms import BasePage
from business.pms.HomePage import Home
from business.pms.Resource import R


class PoLackManagement(BasePage.Base):
    """homepage 对象"""

    def get_search_all(self):
        """查询全部"""
        self.click(R.po_lack_management.search)
        sleep(3)

