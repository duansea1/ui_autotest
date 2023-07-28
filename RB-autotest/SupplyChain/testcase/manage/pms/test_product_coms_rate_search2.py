#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/4/27
# @Author  : wanghui
import pytest
from business.pms.HomePage import Home
from business.pms.ProductComsRateSearch import ProductComsRatesSearch
from business.pms.Resource import R
from business.manage.manage_home import ManageSystem


@pytest.mark.pms_1
def test_supplier_maanshan(selenium):
    """菜单：商家管理--产品佣金比率查询，按产品编码查询功能正确"""
    mgr=ManageSystem(selenium)     #集成管理系统
    mgr.login_with_account()     #登录
#     mgr.chose_subsystem('采购管理系统(集团)','系统仓库')     #进入-采购管理系统(集团)
    mgr.choose_subsystem_from_mysystem("采购管理系统")  #从我的工作台更多中，进入采购管理系统(集团)
    h=Home(selenium)     #PMS
    h.go_product_Coms_Rate_search()
    s =ProductComsRatesSearch(selenium)
    s.get_search_result()
    product_code = s.driver.find_element_by_css_selector('.l-grid-body-table>tbody>tr>td[columnname="productCode"]>div').text   #产品编码
    s.get_search_by_product_code(product_code)
    table_item = s.find_element(R.product_Coms_Rate_search.table_items)
    table_items_rows = table_item.find_elements_by_tag_name ( 'tr' )
    assert len(table_items_rows)>0

if __name__ == '__main__':
    from public import test
    test.runtc(__file__, 'pms_0',driver='Chrome')