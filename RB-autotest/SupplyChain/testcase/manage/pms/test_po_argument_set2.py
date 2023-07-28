#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/29
# @Author  : wanghui
import pytest
from business.pms.HomePage import Home
from business.pms.PoArgumentSet import PoArgumentSet
from business.pms.Resource import R
from business.manage.manage_home import ManageSystem
from selenium import webdriver


@pytest.mark.pms_3
def test_search_all(selenium):
    """查询全部"""
    mgr=ManageSystem(selenium)     #集成管理系统
    mgr.login_with_account()     #登录
#     mgr.chose_subsystem('采购管理系统(集团)','系统仓库')     #进入-采购管理系统(集团)
    mgr.choose_subsystem_from_mysystem("采购管理系统")  #从我的工作台更多中，进入采购管理系统(集团)
    h = Home(selenium)
    h.go_po_argument_set()
    p = PoArgumentSet(selenium)
    p.search_all()
    table_item = p.find_element(R.po_argument_set.table_items)
    table_item_rows =  table_item.find_elements_by_tag_name('tr')
    assert len(table_item_rows)>1

    
@pytest.mark.pms_2
def test_search_by_product_code(selenium):
    """根据产品编码查询"""
    mgr=ManageSystem(selenium)     #集成管理系统
    mgr.login_with_account()     #登录
    mgr.chose_subsystem('采购管理系统(集团)','系统仓库')     #进入-采购管理系统(集团)
    h = Home(selenium)
    h.go_po_argument_set()
    p = PoArgumentSet(selenium)
    p.search_all()
    product_code = p.driver.find_element_by_xpath('//*[@id="autopopmp"]/tbody/tr[1]/td[2]').text
    p.get_search_by_product_code(product_code)
    table_item = p.find_element(R.po_argument_set.table_items)
    table_item_rows = table_item.find_elements_by_tag_name('tr')
    assert len(table_item_rows)>1

@pytest.mark.pms_2
def test_search_by_warehourse(selenium):
    """
    根据仓库查询
    :param selenium:
    :return:
    """
    mgr=ManageSystem(selenium)     #集成管理系统
    mgr.login_with_account()     #登录
    mgr.chose_subsystem('采购管理系统(集团)','系统仓库')     #进入-采购管理系统(集团)
    h = Home(selenium)
    h.go_po_argument_set()
    p = PoArgumentSet(selenium)
    p.get_search_by_warehourse(2)
    table_item = p.find_element(R.po_argument_set.table_items)
    table_item_rows = table_item.find_elements_by_tag_name('tr')
    assert len(table_item_rows)>1


if __name__ == '__main__':
    from public import test
    test.runtc(__file__, 'pms_0',driver='Chrome')