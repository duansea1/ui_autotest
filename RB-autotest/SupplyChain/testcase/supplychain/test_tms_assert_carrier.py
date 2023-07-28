"""
Created on 2019/3/9
@author: liya
"""

import pytest
import cx_Oracle
from business.warehouse_sys.wms_oracle_query import Wms_Oracle
from business.tms.HomePage import Home
from business.tms.MenuPage import Menu
from business.tms.Resource import R
from business.manage.manage_home import ManageSystem
from business.tms.OrderManagement import OrderManagement


@pytest.mark.test_supply_1
@pytest.mark.tiaoshi
def test_wms_oracle_query(selenium):
    '''查询wms数据库中的do号的预计出库时间运&承运商ID&运单号'''
    w = Wms_Oracle(selenium)
    w.clear_file('wms_do_carrier.txt')  # 清空文件内容
    w.wms_oracle_query()


@pytest.mark.test_supply_1
@pytest.mark.tiaoshi
def test_tms_assign_carrier(selenium):
    """TMS修改承运商"""
    mgr=ManageSystem(selenium)     #集成管理系统
    mgr.login_with_account()     #登录
    h = Home(selenium)
    h.go_to_tms_new_system()   #进入TMS新系统
    m = Menu(selenium)
    m.new_menu('订单管理','承运商指派')  #进入订单管理-承运商指派页面
    o = OrderManagement(selenium)
    o.query_do_code('CSXGCYSWD')  #查询DO单号
    o.do_status()    #DO单状态
    o.assign_carrier()  #指派承运商-圆通药网


@pytest.mark.test_supply_1
@pytest.mark.tiaoshi
def test_wms_do_carrier_assert(selenium):
    '''校验DO号中的预计出库时间运&承运商ID&运单号是否变更'''
    w = Wms_Oracle(selenium)
    w.wms_oracle_query() # tms修改承运商后，保存数据
    w.assert_do_carrier()  #校-验修改前后的数据，是否有变化
    # w.clear_file('wms_do_carrier.txt')  # 清空文件内容


if __name__ == '__main__':
    from public import test
    test.runtc(__file__,  tclevel='tiaoshi', driver='Chrome')  # Firefox，Chrome
