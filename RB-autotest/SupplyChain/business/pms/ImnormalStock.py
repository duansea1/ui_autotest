#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/24
# @Author  : wanghui
from time import sleep
from business.pms import BasePage
from business.pms.Resource import R

class ImnormalStock(BasePage.Base):
    """homepage 对象"""

    def search_result(self):
        """
        查询全部结果
        :return:
        """
        self.click(R.imnormal_stock.reset_button)
        self.click ( R.imnormal_stock.search )
        sleep ( 3 )

    def search_by_demand_code(self,demand_code):
        """
        根据需求编号查询
        :param demand_code:
        :return:
        """
        self.click ( R.imnormal_stock.reset_button )
        self.send_keys(R.imnormal_stock.demand_code,demand_code)
        self.click(R.imnormal_stock.search)
        sleep(3)

    def search_by_applicants(self,applicants):
        """
        根据申请人查询
        :param applicants:
        :return:
        """
        self.click ( R.imnormal_stock.reset_button )
        self.send_keys(R.imnormal_stock.applicants,applicants)
        self.click(R.imnormal_stock.search)
        sleep(3)

    def search_by_supplier_name(self,supplier_name):
        """
        根据供应商名称查询
        :param supplier_name:
        :return:
        """
        self.click ( R.imnormal_stock.reset_button )
        self.send_keys ( R.imnormal_stock.supplier_name, supplier_name )
        self.click ( R.imnormal_stock.search )
        sleep ( 3 )

    def search_by_supplier_code(self,supplier_code):
        """
        根据供应商编码查询
        :param supplier_code:
        :return:
        """
        self.click ( R.imnormal_stock.reset_button )
        self.send_keys ( R.imnormal_stock.supplier_code, supplier_code )
        self.click ( R.imnormal_stock.search )
        sleep ( 3 )