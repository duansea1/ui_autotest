'''
# -*- coding: utf-8 -*-
#开发人员:   chenpeng
#开发日期:   2019-04-18
#文件项目:   TMS
#文件名称:   配送规则管理
 '''

import pytest
from business.tms.Carrier_management import Carrier_management
from business.tms.MenuPage import Menu
from business.tms.login import Login
from business.tms.Resource import R
from time import sleep
import random

@pytest.mark.delivery_rules_manage
def test_delivery_rules_add(selenium):
    '''新增一条配送规则'''
    tms=Login(selenium)
    tms.tms_login()
    m=Menu(selenium)
    m.menu('承运商管理', '配送规则管理')
    add=Carrier_management.Delivery_rules_manage(selenium)
    a=['广州药业仓库（新）','昆山亿方药业仓']
    add.add(a[0],'自动化测试承运商','药城','是'
            ,'湖北','武汉市','洪山区','关山街道'
            ,'24','0','1000')
    # add.add(['广州药业仓库（新）'],['自动化测试承运商'],['药城'],['是']
    #         ,['湖北'],['武汉市'],['洪山区'],['关山街道']
    #         ,['24'],['0'],['1000'])
    sleep(1)
    add.query('广州药业仓库（新）','自动化测试承运商','湖北','武汉市','洪山区','关山街道')
    result=add.find_element(R.Psgz.first_carrier).text
    assert '自动化测试承运商' == result
    print('配送规则新增成功')

@pytest.mark.delivery_rules_manage
def test_delivery_rules_add_repeat(selenium):
    '''新增一条配送规则，校验是否重复'''
    tms=Login(selenium)
    tms.tms_login()
    m=Menu(selenium)
    m.menu('承运商管理', '配送规则管理')
    add=Carrier_management.Delivery_rules_manage(selenium)
    #a=['广州药业仓库（新）','昆山亿方药业仓']
    add.add('广州药业仓库（新）','自动化测试承运商','药城','是'
            ,'湖北','武汉市','洪山区','关山街道'
            ,'24','0','1000')
    sleep(1)
    assert '此规则已经存在' in add.driver.page_source
    print('此规则已经存在，请勿重复添加')

@pytest.mark.delivery_rules_manage
def test_delivery_rules_edit(selenium):
    '''编辑新增的配送规则'''
    tms=Login(selenium)
    tms.tms_login()
    m=Menu(selenium)
    m.menu('承运商管理', '配送规则管理')
    edit=Carrier_management.Delivery_rules_manage(selenium)
    edit.query('广州药业仓库（新）','自动化测试承运商','湖北','武汉市','洪山区','关山街道')
    edit.edit('72','1','100')
    sleep(1)
    print ('切换到iframe1')
    a = edit.find_element (R.tms_menu.iframe1)
    edit.driver.switch_to.frame (a)
    result=edit.find_element(R.Psgz.first_deliverytime).text
    onoff_status1=edit.find_element(R.Psgz.switch).text
    print('当前配送时效：'+result)
    assert '72' == result
    print('编辑成功')
    edit.onoff()
    onoff_status2=edit.find_element(R.Psgz.switch).text
    assert onoff_status1 !=onoff_status2
    print('此规则已启用/停用')

@pytest.mark.delivery_rules_manage
def test_delivery_rules_delete(selenium):
    '''删除已添加的配送规则'''
    tms=Login(selenium)
    tms.tms_login()
    m=Menu(selenium)
    m.menu('承运商管理', '配送规则管理')
    delete=Carrier_management.Delivery_rules_manage(selenium)
    delete.query('广州药业仓库（新）','自动化测试承运商','湖北','武汉市','洪山区','关山街道')
    delete.delete()


if __name__ == '__main__':
    from public import test
    test.runtc(__file__, tclevel='delivery_rules_manage', driver='Chrome')  # Firefox，Chrome




