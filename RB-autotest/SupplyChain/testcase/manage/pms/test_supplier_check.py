#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/12
# @Author  : wanghui
import pytest
from business.pms.HomePage import Home
from business.pms.SupplierCheck import SupplierCheck
from business.manage.manage_home import ManageSystem


@pytest.mark.pms_0
def test_search_by_supplierName(selenium):
    """根据供应商名称查询"""
    mgr=ManageSystem(selenium)     #集成管理系统
    mgr.login_with_account()     #登录
#     mgr.chose_subsystem('采购管理系统(集团)','系统仓库')     #进入-采购管理系统(集团)
    mgr.choose_subsystem_from_mysystem("采购管理系统")  #从我的工作台更多中，进入采购管理系统(集团)
    h = Home(selenium)
    h.go_supplier_check()
    s = SupplierCheck(selenium)
    s.get_search_result()
    supplier_name = s.driver.find_element_by_css_selector('.l-grid-body-table>tbody>tr>td[columnname="supplierCompanyName"]>div').text    #供应商名称
    s.get_search_by_supplierName(supplier_name)
    page_source = s.get_page_source()
    assert  '保证金录入'in page_source


@pytest.mark.pms_1
def test_search_by_supplierCode(selenium):
    """根据供应商编码查询"""
    mgr=ManageSystem(selenium)     #集成管理系统
    mgr.login_with_account()     #登录
    mgr.chose_subsystem('采购管理系统(集团)','系统仓库')     #进入-采购管理系统(集团)
    h = Home(selenium)
    h.go_supplier_check()
    s = SupplierCheck(selenium)
    s.get_search_result()
    supplier_code = s.driver.find_element_by_css_selector('.l-grid-body-table>tbody>tr>td[columnname="supplierCode"]>div').text    #供应商编码
    s.get_search_by_supplierCode(supplier_code)
    page_source = s.get_page_source()
    assert '保证金录入'in page_source

@pytest.mark.pms_1
def test_search_by_supplierStatus(selenium):
    """根据供应商状态查询--查询审核通过数据"""
    mgr=ManageSystem(selenium)     #集成管理系统
    mgr.login_with_account()     #登录
    mgr.chose_subsystem('采购管理系统(集团)','系统仓库')     #进入-采购管理系统(集团)
    h = Home(selenium)
    h.go_supplier_check()
    s = SupplierCheck(selenium)
    s.get_search_result ()
    s.get_search_by_supplierStatus('3')
    page_source = s.get_page_source()
    assert  '保证金录入'in page_source


if __name__ == '__main__':
    from public import test
    test.runtc(__file__, 'pms_0',driver='Chrome')
