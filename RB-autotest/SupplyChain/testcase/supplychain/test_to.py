'''
Created on 2019/3/4

@author: liya
'''
"""
自动化专用商品-产品编码：2916903579
广州药业仓库（新）-天津仓 的 TO单：700072757727
"""

import pytest
from business.pms.HomePage import Home
from business.pms.ToManagement import ToManagement
from business.pms.Resource import R
from business.manage.manage_home import ManageSystem
from time import sleep


# @pytest.mark.test_supply_1
@pytest.mark.pms_0
def test_to_copy_to_done(selenium):
    """自动化专用商品TO-复制-批准（下TO）"""
    mgr=ManageSystem(selenium)     #集成管理系统
    mgr.login_with_account()     #登录
#     mgr.chose_subsystem('采购管理系统(集团)','系统仓库')     #进入-采购管理系统(集团)
    mgr.choose_subsystem_from_mysystem("采购管理系统")  #从我的工作台更多中，进入采购管理系统(集团)
    h = Home(selenium)  # PMS
    h.go_to_management()
    t = ToManagement(selenium)
    t.to_query_test('700072757727','2018-1-1')   #查询TO单：广州药业仓库（新）--天津仓
    t.to_copy()  # TO复制 ：广州药业仓库（新）--天津仓
    t.to_approve()  # TO批准
    to_status = t.to_status()
    assert '已审核' in to_status  # 批准后的TO状态校验


if __name__ == '__main__':
    from public import test
    test.runtc(__file__, tclevel='test_supply_1', driver='Chrome')  # Firefox，Chrome
    # args = ['test_po_copy_to_done.py', '-m pms_0', '--driver=Chrome']
    # pytest.main(args)