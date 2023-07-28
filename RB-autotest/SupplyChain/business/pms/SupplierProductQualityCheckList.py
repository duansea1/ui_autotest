#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/24
# @Author  : wanghui
from time import sleep
from business.pms import BasePage
from business.pms.Resource import R

class SupplierProductQualityCheckList(BasePage.Base):
    """homepage 对象"""

    def search_all(self):
        """
        查询全部结果
        :return:
        """
        #self.click(R.supplier_product_quality_check_list.reset_button)
        self.click(R.supplier_product_quality_check_list.search)
        sleep (3)

    def search_by_product_codes(self,product_codes):
        """
        根据产品编码查询
        :param product_codes:
        :return:
        """
        #self.click(R.supplier_product_quality_check_list.reset_button)
        self.send_keys(R.supplier_product_quality_check_list.product_codes,product_codes)
        self.click ( R.supplier_product_quality_check_list.search )
        sleep ( 3 )

    def search_by_product_name(self,product_name):
        """
        根据产品名称查询
        :param product_name:
        :return:
        """
        #self.click(R.supplier_product_quality_check_list.reset_button)
        self.send_keys(R.supplier_product_quality_check_list.product_name,product_name)
        self.click(R.supplier_product_quality_check_list.search)
        sleep(3)
