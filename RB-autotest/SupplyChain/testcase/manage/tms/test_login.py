#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/13
# @Author  : zhangqinqin

from business.tms.HomePage import Home
import pytest


@pytest.mark.tms_0
def test_login(selenium):
    """登录并检查登录信息"""
    h = Home(selenium)
    h.open_login_page(selenium)
    h.login()
    page_source = h.get_page_source()
    assert '尊敬的:TMS管理员，您好！' in page_source

@pytest.mark.tms_0
def test_sysmenu(selenium):
    """登录并浏览菜单管理菜单"""
    h = Home(selenium)
    h.open_login_page(selenium)
    h.login()
    h.go_menu_page()
    page_source = h.get_page_source()
    # print(page_source)
    assert '您的位置：&gt;系统管理&gt;' in page_source
    assert '菜单管理' in page_source

@pytest.mark.tms_0
def test_sysrole(selenium):
    """登录并浏览角色管理菜单"""
    h = Home(selenium)
    h.open_login_page(selenium)
    h.login()
    h.go_role_page()
    page_source = h.get_page_source()
    # print(page_source)
    assert '您的位置：&gt;系统管理&gt;' in page_source
    assert '角色管理' in page_source

@pytest.mark.tms_0
def test_sysuser(selenium):
    """登录并浏览用户管理菜单"""
    h = Home(selenium)
    h.open_login_page(selenium)
    h.login()
    h.go_user_page()
    page_source = h.get_page_source()
    # print(page_source)
    assert '您的位置：&gt;系统管理&gt;' in page_source
    assert '用户管理' in page_source

@pytest.mark.tms_0
def test_sysdata(selenium):
    """登录并浏览数据字典菜单"""
    h = Home(selenium)
    h.open_login_page(selenium)
    h.login()
    # h.go_user_page()
    h.go_data_page()
    page_source = h.get_page_source()
    # print(page_source)
    assert '您的位置：&gt;系统管理&gt;' in page_source
    assert '数据字典管理' in page_source

@pytest.mark.tms_0
def test_sysjob(selenium):
    """登录并浏览定时任务菜单"""
    h = Home(selenium)
    h.open_login_page(selenium)
    h.login()
    # h.go_user_page()
    h.go_job_page()
    page_source = h.get_page_source()
    # print(page_source)
    assert '您的位置：&gt;系统管理&gt;' in page_source
    assert '定时任务管理' in page_source


if __name__ == '__main__':
    from public import test
    test.runtc(__file__, 'tms_0',driver='Chrome')