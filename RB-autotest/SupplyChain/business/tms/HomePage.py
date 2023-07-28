#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/13
# @Author  : zhangqinqin

from business.tms import BasePage
from business.tms.Resource import R
from time import sleep
from business.manage.manage_home import ManageSystem

from public import files


class Home(BasePage.Base):
    """homepage 对象"""


    def login(self):
        """
        登录
        :param username:
        :param password:
        :return:
        """
        name = files.get_system_value('TMS-account', 'username')
        pword = files.get_system_value('TMS-account', 'password')
        # print(name)
        # print(pword)
        self.send_keys(R.Login.front_user_name, name)
        # print('The username is:%s' % name)
        self.send_keys(R.Login.front_password, pword)
        self.click(R.Login.front_login_button)
        sleep(3)

    @staticmethod
    def open_login_page(selenium, url="http://10.6.80.100:8080/admin/login"):
        """
        打开登录页面，静态方法
        :param selenium:
        :param url:
        :return:
        """
        selenium.get(url)

    @staticmethod
    def get_page_title(selenium):
        """
        获取页面标题
        :param selenium:
        :return:
        """
        print('The page title is:%s' % selenium.title)
        return selenium.title

    def go_menu_page(self):
        """
        获取菜单管理iframe
        :param selenium:
        :return:
        """
        self.click(R.menu.menu_page_link)
        self.driver.switch_to_frame(0)  # 切换到新的iframe
        sleep(3)

    def go_role_page(self):
        """
        获取角色管理iframe
        :param selenium:
        :return:
        """
        self.click(R.role.role_page_link)
        self.driver.switch_to_frame(0)  # 切换到新的iframe
        sleep(3)

    def go_user_page(self):
        """
        获取角色管理iframe
        :param selenium:
        :return:
        """
        self.click(R.user.user_page_link)
        self.driver.switch_to_frame(0)  # 切换到新的iframe
        sleep(3)

    def go_data_page(self):
        """
        获取数据字典iframe
        :param selenium:
        :return:
        """
        self.click(R.data.data_page_link)
        self.driver.switch_to_frame(0)  # 切换到新的iframe
        sleep(3)

    def go_job_page(self):
        """
        获取定时任务iframe
        :param selenium:
        :return:
        """
        self.click(R.job.job_page_link)
        self.driver.switch_to_frame(0)  # 切换到新的iframe
        sleep(3)

    def go_to_tms_new_system(self):
        """进入tms系统页面"""
        url = R.tms_menu.menu_link
        print('进入TMS配送管理系统')
        self.driver.get(url)
        sleep(3)


