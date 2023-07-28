'''
Created on 2019/3/4

@author: liya
'''

"""
自动化专用商品-产品编码：2916903579
RTV的单供应商是[陈氏药业]，如果后期该供应商的商品没有库存，走po单补充库存，再进行rtv退货操作；
RTV单号：700743955380，陈氏药业-广州药网仓库（新）的PO单号：700743955263
"""

import pytest
from business.pms.HomePage import Home
from business.pms.PoManagement import PoManagement
from business.pms.Resource import R
from business.manage.manage_home import ManageSystem
from time import sleep


# @pytest.mark.test_supply_1
@pytest.mark.pms_0
def test_rtv_copy_to_done(selenium):
    """自动化专用商品RTV-复制-批准-负po生成RTV（下RTV）"""
    mgr=ManageSystem(selenium)     #集成管理系统
    mgr.login_with_account()     #登录
#     mgr.chose_subsystem('采购管理系统(集团)','系统仓库')     #进入-采购管理系统(集团)
    mgr.choose_subsystem_from_mysystem("采购管理系统")  #从我的工作台更多中，进入采购管理系统(集团)
    h = Home(selenium)  # PMS
    h.go_po_management()
    p = PoManagement(selenium)
    p.po_query_test('700743955380','2018-1-1','1')  #查询RTV，广州仓库（新）
    p.po_copy()  #复制RTV
    p.po_approve()   #批准RTV
    p.negative_po()  #负po生成RTV
    po_status = p.po_status()
    assert '待收发货' in po_status # 批准后的rtv状态校验


if __name__ == '__main__':
    from public import test
    test.runtc(__file__, tclevel='test_supply_1', driver='Chrome')  # Firefox，Chrome
    