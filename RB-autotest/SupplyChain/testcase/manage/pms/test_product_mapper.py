#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/22
# @Author  : wanghui
import pytest
from business.pms.HomePage import Home
from business.pms.ProductMapper import ProductMapper
from business.pms.Resource import R
from business.manage.manage_home import ManageSystem


@pytest.mark.pms_0
def test_search_by_product_name(selenium):
    """根据产品名称查询"""
    mgr=ManageSystem(selenium)     #集成管理系统
    mgr.login_with_account()     #登录
#     mgr.chose_subsystem('采购管理系统(集团)','系统仓库')     #进入-采购管理系统(集团)
    mgr.choose_subsystem_from_mysystem("采购管理系统")  #从我的工作台更多中，进入采购管理系统(集团)
    h=Home(selenium)     #PMS
    h.go_product_mapper()
    p = ProductMapper(selenium)
    p.search_all ()
    product_name = p.driver.find_element_by_css_selector('.l-grid-body-table>tbody>tr>td[columnname="productName"]>div').text    #产品名称
    p.search_by_product_name(product_name)
    table_item = p.find_element ( R.product_mapper.table_items )
    table_items_rows = table_item.find_elements_by_tag_name ( 'tr' )
    assert len ( table_items_rows ) > 0

@pytest.mark.pms_1
def test_search_by_product_code(selenium):
    """根据产品编码查询"""
    mgr=ManageSystem(selenium)     #集成管理系统
    mgr.login_with_account()     #登录
#     mgr.chose_subsystem('采购管理系统(集团)','系统仓库')     #进入-采购管理系统(集团)
    mgr.choose_subsystem_from_mysystem("采购管理系统")  #从我的工作台更多中，进入采购管理系统(集团)
    h=Home(selenium)     #PMS
    h.go_product_mapper()
    p = ProductMapper(selenium)
    p.search_all ()
    product_code = p.driver.find_element_by_css_selector('.l-grid-body-table>tbody>tr>td[columnname="productCode"]>div').text    #产品编码
    p.search_by_product_code(product_code)
    table_item = p.find_element ( R.product_mapper.table_items )
    table_items_rows = table_item.find_elements_by_tag_name ( 'tr' )
    assert len ( table_items_rows ) > 0

@pytest.mark.pms_1
def test_search_by_customer_product_code(selenium):
    """根据客户产品编码查询"""
    mgr=ManageSystem(selenium)     #集成管理系统
    mgr.login_with_account()     #登录
#     mgr.chose_subsystem('采购管理系统(集团)','系统仓库')     #进入-采购管理系统(集团)
    mgr.choose_subsystem_from_mysystem("采购管理系统")  #从我的工作台更多中，进入采购管理系统(集团)
    h=Home(selenium)     #PMS
    h.go_product_mapper()
    p = ProductMapper(selenium)
    p.search_all ()
    customer_product_code = p.driver.find_element_by_css_selector('.l-grid-body-table>tbody>tr>td[columnname="customerProductCode"]>div').text    #产品编码-客户
    p.search_by_customer_product_code(customer_product_code)
    table_item = p.find_element ( R.product_mapper.table_items )
    table_items_rows = table_item.find_elements_by_tag_name ( 'tr' )
    assert len ( table_items_rows ) > 0

if __name__ == '__main__':
    from public import test
    test.runtc(__file__, 'pms_0',driver='Chrome')
