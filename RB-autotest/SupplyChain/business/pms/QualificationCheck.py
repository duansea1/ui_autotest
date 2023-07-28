#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/5/23
# @Author  : wanghui
from time import sleep
from business.pms import BasePage
from business.pms.Resource import R

class QualificationCheck(BasePage.Base):
    """homepage 对象"""

    def search_all(self):
        """查询一年内数据"""
        self.click(R.qualification_check.create_time)
        start_time = self.getDatetimeSub(-365).strftime('%Y-%m-%d')#当前时间一年前日期
        self.driver.find_element_by_name('daterangepicker_start').clear()
        self.send_keys(R.qualification_check.start_time,start_time)
        self.click(R.qualification_check.time_confirm_button)
        self.click(R.qualification_check.search)
        sleep(2)

    def search_by_supplier_code(self,supplier_code):
        """根据供应商编号查询"""
        self.search_all()
        self.send_keys(R.qualification_check.supplier_code,supplier_code)
        self.click(R.qualification_check.search)
        sleep(2)

    def search_by_supplier_name(self,supplier_name):
        """根据供应商名称查询"""
        self.search_all()
        self.send_keys(R.qualification_check.supplier_name,supplier_name)
        self.click(R.qualification_check.search)
        sleep(2)


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
