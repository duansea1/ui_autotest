#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/11
# @Author  : wanghui
from time import sleep
from business.pms import BasePage
from business.pms.Resource import R

class AutoPoSalesPredicManagement(BasePage.Base):
    """homepage 对象"""

    def search_all(self):
        """查询全部"""
        self.click(R.auto_po_sales_predic_management.search)
        sleep(3)


# if __name__ == '__main__':
#     driver = webdriver.Chrome()
#     driver.maximize_window()
#     h = Home(driver)
#     h.open_login_page(driver)
#     h.login()
#     h.enter_pms_platform()
#     h.go_qualification_check_kunshan()
#     t = qualification_check_guangzhou(driver)
#     t.search_all()
