#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/14
# @Author  : wanghui
import pytest
from business.pms.DepositExamine import DepositExamine
from business.pms.HomePage import Home
from business.pms.Resource import R
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
#     h.go_deposit_examine()
#     yield dr
#     dr.quit()

@pytest.mark.pms_0
def test_search_by_supplierName(selenium):
    """根据供应商名称查询"""
    mgr=ManageSystem(selenium)     #集成管理系统
    mgr.login_with_account()     #登录
#     mgr.chose_subsystem('采购管理系统(集团)','系统仓库')     #进入-采购管理系统(集团)
    mgr.choose_subsystem_from_mysystem("采购管理系统")  #从我的工作台更多中，进入采购管理系统(集团)
    h=Home(selenium)     #PMS
    h.go_deposit_examine()
    p = DepositExamine(selenium)
    #p.search_all()
    supplier_name=p.driver.find_element_by_xpath('//*[@id="maingrid4|2|r1001|c105"]/div').text
    p.search_by_supplierName(supplier_name)
    table_item = p.find_element(R.deposit_examine.table_items)
    table_items_rows = table_item.find_elements_by_tag_name('tr')
    #print(len(table_items_rows))
    assert len(table_items_rows)>0

if __name__ == '__main__':
    from public import test
    test.runtc(__file__, 'pms_0',driver='Chrome')
