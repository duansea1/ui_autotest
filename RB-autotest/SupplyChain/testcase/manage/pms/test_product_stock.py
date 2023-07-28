#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/15
# @Author  : wanghui
import pytest
from business.pms.HomePage import Home
from business.pms.ProductStock import ProductStock
from business.pms.Resource import R
from business.manage.manage_home import ManageSystem



@pytest.mark.pms_0
def test_search_all(selenium):
    """查询全部"""
    mgr=ManageSystem(selenium)     #集成管理系统
    mgr.login_with_account()     #登录
#     mgr.chose_subsystem('采购管理系统(集团)','系统仓库')     #进入-采购管理系统(集团)
    mgr.choose_subsystem_from_mysystem("采购管理系统")  #从我的工作台更多中，进入采购管理系统(集团)
    h=Home(selenium)     #PMS
    h.go_product_stock()
    p = ProductStock(selenium)
    p.search_all()
    table_item = p.find_element(R.product_stock.table_items)
    table_items_rows = table_item.find_elements_by_tag_name('tr')
    assert len(table_items_rows)>0

if __name__ == '__main__':
    from public import test
    test.runtc(__file__, 'pms_0',driver='Chrome')