#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/15
# @Author  : wanghui
import pytest
from business.pms.HomePage import Home
from business.pms.PoSet import PoSet
from business.pms.Resource import R
from business.manage.manage_home import ManageSystem



@pytest.mark.pms_0
def test_search_by_productCode(selenium):
    """根据产品编码查询"""
    mgr=ManageSystem(selenium)     #集成管理系统
    mgr.login_with_account()     #登录
#     mgr.chose_subsystem('采购管理系统(集团)','系统仓库')     #进入-采购管理系统(集团)
    mgr.choose_subsystem_from_mysystem("采购管理系统")  #从我的工作台更多中，进入采购管理系统(集团)
    h=Home(selenium)     #PMS
    h.go_po_set()
    p = PoSet(selenium)
    product_code=p.driver.find_element_by_css_selector('.l-grid-body-table>tbody>tr>td[columnname="productCode"]>div').text 
    print('查找商品编码：',product_code)
    p.get_search_by_productCode(product_code)
    table_item = p.find_element(R.po_set.table_items)
    table_items_rows = table_item.find_elements_by_tag_name('tr')
    assert len(table_items_rows)>0

if __name__ == '__main__':
    from public import test
    test.runtc(__file__, 'pms_0',driver='Chrome')