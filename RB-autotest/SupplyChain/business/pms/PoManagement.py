#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/22
# @Author  : wanghui
from time import sleep

from selenium import webdriver
from business.pms.Resource import R
from business.pms import BasePage
from business.pms.HomePage import Home
from selenium.webdriver.support.select import Select




class PoManagement(BasePage.Base):
    """homepage 对象"""

    def search_all(self):
        """
        查询全部
        :return:
        """
        self.click(R.auto_po_management.search)
        sleep(10)


    def get_search_by_product_code(self,product_code):
        """
        根据产品编码查询
        :return:
        """
        self.click(R.auto_po_management.search)
        sleep(3)
        self.send_keys(R.auto_po_management.product_code,product_code)
        self.click(R.auto_po_management.search)
        sleep(3)

    # def po_url(self):
    #     """PO_url"""
    #     print("进入PO管理")
    #     url = 'http://pms.111.com.cn/jsp/po/purchaseOrderManagement.jsp'
    #     self.driver.get(url)
    #     sleep(3)
    #     self.switch_to_latest_windows()


    def search_product_to_po(self, product_code,value='0'):
        """搜索产品编码-提取po，并查询最新的po单号"""
        print('打印当前页面：' + self.driver.title)
        # print('页面源码' + self.get_page_source())
        sleep(1)
        print('点击重置')
        self.click(R.to_management.reset_btn)
        print('输入产品编码：'+ product_code)
        self.send_keys(R.po_management.product_code,product_code)
        # self.driver.find_element_by_xpath('//*[@id="toolbar2"]/div[2]/span').click()\
        print('选择po类型：%s' % value)
        select = Select(self.driver.find_element_by_id('poType'))
        select.select_by_value(value)
        print('查询')
        self.click(R.po_management.query_btn)
        sleep(1)
        new_po = self.driver.find_element_by_xpath('//*[@id="maingrid4|2|r1001|c103"]/div/a').text
        print('新po单号：' + new_po)
        print('输入po单号')
        self.send_keys(R.po_management.po_code,new_po)
        sleep(1)
        print('查询')
        self.click(R.po_management.query_btn)
        sleep(1)
        return new_po


    def po_query_test(self,po_code,createdate,value='0'):
        """查询自动化专用po"""
        print('打印当前页面：'+ self.driver.title)
        print("输入po编码")
        # self.driver.find_element_by_name('poCodes').click()
        self.send_keys(R.po_management.po_code,po_code)
        sleep(1)
        print("输入po生成时间")
        self.send_keys(R.po_management.po_createdate,createdate)
        sleep(1)
        print('选择po类型：'+ value)
        select = Select(self.driver.find_element_by_id('poType'))
        select.select_by_value(value)
        print("查询")
        self.click(R.po_management.query_btn)
        sleep(1)

    def po_copy(self):
        "复制PO"
        print('复制po')
        # print(value)
        # if value == '0':
        self.click(R.po_management.copy_po)
        # elif value == '1':
        #     self.click(R.po_management.copy_rtv)
        sleep(1)
        self.switch_to_latest_windows()
        print("复制PO-弹窗-是")
        self.click(R.po_management.copy_yes_btn)
        sleep(1)
        self.switch_to_latest_windows()
        po_info = self.driver.find_element_by_xpath('/html/body/div[6]/table/tbody/tr[2]/td[2]/div/div[1]').text
        new_po = po_info.split(":")[1]
        print('po信息：' + po_info)
        print('po信息：' + new_po)
        print('复制PO-弹窗-确认按钮')
        self.click(R.po_management.confirm_btn)
        sleep(2)
        self.po_status()
        return new_po

        # assert '待批准' in self.po_status()

    # def po_new_code(self):
    #     po_code = self.po_copy().split[':'][1]
    #     print(po_code)
    #     return po_code

    def po_status(self):
        """po状态"""
        po_status = self.driver.find_element_by_xpath('//*[@id="maingrid4|2|r1001|c104"]/div').text
        print("po状态：" + po_status)
        return po_status

    def po_approve(self):
        """po批准"""
        # po_status = self.driver.find_element('//*[@id="maingrid4|2|r1001|c104"]/div').text
        # print("po状态：" + po_status)
        # self.po_status()
        print('po批准-勾选po单')
        self.click(R.po_management.chose)
        sleep(1)
        print("po批准-批准po")
        self.click(R.po_management.approve)
        sleep(1)
        self.switch_to_latest_windows()
        print("po批准-弹窗-是")
        self.click(R.po_management.copy_yes_btn)
        sleep(1)
        self.switch_to_latest_windows()
        # info = self.driver.find_element_by_xpath('/html/body/table/tbody/tr/td').text
        # print("批准po信息：" + info)
        self.click(R.po_management.close)
        sleep(1)
        # print("po状态：" + po_status)
        self.po_status()
        # assert '待收发' in self.po_status()

    def po_confirm_send(self):
        """po确认发货"""
        # self.po_status()
        print('确认发货-勾选po单')
        self.click(R.po_management.chose)
        sleep(1)
        print('确认发货-确认发货')
        self.click(R.po_management.confirm_send)
        sleep(1)
        self.switch_to_latest_windows()
        print("确认发货-弹窗-是")
        self.click(R.po_management.send_yes_btn)
        sleep(1)
        self.click(R.po_management.confirm_btn)
        # send_info = self.driver.find_element_by_xpath('/html/body/div[7]/table/tbody/tr[2]/td[2]/div/div[1]').text
        # print('确认发货信息：' + send_info)
        sleep(1)
        self.po_status()
        # assert '待收发货' in self.po_status()


    def negative_po(self):
        """负po生成RTV"""
        self.po_status()
        print('勾选po单')
        self.click(R.po_management.chose)
        print('负po生成RTV')
        self.click(R.po_management.negative_po_create_rtv_btn)
        sleep(1)
        self.switch_to_latest_windows()
        self.click(R.po_management.send_yes_btn)
        sleep(1)
        self.switch_to_latest_windows()
        self.click(R.po_management.negative_po_close_btn)
        sleep(1)
        self.po_status()
        # assert '待收发' in self.po_status()




















