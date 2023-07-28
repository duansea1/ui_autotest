#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/15
# @Author  : wanghui
from time import sleep

from business.pms import BasePage
from business.pms.Resource import R


class SupplierProductInPriceCheck(BasePage.Base):
    """homepage 对象"""

    def get_search_result(self):
        """
        查询全部结果
        :return:
        """
        self.click ( R.supplier_product_inPrice_check.search )
        sleep ( 20 )
