'''
# -*- coding: utf-8 -*-
#开发人员:   chenpeng
#开发日期:   2019-04-24
#文件项目:   TMS
#文件名称:   配送时效管理
 '''

import pytest
from business.tms.Carrier_management import Carrier_management
from business.tms.MenuPage import Menu
from business.tms.login import Login
from business.tms.Resource import R
from time import sleep

@pytest.mark.delivery_time_manage
def test_delivery_time_template_upload(selenium):
    '''新增配送时效模板'''
    tms=Login(selenium)
    tms.tms_login()
    m=Menu(selenium)
    m.menu('承运商管理', '配送时效管理')
    upload = Carrier_management.delivery_time_manage(selenium)
    upload.upload()
    carrier="自动化测试承运商"
    print('切换到主文档')
    upload.driver.switch_to.default_content()
    upload.query(carrier)
    result=upload.find_element(R.delivery_time_template.carrier_line1).text
    sleep(1)
    assert result == carrier
    print("配送时效导入成功")

@pytest.mark.delivery_time_manage
def test_delivery_time_template_edit(selenium):
    '''修改配送时效模板'''
    tms=Login(selenium)
    tms.tms_login()
    m=Menu(selenium)
    m.menu('承运商管理', '配送时效管理')
    edit=Carrier_management.delivery_time_manage(selenium)
    carrier="自动化测试承运商"
    delivery_time="72H"
    edit.query(carrier)
    result1=edit.find_element(R.delivery_time_template.delivery_time_line1).text
    edit.edit(carrier,delivery_time)
    sleep(1)
    edit.query(carrier)
    sleep(0.5)
    result2=edit.find_element(R.delivery_time_template.delivery_time_line1).text
    print("编辑前配送时效为："+result1,"编辑后配送时效为："+result2)
    assert  result1!=result2
    print('修改成功')

@pytest.mark.delivery_time_manage
def test_delivery_time_template_delete(selenium):
    '''删除配送时效模板'''
    tms=Login(selenium)
    tms.tms_login()
    m=Menu(selenium)
    m.menu('承运商管理', '配送时效管理')
    delete=Carrier_management.delivery_time_manage(selenium)
    carrier="自动化测试承运商"
    delete.query(carrier)
    delete.delete()
    sleep(1)
    result=delete.find_element(R.delivery_time_template.tips_nodata).text
    assert result=="无数据"
    print("删除成功")




if __name__ == '__main__':
    from public import test
    test.runtc(__file__,  tclevel='delivery_time_manage', driver='Chrome')  # Firefox，Chrome