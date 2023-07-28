#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/7
# @Author  : wanghui

#from webbrowser import browser
from business.pms import BasePage
from business.pms.Resource import R
from time import sleep


class Home(BasePage.Base):
    """homepage 对象"""

    @staticmethod
    def get_page_title(selenium):
        """
        获取页面标题
        :param selenium:
        :return:
        """
        print('The page title is:%s' % selenium.title)
        return selenium.title

    def go_supplier_manager_check(self):
        """
        进入菜单：质管负责人审核
        :param selenium:
        :return:
        """
        url = R.supplier_manager_check.menu_link
        self.driver.get(url)
        sleep(3)

    def go_supplier_check(self):
        """
        进入菜单：质管审核
        :return:
        """
        url = R.supplier_check.menu_link
        self.driver.get(url)
        sleep(3)

    def go_supplier(self):
        """
        进入菜单：供应商管理
        :param selenium:
        :return:
        """
        url = R.supplier.menu_link
        self.driver.get(url)
        sleep(3)

    def go_qualification_check(self):
        """
        进入菜单：供应商资质管理
        :return:
        """
        url = R.qualification_check.menu_link
        self.driver.get ( url )
        sleep ( 3 )

    def go_po_order(self):
        """
        进入菜单：自动PO订单
        :return:
        """
        url = R.po_order.menu_link
        self.driver.get ( url )
        sleep ( 3 )

    def go_auto_po_sales_predic_management(self):
        """
        进入菜单：日销量预测
        :return:
        """
        url = R.auto_po_sales_predic_management.menu_link
        self.driver.get(url)
        sleep(3)

    def go_po_argument_set(self):
        """
        进入菜单：采购优化参数设置
        :return:
        """
        url = R.po_argument_set.menu_link
        self.driver.get(url)
        sleep(1)
        head=self.driver.find_element_by_css_selector('.header>.current')
        print(head.text)

#     def go_po_management(self):
#         """
# 
#         进入菜单：自动po管理
#         :return:
#         """
#         url = R.auto_po_management.menu_link
#         url = R.po_management.menu_link
#         self.driver.get(url)
#         sleep(3)
        
    def go_po_management(self):
        """进入菜单，po管理"""
        print("进入PO管理")
        url = 'http://pms.111.com.cn/jsp/po/purchaseOrderManagement.jsp'
        self.driver.get(url)
        sleep(3)
        handles = self.driver.window_handles  # 获取所有弹出窗口句柄
        self.driver.switch_to.window(handles[-1])  # 切换到弹出窗口

    def go_po(self):
        """进入菜单，po管理"""
        print('进入po管理')
        url = R.po_management.menu_link
        self.driver.get(url)
        sleep(3)

    def go_to_management(self):
        """进入菜单，to管理"""
        print('进入to管理')
        url = R.to_management.menu_link
        self.driver.get(url)
        sleep(3)

    def go_po_set(self):
        """
        进入菜单：自动po-设置
        :return:
        """
        url = R.po_set.menu_link
        self.driver.get(url)
        sleep(3)

    def go_po_lack_management(self):
        """
        进入菜单：PO缺货清单管理
        :return:
        """
        url= R.po_lack_management.menu_link
        self.driver.get(url)
        sleep(1)

    def go_product_Coms_Rate_search(self):
        """
        进入产品佣金比率查询
        :return:
        """
        url = R.product_Coms_Rate_search.menu_link
        self.driver.get(url)
        sleep(1)

    def go_merchant_coms_management(self):
        """
        进入菜单：商家佣金产品管理
        :return:
        """
        url = R.merchant_coms_management.menu_link
        self.driver.get(url)
        sleep(1)

    def go_merchant_coms_check(self):
        """
        进入菜单：商家佣金审核
        :return:
        """
        url = R.merchant_coms_check.menu_link
        self.driver.get(url)
        sleep(1)

    def go_contract_sync(self):
        """
        进入菜单：合同返利
        :return:
        """
        url=R.contract_sync.menu_link
        self.driver.get(url)
        sleep(1)

    def go_contract_manage(self):
        """
        进入菜单：合同管理
        :return:
        """
        url = R.contract_manage.menu_link
        self.driver.get(url)
        sleep(1)

    def go_contract_examine(self):
        """
        进入菜单：合同审批
        :return:
        """
        url = R.contract_examine.menu_link
        self.driver.get(url)
        sleep(1)

    def go_brand_manage(self):
        """
        进入菜单：品牌方管理
        :return:
        """
        url = R.brand_manage.menu_link
        self.driver.get(url)
        sleep(1)

    def go_deposit_examine(self):
        """
        进入菜单：保证金审核
        :return:
        """
        url = R.deposit_examine.menu_link
        self.driver.get(url)
        sleep(1)

    def go_supplier_product_inPrice_check(self):
        """
        进入菜单：进价一审
        :return:
        """
        url = R.supplier_product_inPrice_check.menu_link
        self.driver.get(url)
        sleep(1)

    def go_supplier_product_inPrice_check2(self):
        """
        进入菜单：进价二审
        :return:
        """
        url = R.supplier_product_inPrice_check2.menu_link
        self.driver.get(url)
        sleep(1)

    def go_supplier_product_quality_check_audit(self):
        """
        进入菜单：质量档案(首营品种审核)
        :return:
        """
        url = R.supplier_product_quality_check_audit.menu_link
        self.driver.get(url)
        sleep(1)

    def go_supplier_product_quality_check_list(self):
        """
        进入菜单：质量管理
        :return:
        """
        url = R.supplier_product_quality_check_list.menu_link
        self.driver.get(url)
        sleep(1)

    def go_inner_tran_order_management(self):
        """
        进入菜单：TO内采内退管理
        :return:
        """
        url = R.inner_tran_order_management.menu_link
        self.driver.get(url)
        sleep(1)

    def go_inner_po_management(self):
        """
        进入菜单：历史po内采
        :return:
        """
        url = R.inner_po_management.menu_link
        self.driver.get(url)
        sleep(1)

    

    def go_warehouse_management(self):
        """
        进入菜单：仓库管理
        :return:
        """
        url = R.warehouse_management.menu_link
        self.driver.get(url)
        sleep(1)

    def go_request_bill(self):
        """
        进入菜单：请货单
        :return:
        """
        url = R.request_bill.menu_link
        self.driver.get(url)
        sleep(1)

    def go_product_mapper(self):
        """
        进入菜单：客户对码管理
        :return:
        """
        url = R.product_mapper.menu_link
        self.driver.get(url)
        sleep(1)

    def go_kingbos_inner_tran_order_management(self):
        """
        进入菜单：门店内采内退管理
        :return:
        """
        url = R.kingbos_inner_tran_order_management.menu_link
        self.driver.get(url)
        sleep(1)

    def go_product_stock(self):
        """
        进入菜单：客户库存管理
        :return:
        """
        url = R.product_stock.menu_link
        self.driver.get(url)
        sleep(1)

    def go_imnormal_stock(self):
        """
        进入菜单：非备管理
        :return:
        """
        url = R.imnormal_stock.menu_link
        self.driver.get(url)
        sleep(1)

    def go_imnormal_stock_to_caikong(self):
        """
        进入菜单：非备-采控管理
        :return:
        """
        url = R.imnormal_stock_to_caikong.menu_link
        self.driver.get(url)
        sleep(1)