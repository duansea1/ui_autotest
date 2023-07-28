'''
Created on 2019/3/8

@author: liya
'''

import pytest
from business.pms.HomePage import Home
from business.pms.PoManagement import PoManagement
from business.pms.Resource import R
from business.manage.manage_home import ManageSystem
from time import sleep


@pytest.mark.pms_2
@pytest.mark.test_supply_1
def test_po_auto_assert(selenium):
    """自动化专用商品PO-状态：完成-校验"""
    mgr = ManageSystem(selenium)  # 集成管理系统
    mgr.login_with_account()  # 登录
    #     mgr.chose_subsystem('采购管理系统(集团)','系统仓库')     #进入-采购管理系统(集团)
    mgr.choose_subsystem_from_mysystem("采购管理系统")  # 从我的工作台更多中，进入采购管理系统(集团)
    h = Home(selenium)  # PMS
    h.go_po_management()
    p = PoManagement(selenium)
    p.search_product_to_po('2916903579','0')  #搜索自动化测试专用商品的最新po，查询
    # p.po_query_test(po_code,'2018-1-1')  #输入po单号，查询
    po_status = p.po_status()
    assert '完成' in po_status  #完成后的PO状态校验
if __name__ == '__main__':
    from public import test

    test.runtc(__file__, tclevel='test_supply_1', driver='Chrome')  # Firefox，Chrome