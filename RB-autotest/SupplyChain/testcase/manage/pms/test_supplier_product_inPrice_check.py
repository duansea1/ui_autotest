#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/22
# @Author  : wanghui
import pytest

from business.pms.HomePage import Home
from business.pms.Resource import R
from business.pms.SupplierProductInPriceCheck import SupplierProductInPriceCheck
from business.manage.manage_home import ManageSystem
#from selenium import webdriver
# session的fixture适合多个用例，如果只有一个用例的时候，用pytest的自带fixture：selenium更合适
# @pytest.fixture('session')
# def chrome_dr():
#     dr=webdriver.Chrome()
#     h = Home(dr)
#     h.open_login_page(dr)
#     h.login()
#     h.enter_pms_platform()
#     h.go_supplier_product_inPrice_check()
#     yield dr
#     dr.quit()

@pytest.mark.pms_2
def test_search_all(selenium):
    """查询全部"""
    mgr=ManageSystem(selenium)     #集成管理系统
    mgr.login_with_account()     #登录
#     mgr.chose_subsystem('采购管理系统(集团)','系统仓库')     #进入-采购管理系统(集团)
    mgr.choose_subsystem_from_mysystem("采购管理系统")  #从我的工作台更多中，进入采购管理系统(集团)
    h=Home(selenium)     #PMS
    h.go_supplier_product_inPrice_check()
    p = SupplierProductInPriceCheck(selenium)
    p.get_search_result()
    table_item = p.find_element(R.supplier_product_inPrice_check.table_items)
    table_items_rows = table_item.find_elements_by_tag_name('tr')
    assert len(table_items_rows)>0

if __name__ == '__main__':
    from public import test
    test.runtc(__file__, 'pms_0',driver='Chrome')
