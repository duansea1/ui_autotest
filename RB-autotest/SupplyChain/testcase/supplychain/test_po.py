'''
Created on 2019/3/4

@author: liya
'''

"""
自动化专用商品-产品编码：2916903579
广州药业仓库（新）的 PO单：700743954139
"""

import pytest
from business.pms.HomePage import Home
from business.pms.PoManagement import PoManagement
from business.pms.Resource import R
from business.manage.manage_home import ManageSystem
from time import sleep
from interface.pms_job import Pms_Job


# @pytest.mark.test_supply_1
@pytest.mark.pms_0
def test_po(selenium):
    """自动化专用商品PO-复制-批准-确认发货（下PO）"""
    mgr=ManageSystem(selenium)     #集成管理系统
    mgr.login_with_account()     #登录
#     mgr.chose_subsystem('采购管理系统(集团)','系统仓库')     #进入-采购管理系统(集团)
    mgr.choose_subsystem_from_mysystem("采购管理系统")  #从我的工作台更多中，进入采购管理系统(集团)
    h = Home(selenium)  # PMS
    h.go_po()
    p = PoManagement(selenium)
    # p.search()
    p.po_query_test('700743954139','2018-1-1') #查询po,广州仓库（新）
    # p.po_query_test() #查询po
    p.po_copy()  #复制po
    p.po_approve()  #批准po
    p.po_confirm_send()  #确认发货
    po_status = p.po_status()
    assert '待收发货' in po_status  #确认发货后的PO状态校验

if __name__ == '__main__':
    from public import test
    test.runtc(__file__, tclevel='pms_0', driver='Chrome',)  # Firefox，Chrome
    