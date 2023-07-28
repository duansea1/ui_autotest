#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/9
# @Author  : zhangqinqin
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from business.tms import BasePage
from business.tms.Resource import R
from time import sleep
from selenium.webdriver.common.by import By
class Menu(BasePage.Base):
    """menupage 对象"""


    def get_result_by_parentMenu(self,i):
        """
        获取根据父订单查询的结果
        :param i: 第i个选项
        :return:
        """
        parentMenu_list = self.find_element(R.menu.parentMenu)
        print(parentMenu_list)
        parentMenu_list.find_element_by_xpath('//*[@id="parentId"]/option['+str(i)+']').click()
        sleep(2)
        self.click(R.menu.search)
        sleep(5)

    def get_result_by_url(self,url):
        """
        获取根据url查询的结果
        :param url: URL
        :return:
        """
        self.send_keys(R.menu.url,url)
        sleep(2)
        self.click(R.menu.search)
        sleep(5)

    def get_result_by_menuName(self,menuName):
        """
        获取根据菜单名称查询的结果
        :param menuName: 菜单名称
        :return:
        """
        self.send_keys(R.menu.menu_name,menuName)
        sleep(2)
        self.click(R.menu.search)
        sleep(5)

    def get_result_by_type(self,j):
        """
        获取根据类型查询的结果
        :param j: 第j个选项
        :return:
        """
        # self.click(R.menu.type)
        type_list = self.find_element(R.menu.type)
        type_list.find_element_by_xpath('//*[@id="type"]/option['+str(j)+']').click()
        sleep(2)
        self.click(R.menu.search)
        sleep(5)


    def reset(self,url,menuName):
        """
        重置
        :param url: URL
        :param menuName: 菜单名称
        :return:
        """

        self.send_keys(R.menu.url, url)
        sleep(2)
        self.send_keys(R.menu.menu_name, menuName)
        sleep(2)

        self.click(R.menu.reset)
        sleep(5)

    def get_reset_value(self):
        """
        获取重置后结果
        :return: None
        """
        url = self.find_element(R.menu.url).text
        print(url)
        menuname = self.find_element(R.menu.menu_name).text
        print(menuname)
        if url == '' and menuname == '':
            return None
        else:
            return 'Error'

    def add_menu_cancel(self):
        """
        新增菜单
        :return: None
        """
        self.click(R.menu.add)
        sleep(2)
        self.driver.find_element_by_xpath('/html/body/div[2]/table/tbody/tr[2]/td[2]/div/div[2]/div/div[1]/div[3]').click()
        sleep(2)
        try:
            self.driver.find_element_by_xpath('/html/body/div[4]/table/tbody/tr[2]/td[2]/div/div[2]/div/div[2]/div[3]')
            return "Error"
        except NoSuchElementException:
            # print(u"%s 页面中未能找到 %s 元素" % (self, msg))
            return None

    def new_menu(self, first, second):
        """tms新菜单"""
        all_first_menus = self.find_elements(R.tms_menu.first_menu)
        all_second_menus = self.find_elements(R.tms_menu.second_menu)

        for father in all_first_menus:
            if father.text.strip() == first:
                print('父菜单：' + first)
                father.click()
                sleep(3)
                for son in all_second_menus:
                    if son.text.strip() == second:
                        print('子菜单：' + second)
                        son.click()
                        sleep(3)

    def menu(self,first,second):
        '''鼠标悬停方式进入新菜单'''
        mouse=self.find_element((By.LINK_TEXT,first))
        ActionChains (self.driver).move_to_element (mouse).perform ()
        sleep (1)
        #self.find_element((By.LINK_TEXT,senond)).click()
        self.find_element((By.XPATH,'//dl/dd/a[text()="'+second+'"]')).click()

    def select_list(self,text):
        '''下拉框选择'''
        A=self.find_element((By.XPATH,"//dd[text()='"+text+"']"))
        A.click()








