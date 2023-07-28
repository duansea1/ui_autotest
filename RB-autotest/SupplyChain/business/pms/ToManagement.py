'''
Created on 2019/3/4

@author: liya
'''
from time import sleep

from selenium import webdriver

from business.pms import BasePage
from business.pms.HomePage import Home
from business.pms.Resource import R


class ToManagement(BasePage.Base):
    """homepage 对象"""

    def to_query_test(self,to_code,to_createdate):
        """TO_查询自动化专用to"""
        print("输入TO编码")
        self.send_keys(R.to_management.to_code,to_code)
        sleep(1)
        print('修改TO生成时间')
        self.send_keys(R.to_management.to_createdate,to_createdate)
        print('查询按钮')
        self.click(R.to_management.query_btn)
        sleep(1)

    def search_product_to_to(self,product_code):
        """查询自动化专用商品的最新to，查询"""
        print('点击重置')
        self.click(R.to_management.reset_btn)
        print('输入产品编码：' + product_code)
        self.send_keys(R.po_management.product_code,product_code)
        sleep(1)
        print('查询')
        self.click(R.to_management.query_btn)
        sleep(1)
        new_to = self.driver.find_element_by_xpath('//*[@id="maingrid4|2|r1001|c103"]/div/a').text
        print('输入to号')
        self.send_keys(R.to_management.to_code,new_to)
        print('查询')
        self.click(R.to_management.query_btn)
        sleep(1)
        return new_to

    def to_query(self,to_code):
        """输入to号，查询"""
        print('输入to号')
        self.send_keys(R.to_management.to_code, to_code)
        print('查询')
        self.click(R.to_management.query_btn)
        sleep(1)

    def to_status(self):
        """to状态"""
        to_status = self.driver.find_element_by_xpath('//*[@id="maingrid4|2|r1001|c107"]/div').text
        print("to状态：" + to_status)
        return to_status

    def to_copy(self):
        """复制to"""
        print('勾选自动化专用TO')
        self.click(R.po_management.chose)
        sleep(1)
        print('复制TO')
        self.click(R.po_management.copy_po)
        sleep(1)
        print('弹窗-是')
        self.click(R.to_management.approve_yes_btn)
        sleep(1)
        self.switch_to_latest_windows()
        to_info = self.driver.find_element_by_xpath('/html/body/div[6]/table/tbody/tr[2]/td[2]/div/div[1]').text
        new_to = to_info.split(":")[1]
        print('TO信息：' + to_info)
        print('TO信息：' + new_to)
        print('复制TO-弹窗-确认按钮')
        self.click(R.po_management.confirm_btn)
        sleep(2)
        self.to_status()

    def to_approve(self):
        """to批准"""
        print('勾选自动化专用TO')
        self.click(R.po_management.chose)
        sleep(1)
        print('批准TO')
        self.click(R.to_management.to_approve)
        sleep(1)
        self.switch_to_latest_windows()
        print('弹框-是')
        self.click(R.to_management.approve_yes_btn)
        sleep(1)
        self.switch_to_latest_windows()
        print('审核通过-弹框-关闭')
        self.click(R.to_management.close)
        sleep(1)
        self.to_status()












