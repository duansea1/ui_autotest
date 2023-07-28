'''
# -*- coding: utf-8 -*-
#开发人员:   chenpeng
#开发日期:   2019-04-25
#文件项目:   TMS
#文件名称:   承运商账户管理
 '''

import pytest
from business.tms.Carrier_management import Carrier_management
from business.tms.MenuPage import Menu
from business.tms.login import Login
from business.tms.Resource import R
from time import sleep

@pytest.mark.carrier_account_manage
def test_carrier_account_add(selenium):
    '''SQL物理删除承运商账户并新增承运商账户'''
    add=Carrier_management.carrier_account_manage(selenium)
    SQL='DELETE from tms_carrier_account where carrier_code=%s'
    code="2222222"
    type="Autotest_type"
    add.sql_del(SQL,code)
    tms=Login(selenium)
    tms.tms_login()
    m=Menu(selenium)
    m.menu('承运商管理', '配送商账号管理')
    add.add(code,type,'test_cardnumber','test_account','test_pwd','www.auto_test.com')
    sleep(1)
    add.query(type)
    result=add.find_element(R.carrier_account_manage.first_carrier).text
    assert result == code
    print('新增成功')

@pytest.mark.carrier_account_manage
def test_carrier_account_edit(selenium):
    '''编辑新增承运商账户'''
    edit=Carrier_management.carrier_account_manage(selenium)
    carrier_type="Autotest_type"
    carrier_monthcard='test_cardnumber2'
    tms=Login(selenium)
    tms.tms_login()
    m=Menu(selenium)
    m.menu('承运商管理', '配送商账号管理')
    edit.query(carrier_type)
    edit.edit(carrier_monthcard)
    sleep(1)
    edit.switch_to_iframe1()
    result=edit.find_element(R.carrier_account_manage.first_cardnumber).text
    assert result == carrier_monthcard
    print('编辑成功')

@pytest.mark.carrier_account_manage
def test_carrier_account_del(selenium):
    '''逻辑删除新增承运商账户'''
    delete=Carrier_management.carrier_account_manage(selenium)
    carrier_type="Autotest_type"
    tms=Login(selenium)
    tms.tms_login()
    m=Menu(selenium)
    m.menu('承运商管理', '配送商账号管理')
    delete.query(carrier_type)
    delete.delete()
    result=delete.find_element(R.carrier_account_manage.first_delete).text
    assert result == "已删除"
    print('逻辑删除成功')

if __name__ == '__main__':
    from public import test
    test.runtc(__file__,  tclevel='carrier_account_manage', driver='Chrome')  # Firefox，Chrome