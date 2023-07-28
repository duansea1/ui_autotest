#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/14
# @Author  : wanghui
import pytest
from business.pms.ContractManage import ContractManage
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
#     h.go_contract_manage()
#     yield dr
#     dr.quit()

@pytest.mark.pms_4
def test_search_by_contractCode(selenium):
    """根据合同编号查询"""
    mgr=ManageSystem(selenium)     #集成管理系统
    mgr.login_with_account()     #登录
#     mgr.chose_subsystem('采购管理系统(集团)','系统仓库')     #进入-采购管理系统(集团)
    mgr.choose_subsystem_from_mysystem("采购管理系统")  #从我的工作台更多中，进入采购管理系统(集团)
    h=Home(selenium)     #PMS
    h.go_contract_manage()
    p = ContractManage(selenium)
    p.search_all()
    contractCode=p.driver.find_element_by_xpath('//*[@id="604"]/td[3]').text
    p.search_by_contractCode(contractCode)
    table_item = p.find_element(R.contract_manage.table_items)
    table_items_rows = table_item.find_elements_by_tag_name('tr')
    print(len(table_items_rows))
    assert len(table_items_rows)>0

if __name__ == '__main__':
    args = ['test_contract_manage.py', '-m pms_4', '--driver=Chrome']
    pytest.main(args)
