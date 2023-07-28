'''
# -*- coding: utf-8 -*-
#开发人员:   chenpeng
#开发日期:   2019-04-19
#文件项目:   TMS
#文件名称:   运费模板管理
 '''

import pytest
from business.tms.Carrier_management import Carrier_management
from business.tms.MenuPage import Menu
from business.tms.login import Login
from business.tms.Resource import R
from time import sleep
from business.tms.TMS_mysql import TMS_mysql

@pytest.mark.delivery_rules_manage
def test_freight_templates_add(selenium):
    '''SQL删除已添加的全国模板并新增一条运费模板'''
    sql_del=Carrier_management.freight_templates_manage(selenium)
    SQL='DELETE FROM freight_temp where carrier_code = %s'
    COND='2222222'
    sql_del.sql_delete(SQL,COND)

    '''新增一条运费模板'''
    tms=Login(selenium)
    tms.tms_login()
    m=Menu(selenium)
    m.menu('承运商管理', '运费模板管理')
    add=Carrier_management.freight_templates_manage(selenium)
    add.add('广州药业仓库（新）','自动化测试承运商',
            '5','20','1','2','0','0','0','0','5',
            '5','30','1','5','0','0','0','0','5')

    sleep(1)
    add.query('广州药业仓库（新）','自动化测试承运商')
    result1=add.find_element(R.Yfmd.first_carrier).text
    result2=add.find_element(R.Yfmd.first_area).text
    print('承运商：'+result1,'收货区域'+result2)
    assert '自动化测试承运商' == result1
    print('配送规则新增成功')

@pytest.mark.delivery_rules_manage
def test_freight_templates_add_repeat(selenium):
    '''新增一条运费模板，校验是否重复'''
    tms=Login(selenium)
    tms.tms_login()
    m=Menu(selenium)
    m.menu('承运商管理', '运费模板管理')
    add=Carrier_management.freight_templates_manage(selenium)
    add.add('广州药业仓库（新）','自动化测试承运商',
            '5','20','1','2','0','0','0','0','5',
            '5','30','1','5','0','0','0','0','5')
    sleep(1)
    assert '运费模板已存在' in add.driver.page_source
    print('此规则已经存在，请勿重复添加')

@pytest.mark.delivery_rules_manage
def test_freight_templates_edit(selenium):
    '''编辑新增的运费模板'''
    tms=Login(selenium)
    tms.tms_login()
    m=Menu(selenium)
    m.menu('承运商管理', '运费模板管理')
    edit=Carrier_management.freight_templates_manage(selenium)
    sleep(1)
    edit.query('广州药业仓库（新）','自动化测试承运商')
    sleep(1)
    result1=edit.find_element(R.Yfmd.first_area).text
    edit.edit('6','31','1','5','0','0','0','0','6')
    sleep(1)
    edit.query('广州药业仓库（新）','自动化测试承运商')
    result2=edit.find_element(R.Yfmd.first_area).text
    print('编辑前收货区域：'+result1,'编辑后收获区域：'+result2)
    assert result1 != result2
    print('编辑成功')

@pytest.mark.delivery_rules_manage
def test_freight_templates_delete(selenium):
    '''删除已添加的运费模板'''
    tms=Login(selenium)
    tms.tms_login()
    m=Menu(selenium)
    m.menu('承运商管理', '运费模板管理')
    delete=Carrier_management.freight_templates_manage(selenium)
    sleep(1)
    delete.query('广州药业仓库（新）','自动化测试承运商')
    delete.delete()
    sleep(1)
    delete.query('广州药业仓库（新）','自动化测试承运商')
    sleep(1)
    result=delete.find_element(R.Yfmd.first_allarea).text
    assert  '[全国]'== result
    print('删除成功')


if __name__ == '__main__':
    from public import test
    test.runtc(__file__, tclevel='delivery_rules_manage', driver='Chrome')  # Firefox，Chrome
