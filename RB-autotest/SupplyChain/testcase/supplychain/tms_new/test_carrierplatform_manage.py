'''
# -*- coding: utf-8 -*-
#开发人员:   chenpeng
#开发日期:   2019-04-16 17:20:55
#文件项目:   TMS
#文件名称:   承运商平台管理
 '''

import pytest
from business.tms.Carrier_management import Carrier_management
from business.tms.MenuPage import Menu
from business.tms.login import Login
from business.tms.Resource import R
from time import sleep

@pytest.mark.carrierplat_manage
def test_carrierplat_add(selenium) :
    '''新增一个承运商平台，检验是否保存成功'''
    sql_del=Carrier_management.carrier_platform_management(selenium)
    SQL='DELETE FROM tms_carrier_platform WHERE CODE =%s'
    COND='autotest2'
    sql_del.mysql_delete(SQL,COND)
    #登录TMS
    tms = Login (selenium)
    tms.tms_login ()
    m = Menu (selenium)
    m.new_menu ('承运商管理', '承运商平台管理')
    add = Carrier_management.carrier_platform_management (selenium)
    add.add ('autotest2', '自动化测试平台2', 'kyd', 'www.aututest2.com.cn', '已签收', '拒绝签收') #新增承运商平台
    add.query('autotest2')  #查询新增的承运商
    result=add.find_element(R.Carrier_platform_manage.first_code).text  #查询结果
    assert 'autotest2' ==result, print ('查询结果错误')
    print ('保存成功，查询结果为：' + result + '，正确')


@pytest.mark.carrierplat_manage
def test_carrierplat_add_repeat(selenium):
    '''新增已存在的承运商平台校验重复性'''
    tms=Login(selenium)
    tms.tms_login()
    m=Menu(selenium)
    m.new_menu('承运商管理','承运商平台管理')
    add=Carrier_management.carrier_platform_management(selenium)
    add.add('autotest2','自动化测试平台','kyd','www.aututest.com.cn','已签收','拒绝签收')
    assert '插入失败' in add.driver.page_source, print ('保存成功')
    print ('保存失败，编码重复')

@pytest.mark.carrierplat_manage
def test_carrierplat_delete(selenium):
    '''逻辑删除已新增的平台'''
    tms=Login(selenium)
    tms.tms_login()
    m=Menu(selenium)
    m.new_menu('承运商管理','承运商平台管理')
    delete=Carrier_management.carrier_platform_management(selenium)
    delete.delete('autotest')
    sleep (1)
    assert '修改成功' in delete.driver.page_source, print ('删除失败')
    print ('删除成功')

@pytest.mark.carrierplat_manage
def test_carrierplat_edit(selenium):
    '''编辑新增的承运商平台，启用/停用'''
    tms=Login(selenium)
    tms.tms_login()
    m=Menu(selenium)
    m.new_menu('承运商管理','承运商平台管理')
    edit=Carrier_management.carrier_platform_management(selenium)
    edit.query('autotest')
    status_first = edit.find_element (R.Carrier_platform_manage.first_status).text
    print('当前状态：'+status_first)
    edit.edit('autotest')
    status_end = edit.find_element (R.Carrier_platform_manage.first_status).text
    print('当前状态：'+status_end)
    assert status_first != status_end, print ('编辑失败')
    print ('编辑成功')

@pytest.mark.carrierplat_manage
def test_carrierplat_query(selenium) :
    '''查询已新增的平台'''
    tms = Login (selenium)
    tms.tms_login ()
    m = Menu (selenium)
    m.new_menu ('承运商管理', '承运商平台管理')
    query = Carrier_management.carrier_platform_management (selenium)
    query.query ('autotest')
    result=query.find_element(R.Carrier_platform_manage.first_code).text
    assert 'autotest'==result,print('查询结果错误')
    print('保存成功，查询结果为：'+result+'，正确')





if __name__ == '__main__':
    from public import test
    test.runtc(__file__,  tclevel='carrierplat_manage', driver='Chrome')  # Firefox，Chrome