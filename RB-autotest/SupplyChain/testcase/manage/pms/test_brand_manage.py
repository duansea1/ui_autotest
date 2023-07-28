#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/14
# @Author  : wanghui
import pytest
from business.manage.manage_home import ManageSystem
from business.pms.BrandManage import BrandManage
from business.pms.HomePage import Home
from business.pms.Resource import R



@pytest.mark.pms_0
def test_search_by_brandName(selenium):
    """根据合同编号查询"""
    mgr=ManageSystem(selenium)     #集成管理系统
    mgr.login_with_account()     #登录
#     mgr.my_system_more()      #我的工作台，我的系统-更多
    mgr.choose_subsystem_from_mysystem("采购管理系统")  #从我的工作台更多中，进入采购管理系统(集团)
#     mgr.chose_subsystem('采购管理系统(集团)')     #进入-采购管理系统(集团)
    h=Home(selenium)     #PMS
    h.go_brand_manage()     #进入菜单：品牌方管理
    p = BrandManage(selenium)
    p.search_all()
    brandName=p.driver.find_element_by_xpath('//*[@id="3"]/td[3]').text
    p.search_by_brandName(brandName)
    table_item = p.find_element(R.brand_manage.table_items)
    table_items_rows = table_item.find_elements_by_tag_name('tr')
    print(len(table_items_rows))
    assert len(table_items_rows)>0

if __name__ == '__main__':
    from public import test
    test.runtc(__file__, 'pms_0',driver='Chrome')
