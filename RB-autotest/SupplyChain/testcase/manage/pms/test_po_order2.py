#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''

'''
import pytest
from business.pms.HomePage import Home
from business.pms.PoOrder import PoOrder
from business.pms.Resource import R
from business.manage.manage_home import ManageSystem



@pytest.mark.pms_2
def test_search_by_poTime(selenium):
    """根据PO生成时间查询，查询当天PO订单"""
    mgr=ManageSystem(selenium)     #集成管理系统
    mgr.login_with_account()     #登录
#     mgr.chose_subsystem('采购管理系统(集团)','系统仓库')     #进入-采购管理系统(集团)
    mgr.choose_subsystem_from_mysystem("采购管理系统")  #从我的工作台更多中，进入采购管理系统(集团)
    h = Home(selenium)
    h.go_po_order()
    p = PoOrder(selenium)
    p.get_search_by_POTime()
    table_item = p.find_element(R.po_order.table_items)
    table_items_rows = table_item.find_elements_by_tag_name('tr')
    assert len(table_items_rows)>0

@pytest.mark.pms_1
def test_search_by_supplierName(selenium):
    """根据供应商名称查询"""
    mgr=ManageSystem(selenium)     #集成管理系统
    mgr.login_with_account()     #登录
#     mgr.chose_subsystem('采购管理系统(集团)','系统仓库')     #进入-采购管理系统(集团)
    mgr.choose_subsystem_from_mysystem("采购管理系统")  #从我的工作台更多中，进入采购管理系统(集团)
    h = Home(selenium)
    h.go_po_order()
    p = PoOrder(selenium)
    p.get_search_all()
    supplier_name = p.driver.find_element_by_css_selector('.l-grid-body-table>tbody>tr>td[columnname="supplierName"]>div').text #供应商名称
    p.get_search_by_supplierName(supplier_name)
    table_item = p.find_element(R.po_order.table_items)
    table_items_rows = table_item.find_elements_by_tag_name('tr')
    assert  len(table_items_rows)>0

@pytest.mark.pms_1
def test_search_by_supplierCode(selenium):
    """根据PO编号查询"""
    mgr=ManageSystem(selenium)     #集成管理系统
    mgr.login_with_account()     #登录
#     mgr.chose_subsystem('采购管理系统(集团)','系统仓库')     #进入-采购管理系统(集团)
    mgr.choose_subsystem_from_mysystem("采购管理系统")  #从我的工作台更多中，进入采购管理系统(集团)
    h = Home(selenium)
    h.go_po_order()
    p = PoOrder(selenium)
    p.get_search_all()
    po_code = p.driver.find_element_by_css_selector('.l-grid-body-table>tbody>tr>td[columnname="poCode"]>div>a').text #PO编号
    p.get_search_by_PoCode(po_code)
    table_item = p.find_element(R.po_order.table_items)
    table_items_rows = table_item.find_elements_by_tag_name('tr')
    assert  len(table_items_rows)>0

if __name__ == '__main__':
    from public import test
    test.runtc(__file__, 'pms_0',driver='Chrome')
