'''
# -*- coding: utf-8 -*-
#开发人员:   chenpeng
#开发日期:   2019-04-17 16:13:47
#文件项目:   TMS
#文件名称:   免邮设置
 '''
import pytest
from business.tms.Carrier_management import Carrier_management
from business.tms.MenuPage import Menu
from business.tms.login import Login
from business.tms.Resource import R
from time import sleep
import random

# def setup_function(selenium):
#     print ("setup_function():每个方法之前执行")
#     a=random.randint(1,5)
#     print(a)

# def teardown_function(selenium):
#     print ("teardown_function():每个方法之后执行")


@pytest.mark.freight_setup
def test_freight_setup_add(selenium):
    '''新增一个免邮，检验是否保存成功'''
    sql_del=Carrier_management.carrier_platform_management(selenium)
    SQL='DELETE from free_postage where bussiness_id=%s'
    COND='222'
    sql_del.mysql_delete(SQL,COND)
    #登录TMS
    tms = Login (selenium)
    tms.tms_login ()
    print('登录')
    m = Menu (selenium)
    m.new_menu ('承运商管理', '免邮接口')
    add = Carrier_management.freight_free_setup (selenium)
    add.add(COND,100,30)
    sleep(1)
    add.query(222)
    sleep(1)
    result=add.find_element(R.mysz.id_line1).text
    print('查询成功，商家ID为：'+result)
    assert COND == result
    print('新增成功')


@pytest.mark.freight_setup
def test_freight_setup_add_repeat(selenium):
    '''新增一个免邮，检验是否重复并提示'''
    #登录TMS
    tms = Login (selenium)
    tms.tms_login ()
    print('登录')
    m = Menu (selenium)
    m.new_menu ('承运商管理', '免邮接口')
    add = Carrier_management.freight_free_setup (selenium)
    add.add(111,100,30)
    sleep(1)
    assert '数据已存在' in add.driver.page_source
    print('保存失败，当前商家已存在')

@pytest.mark.freight_setup
def test_freight_setup_edit(selenium):
    '''编辑当前新增规则'''
    #登录TMS
    tms = Login (selenium)
    tms.tms_login ()
    m = Menu (selenium)
    m.new_menu ('承运商管理', '免邮接口')
    edit=Carrier_management.freight_free_setup(selenium)
    edit.query(111)
    sleep(1)
    result1=edit.find_element(R.mysz.freefee_line1).text
    print('free1='+result1)
    a=random.randrange(200,1000,100)
    print(a)
    edit.edit(str(a),'60')
    sleep(1)
    edit.query(111)
    result2=edit.find_element(R.mysz.freefee_line1).text
    print('free2='+result2)
    assert result2==str(a)
    print('编辑成功')

@pytest.mark.freight_setup
def test_freight_setup_onoff(selenium):
    '''启用/停用当前新增规则'''
    #登录TMS
    tms = Login (selenium)
    tms.tms_login ()
    m = Menu (selenium)
    m.new_menu ('承运商管理', '免邮接口')
    onoff=Carrier_management.freight_free_setup(selenium)
    onoff.query(111)
    result1=onoff.find_element(R.mysz.switch).text
    print('当前状态：'+result1)
    sleep(1)
    onoff.onoff()
    sleep(1)
    result2=onoff.find_element(R.mysz.switch).text
    print('当前状态：'+result2)
    assert result1!=result2
    print('当前规则已启用/停用')




if __name__ == '__main__':
    from public import test
    test.runtc(__file__, tclevel='freight_setup', driver='Chrome')  # Firefox，Chrome