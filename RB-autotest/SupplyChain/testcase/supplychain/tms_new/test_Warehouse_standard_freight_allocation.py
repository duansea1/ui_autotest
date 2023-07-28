'''
# -*- coding: utf-8 -*-
#开发人员:   
#开发日期:   
#文件项目:   
#文件名称:   
 '''

import pytest
from business.tms.Carrier_management import Carrier_management
from business.tms.MenuPage import Menu
from business.tms.login import Login
from business.tms.Resource import R
from time import sleep

@pytest.mark.Warehouse_standard_freight_allocation
def test_Warehouse_standard_freight_allocation_add(selenium):
    '''SQL物理删除仓库运费配置并新增仓库运费配置'''
    add1=Carrier_management.Warehouse_standard_freight_allocation(selenium)
    SQL='DELETE from warehouse_freight where warehouse_id=%s'
    warehouse_id="1"
    warehouse_name='自动化测试专用仓库'
    add1.sql_del(SQL,warehouse_id)
    tms=Login(selenium)
    tms.tms_login()
    m=Menu(selenium)
    m.menu('承运商管理', '仓库标准运费配置')
    add1.add(warehouse_name,'6.6','20','30')
    add1.query(warehouse_name)
    sleep(1)
    result=add1.find_element(R.Ckyf.warehouse_line1).text
    assert result == warehouse_name
    print('新增成功')

@pytest.mark.Warehouse_standard_freight_allocation
def test_Warehouse_standard_freight_allocation_add_repeat(selenium):
    '''新增仓库运费配置校验重复'''
    warehouse_name='自动化测试专用仓库'
    tms=Login(selenium)
    tms.tms_login()
    m=Menu(selenium)
    m.menu('承运商管理', '仓库标准运费配置')
    add2=Carrier_management.Warehouse_standard_freight_allocation(selenium)
    add2.add(warehouse_name,'6.6','20','30')
    assert '该仓库运费模板已存在！' in add2.driver.page_source
    print('该仓库运费模板已存在！')

@pytest.mark.Warehouse_standard_freight_allocation
def test_Warehouse_standard_freight_allocation_edit(selenium):
    '''编辑新增仓库运费配置'''
    warehouse_name='自动化测试专用仓库'
    tms=Login(selenium)
    tms.tms_login()
    m=Menu(selenium)
    m.menu('承运商管理', '仓库标准运费配置')
    edit=Carrier_management.Warehouse_standard_freight_allocation(selenium)
    edit.query(warehouse_name)
    result1=edit.find_element(R.Ckyf.fee_line1).text
    edit.edit('7.7','21')
    edit.query(warehouse_name)
    result2=edit.find_element(R.Ckyf.fee_line1).text
    print('编辑前运费为：'+result1,'编辑后运费为：'+result2)
    assert result2 == '21'
    print('编辑成功')

@pytest.mark.Warehouse_standard_freight_allocation
def test_Warehouse_standard_freight_allocation_delete(selenium):
    '''删除新增仓库运费配置'''
    warehouse_name='自动化测试专用仓库'
    tms=Login(selenium)
    tms.tms_login()
    m=Menu(selenium)
    m.menu('承运商管理', '仓库标准运费配置')
    delete=Carrier_management.Warehouse_standard_freight_allocation(selenium)
    delete.query(warehouse_name)
    result1 = delete.find_element (R.Ckyf.area_line1).text
    delete.delete()
    delete.switch_to_iframe1()
    result2 = delete.find_element (R.Ckyf.area_line1).text
    print('删除前第一条收货区域：'+result1,'删除后第一条收货区域：'+result2)
    assert result1 != result2
    print('删除成功')


if __name__ == "__main__":
    from public import test
    test.runtc(__file__,tclevel='Warehouse_standard_freight_allocation',driver='Chrome')

