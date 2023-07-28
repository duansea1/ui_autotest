'''
# -*- coding: utf-8 -*-
#开发人员:   chenpeng
#开发日期:   2019-04-28
#文件项目:   TMS
#文件名称:   称重管理
 '''

import pytest
from business.tms.Weighing_management import Weighing_management
from business.tms.MenuPage import Menu
from business.tms.login import Login
from business.tms.Resource import R
from time import sleep
import time

@pytest.mark.Weighing_management
def test_freight_calculate(selenium):
    '''计算运费并核对页面结果'''
    tms=Login(selenium)
    tms.tms_login()
    m=Menu(selenium)
    m.menu('称重管理', '运费对账')
    calculate=Weighing_management.freight_checkout(selenium)
    calculate.do_query()
    calculate_freight=calculate.freight_calculate()[0]
    freight=calculate.freight_calculate()[1]
    print('实际运费为：'+freight,'计算的运费为：'+str(calculate_freight))
    assert str(calculate_freight) == freight
    print('运费计算正确')

@pytest.mark.Weighing_management
def test_handover_bysel(selenium):
    '''交接选择的订单--已称重+未交接'''
    tms=Login(selenium)
    tms.tms_login()
    m=Menu(selenium)
    m.menu('称重管理', '称重管理')
    handover=Weighing_management.weighing_management(selenium)
    handover.query('2018-02-01 00:00:00','未交接','已称重')
    do_line1=handover.find_element(R.Czgl.do_line1).text
    status1=handover.find_element(R.Czgl.status_line1).text
    print('第一个DO为：'+do_line1,"交接状态为："+status1)
    carrier_number=handover.carrier_check()
    warehouse_number=handover.warehouse_check()
    print('当前页承运商个数：'+str(carrier_number),'当前页仓库个数：'+str(warehouse_number))
    sleep(1)
    curent_time = time.strftime ('%Y-%m-%d %H:%M:%S', time.localtime (time.time ()))
    handover.handover_bysel(curent_time)
    sleep(1)
    print('校验所选订单是否同一供应商和仓库')
    if carrier_number !=1 and warehouse_number == 1:
        assert '勾选订单不是同一承运商'  in handover.driver.page_source
        print('勾选订单不是同一承运商,交接失败')
    elif carrier_number == 1 and warehouse_number !=1:
        assert  '勾选订单不是同一仓库' in handover.driver.page_source
        print('勾选订单不是同一仓库,交接失败')
    elif carrier_number ==1 and warehouse_number == 1:
        handover.do_handover_state_query('已交接',do_line1)
        status2 = handover.find_element (R.Czgl.status_line1).text
        print('第一个DO为：'+do_line1,"交接状态为："+status2)
        assert status2 == '已交接'
        print('当前页订单为同一承运商统一仓库,交接成功')
    else:
        assert '勾选订单不是同一承运商' in handover.driver.page_source
        print ('勾选订单不是同一承运商且不是同一仓库,交接失败')

@pytest.mark.Weighing_management
def test_handover_notweight(selenium):
    '''交接未称重的订单'''
    tms=Login(selenium)
    tms.tms_login()
    m=Menu(selenium)
    m.menu('称重管理', '称重管理')
    handover=Weighing_management.weighing_management(selenium)
    handover.samedata_query('广州药城德邦','广州药业仓库（新）','2018-02-01 00:00:00','全部','未称重')
    curent_time = time.strftime ('%Y-%m-%d %H:%M:%S', time.localtime (time.time ()))
    handover.handover_all(curent_time)
    sleep(1)
    assert '勾选订单有未完成称重' in handover.driver.page_source
    print ('勾选订单有未完成称重,交接失败')

@pytest.mark.Weighing_management
def test_handover_nothandover(selenium):
    '''交接已交接的订单'''
    tms=Login(selenium)
    tms.tms_login()
    m=Menu(selenium)
    m.menu('称重管理', '称重管理')
    handover=Weighing_management.weighing_management(selenium)
    handover.samedata_query('广州药城德邦','广州药业仓库（新）','2018-02-01 00:00:00','已交接','已称重')
    curent_time = time.strftime ('%Y-%m-%d %H:%M:%S', time.localtime (time.time ()))
    handover.handover_all(curent_time)
    sleep(1)
    assert '勾选订单有已完成交接' in handover.driver.page_source
    print ('勾选订单有已完成交接,交接失败')



if __name__ == "__main__":
    from public import test
    test.runtc(__file__,tclevel='Weighing_management',driver='Chrome')