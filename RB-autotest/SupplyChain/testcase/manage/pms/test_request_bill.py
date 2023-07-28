#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/21
# @Author  : wanghui
import pytest
from business.pms.HomePage import Home
from business.pms.RequestBill import RequestBill
from business.pms.Resource import R
from business.manage.manage_home import ManageSystem


@pytest.mark.pms_0
def test_search_all(selenium):
    """菜单：请货单，查询全部"""
    mgr=ManageSystem(selenium)     #集成管理系统
    mgr.login_with_account()     #登录
#     mgr.chose_subsystem('采购管理系统(集团)','系统仓库')     #进入-采购管理系统(集团)
    mgr.choose_subsystem_from_mysystem("采购管理系统")  #从我的工作台更多中，进入采购管理系统(集团)
    h=Home(selenium)     #PMS
    h.go_request_bill()
    s = RequestBill(selenium)
    s.search_all()
    table_item = s.find_element ( R.request_bill.table_items )
    table_items_rows = table_item.find_elements_by_tag_name ( 'tr' )
    assert len ( table_items_rows ) > 0

@pytest.mark.pms_1
def test_search_by_store_code(selenium):
    """
    根据门店编码查询
    :param selenium:
    :return:
    """
    mgr=ManageSystem(selenium)     #集成管理系统
    mgr.login_with_account()     #登录
    mgr.chose_subsystem('采购管理系统(集团)','系统仓库')     #进入-采购管理系统(集团)
    h=Home(selenium)     #PMS
    h.go_request_bill()
    s = RequestBill(selenium)
    s.search_all ()
    store_code = s.driver.find_element_by_css_selector('.l-grid-body-table>tbody>tr>td[columnname="storeCode"]>div').text   #门店编码
    s.search_by_store_code(store_code)
    table_item = s.find_element(R.request_bill.table_items)
    table_items_rows = table_item.find_elements_by_tag_name('tr')
    assert  len(table_items_rows)>0

@pytest.mark.pms_1
def test_search_by_bill_no(selenium):
    """
    根据请货单编码查询
    :param selenium:
    :return:
    """
    mgr=ManageSystem(selenium)     #集成管理系统
    mgr.login_with_account()     #登录
    mgr.chose_subsystem('采购管理系统(集团)','系统仓库')     #进入-采购管理系统(集团)
    h=Home(selenium)     #PMS
    h.go_request_bill()
    s = RequestBill(selenium)
    s.search_all ()
    bill_no = s.driver.find_element_by_css_selector('.l-grid-body-table>tbody>tr>td:nth-child(3)>div>a').text      #清货单编码
    s.search_by_bill_no(bill_no)
    table_item = s.find_element(R.request_bill.table_items)
    table_items_rows = table_item.find_elements_by_tag_name('tr')
    assert  len(table_items_rows)>0

@pytest.mark.pms_1
def test_search_by_store_name(selenium):
    """
    根据门店名称查询
    :param selenium:
    :return:
    """
    mgr=ManageSystem(selenium)     #集成管理系统
    mgr.login_with_account()     #登录
    mgr.chose_subsystem('采购管理系统(集团)','系统仓库')     #进入-采购管理系统(集团)
    h=Home(selenium)     #PMS
    h.go_request_bill()
    s = RequestBill(selenium)
    s.search_all ()
    store_name = s.driver.find_element_by_css_selector('.l-grid-body-table>tbody>tr>td[columnname="storeName"]>div').text   #门店名称
    s.search_by_store_name(store_name)
    table_item = s.find_element ( R.request_bill.table_items )
    table_items_rows = table_item.find_elements_by_tag_name ( 'tr' )
    assert len ( table_items_rows ) > 0

if __name__ == '__main__':
    from public import test
    test.runtc(__file__, 'pms_0',driver='Chrome')
