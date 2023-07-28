#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/23
# @Author  : zhangqinqin
from selenium.common.exceptions import NoSuchElementException

from business.tms import BasePage
from business.tms.Resource import R
from time import sleep

class Role(BasePage.Base):
    """rolepage 对象"""

    def get_result_by_roleName(self,roleName):
        """
        获取根据角色名称查询的结果
        :param roleName: 角色名称
        :return:
        """
        self.send_keys(R.role.role_name,roleName)
        sleep(2)
        self.click(R.role.search)
        sleep(5)

    def get_result_by_description(self,description):
        """
        获取根据描述的结果
        :param description: 描述
        :return:
        """
        self.send_keys(R.role.description, description)
        sleep(2)
        self.click(R.role.search)
        sleep(5)


    def reset(self,roleName,description):
        """
        重置
        :param roleName: 角色名称
        :param description: 描述
        :return:
        """
        self.send_keys(R.role.role_name, roleName)
        sleep(2)
        self.send_keys(R.role.description, description)
        sleep(2)
        self.click(R.role.reset)
        sleep(5)

    def get_reset_value(self):
        """
        获取重置后结果
        :return: None
        """
        role_name = self.find_element(R.role.role_name).text
        print(role_name)
        description = self.find_element(R.role.description).text
        print(description)
        if role_name == '' and description == '':
            return None
        else:
            return 'Error'

    def add_menu_cancel(self):
        """
        新增角色
        :return: None
        """
        self.click(R.role.add)
        sleep(2)
        self.driver.find_element_by_xpath('/html/body/div[2]/table/tbody/tr[2]/td[2]/div/div[2]/div/div[1]/div[3]').click()
        sleep(2)
        try:
            self.driver.find_element_by_xpath('/html/body/div[2]/table/tbody/tr[2]/td[2]/div/div[2]/div/div[2]/div[3]')
            return "Error"
        except NoSuchElementException:
            # print(u"%s 页面中未能找到 %s 元素" % (self, msg))
            return None







