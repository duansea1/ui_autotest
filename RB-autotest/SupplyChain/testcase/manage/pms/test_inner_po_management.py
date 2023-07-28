#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/15
# @Author  : wanghui
import pytest
from business.pms.HomePage import Home
from business.pms.InnerPoManagement import InnerPoManagement
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
#     h.go_inner_po_management()
#     yield dr
#     dr.quit()

@pytest.mark.pms_0
def test_search_all(selenium):
    """判断页面正常打开"""
    mgr=ManageSystem(selenium)     #集成管理系统
    mgr.login_with_account()     #登录
#     mgr.chose_subsystem('采购管理系统(集团)','系统仓库')     #进入-采购管理系统(集团)
    mgr.choose_subsystem_from_mysystem("采购管理系统")  #从我的工作台更多中，进入采购管理系统(集团)
    h=Home(selenium)     #PMS
    h.go_inner_po_management()
    p = InnerPoManagement(selenium)
    p.get_search_all()
    page_source=p.get_page_source()
    assert '确认发货'in page_source

if __name__ == '__main__':
    from public import test
    test.runtc(__file__, 'pms_0',driver='Chrome')
