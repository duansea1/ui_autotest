#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/9
# @Author  : zhangqinqin

from business.tms.HomePage import Home
import pytest
from business.tms.MenuPage import Menu


@pytest.mark.tms_0
def test_search_by_parentMenu(selenium):
    """菜单管理根据父订单查询"""
    h = Home(selenium)
    h.open_login_page(selenium)
    h.login()
    h.go_menu_page()
    m = Menu(selenium)
    m.get_result_by_parentMenu(2)
    page_source = m.get_page_source()
    assert '配送地址管理' in page_source
    assert '配送商KPI管理' in page_source
    assert 'KPI时效汇总报表' in page_source

@pytest.mark.tms_0
def test_search_by_url(selenium):
    """菜单管理根据url查询"""
    h = Home(selenium)
    h.open_login_page(selenium)
    h.login()
    h.go_menu_page()
    m = Menu(selenium)
    m.get_result_by_url("/master/carrierDeliverRegion/list")
    page_source = m.get_page_source()
    assert '配送地址管理' in page_source

@pytest.mark.tms_0
def test_search_by_menuName(selenium):
    """菜单管理根据菜单名称查询"""
    h = Home(selenium)
    h.open_login_page(selenium)
    h.login()
    h.go_menu_page()
    m = Menu(selenium)
    m.get_result_by_menuName("配送地址管理")
    page_source = m.get_page_source()
    assert 'carrierDeliverRegion' in page_source

@pytest.mark.tms_0
def test_search_by_type(selenium):
    """菜单管理根据类型查询"""
    h = Home(selenium)
    h.open_login_page(selenium)
    h.login()
    h.go_menu_page()
    m = Menu(selenium)
    m.get_result_by_type(3)
    page_source = m.get_page_source()
    assert '用户管理-角色赋权' in page_source

@pytest.mark.tms_0
def test_reset(selenium):
    h = Home(selenium)
    h.open_login_page(selenium)
    h.login()
    h.go_menu_page()
    m = Menu(selenium)
    m.reset('/master/carrierDeliverRegion/list','配送地址管理')
    msg = m.get_reset_value()
    assert msg is None

@pytest.mark.tms_0
def test_add_cancel(selenium):
    h = Home(selenium)
    h.open_login_page(selenium)
    h.login()
    h.go_menu_page()
    m = Menu(selenium)
    msg = m.add_menu_cancel()
    assert msg is None




if __name__ == '__main__':
    from public import test
    test.runtc(__file__, 'tms_0',driver='Chrome')