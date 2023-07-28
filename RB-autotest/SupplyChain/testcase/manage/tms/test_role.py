#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/23
# @Author  : zhangqinqin

from business.tms.HomePage import Home
import pytest
from business.tms.RolePage import Role


@pytest.mark.tms_0
def test_search_by_roleName(selenium):
    """角色管理根据角色名称查询"""
    h = Home(selenium)
    h.open_login_page(selenium)
    h.login()
    h.go_role_page()
    r = Role(selenium)
    r.get_result_by_roleName("TMS管理员角色")
    page_source = r.get_page_source()
    assert 'TMS超级管理员角色' in page_source

@pytest.mark.tms_0
def test_search_by_description(selenium):
    """角色管理根据描述查询"""
    h = Home(selenium)
    h.open_login_page(selenium)
    h.login()
    h.go_role_page()
    r = Role(selenium)
    r.get_result_by_description('TMS超级管理员角色')
    page_source = r.get_page_source()
    assert 'TMS管理员角色' in page_source


@pytest.mark.tms_0
def test_reset(selenium):
    h = Home(selenium)
    h.open_login_page(selenium)
    h.login()
    h.go_role_page()
    r = Role(selenium)
    r.reset('TMS管理员角色','TMS超级管理员角色')
    msg = r.get_reset_value()
    assert msg is None

@pytest.mark.tms_0
def test_add_cancel(selenium):
    h = Home(selenium)
    h.open_login_page(selenium)
    h.login()
    h.go_role_page()
    r = Role(selenium)
    msg = r.add_menu_cancel()
    assert msg is None




if __name__ == '__main__':
    from public import test
    test.runtc(__file__, 'tms_0',driver='Chrome')