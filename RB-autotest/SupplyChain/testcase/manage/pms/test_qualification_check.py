#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/23
# @Author  : wanghui
import pytest

from business.pms.QualificationCheck import QualificationCheck
from business.pms.HomePage import Home
from business.pms.Resource import R
from business.manage.manage_home import ManageSystem


@pytest.mark.pms_0
def test_search_by_supplierName(selenium):
    """根据供应商名称查询"""
    mgr=ManageSystem(selenium)     #集成管理系统
    mgr.login_with_account()     #登录
#     mgr.chose_subsystem('采购管理系统(集团)','系统仓库')     #进入-采购管理系统(集团)
    mgr.choose_subsystem_from_mysystem("采购管理系统")  #从我的工作台更多中，进入采购管理系统(集团)
    h = Home(selenium)
    h.go_qualification_check()  #供应商资质管理
    s = QualificationCheck(selenium)
    s.search_all ()
    supplier_name = s.driver.find_element_by_xpath ('//*[@id="supplierQualificationsList"]/tbody/tr[1]/td[4]' ).text  # 获取列表第一行供应商名称
    s.search_by_supplier_name(supplier_name)
    table = s.find_element ( R.qualification_check.table_items )
    table_size = table.find_elements_by_tag_name ( 'tr' )
    assert len ( table_size ) > 1

@pytest.mark.pms_1
def test_search_by_supplierCode(selenium):
    """根据供应商编号查询"""
    mgr=ManageSystem(selenium)     #集成管理系统
    mgr.login_with_account()     #登录
#     mgr.chose_subsystem('采购管理系统(集团)','系统仓库')     #进入-采购管理系统(集团)
    mgr.choose_subsystem_from_mysystem("采购管理系统")  #从我的工作台更多中，进入采购管理系统(集团)
    h = Home(selenium)
    h.go_qualification_check()  #供应商资质管理
    s = QualificationCheck(selenium)
    s.search_all ()
    supplier_code = s.driver.find_element_by_xpath ('//*[@id="supplierQualificationsList"]/tbody/tr[1]/td[2]' ).text  # 获取列表第一行供应商编号
    s.search_by_supplier_code(supplier_code)
    table = s.find_element ( R.qualification_check.table_items )
    table_size = table.find_elements_by_tag_name ( 'tr' )
    assert len ( table_size ) > 1

if __name__ == '__main__':
    from public import test
    test.runtc(__file__, 'pms_0',driver='Chrome')
