#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/22
# @Author  : wanghui
from time import sleep

from selenium import webdriver

from business.pms import BasePage
from business.pms.HomePage import Home
from business.pms.Resource import R


class KingbosInnerTranOrderManagement(BasePage.Base):
    """homepage 对象"""

    def search_all(self):
        """
        查询全部
        :return:
        """
        self.click(R.kingbos_inner_tran_order_management.search)
        sleep(3)

    def search_by_tran_order_codes(self,tran_order_codes):
        """
        根据单据号查询
        :param tran_order_codes:
        :return:
        """
        self.send_keys(R.kingbos_inner_tran_order_management.tran_order_codes,tran_order_codes)
        self.click(R.kingbos_inner_tran_order_management.search)
        sleep(3)