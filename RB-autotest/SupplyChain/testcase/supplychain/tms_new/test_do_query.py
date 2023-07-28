# -*- coding: utf-8 -*-
#开发人员:   chenpeng
#开发日期:   2019-4-15 15:48:05
#文件项目:   tms
#文件名称:   DO查询

import pytest
from business.tms.HomePage import Home
from business.manage.manage_home import ManageSystem
from business.tms.MenuPage import Menu
from business.tms.OrderManagement import OrderManagement
from business.tms.login import Login
from business.tms.Resource import R




@pytest.mark.do_query
def test_do_query1(selenium):
    '''查询do，并验证查询结果'''
    tms=Login(selenium)   #TMS系统
    tms.tms_login()       #登录TMS
    m = Menu(selenium)
    m.new_menu('订单管理','DO管理')  #进入订单管理-DO管理页面
    o = OrderManagement(selenium)
    do_code='7033048299'
    time_from="2018-03-01"
    o.query_do_code_byleavetime(do_code,time_from)  #查询DO单号
    result1 = o.find_element (R.DO_management.first_do).text  # DO单号
    assert do_code == result1, "查询结果不正确，测试不通过"
    # if do_code == result1:
    print ('查询结果DO为：' + result1 + "，测试通过")

@pytest.mark.do_query
def test_do_query2(selenium):
    '''查询结果无数据提示'''
    tms=Login(selenium)   #TMS系统
    tms.tms_login()       #登录TMS
    m = Menu(selenium)
    m.new_menu('订单管理','DO管理')  #进入订单管理-DO管理页面
    o = OrderManagement(selenium)
    do_code = '70330482991'
    time_from = "2018-03-01"
    o.query_do_code_byleavetime (do_code, time_from)  # 查询DO单号
    result1 = o.find_element (R.DO_management.tips_nodata).text  # DO单号
    assert '无数据' == result1
    print ('查询结果为：' + result1 + "，测试通过")



if __name__ == '__main__':
    from public import test
    test.runtc(__file__,  tclevel='do_query', driver='Chrome')  # Firefox，Chrome