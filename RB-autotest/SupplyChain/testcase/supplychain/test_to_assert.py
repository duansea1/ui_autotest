'''
Created on 2019/3/8

@author: liya
'''
import pytest
from business.pms.HomePage import Home
from business.pms.ToManagement import ToManagement
from business.pms.Resource import R
from business.manage.manage_home import ManageSystem
from time import sleep



@pytest.mark.pms_1
def test_to_out_assert(selenium,to_code):
    """自动化专用商品TO-调拨出库后状态：已出库-校验"""
    mgr = ManageSystem(selenium)  # 集成管理系统
    mgr.login_with_account()  # 登录
#     mgr.chose_subsystem('采购管理系统(集团)','系统仓库')     #进入-采购管理系统(集团)
    mgr.choose_subsystem_from_mysystem("采购管理系统")  # 从我的工作台更多中，进入采购管理系统(集团)
    h = Home(selenium)  # PMS
    h.go_to_management()
    t = ToManagement(selenium)
    # t.search_product_to_to('2916903579')
    t.to_query(to_code)
    to_status = t.to_status()
    assert '已出库' in to_status  # 调拨出库后的TO状态校验


@pytest.mark.test_supply_input
@pytest.mark.pms_2
def test_to_in_assert(selenium,to_code):
    """自动化专用商品TO-调拨入库后状态:已完成-校验"""
    mgr = ManageSystem(selenium)  # 集成管理系统
    mgr.login_with_account()  # 登录
#     mgr.chose_subsystem('采购管理系统(集团)','系统仓库')     #进入-采购管理系统(集团)
    mgr.choose_subsystem_from_mysystem("采购管理系统")  # 从我的工作台更多中，进入采购管理系统(集团)
    h = Home(selenium)  # PMS
    h.go_to_management()   #搜索自动化测试专用商品的最新TO，查询
    t = ToManagement(selenium)
    # t.search_product_to_to('2916903579')
    t.to_query(to_code)  #输入to单号，查询
    to_status = t.to_status()
    assert '已完成' in to_status  # 调拨入库后的TO状态校验


if __name__ == '__main__':
    from public import test
    test.runtc(__file__,  tclevel='test_supply_input', driver='Chrome',
                 options=['--to_code=700072757970'])  # Firefox，Chrome