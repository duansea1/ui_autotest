'''
Created on 2018/12/5

@author: liya
'''
from business import BasePage
from time import sleep
from business.manage import resources as R
from selenium.webdriver.support.select import Select


class CMS(BasePage.Base):

    def __int__(self):
        pass

    def cms_chose_tab(self, tab):
        """cms活动
        @:param:tab: 活动管理，创建活动，模板/参数管理"""
        tabs = self.driver.find_elements_by_css_selector('#myTab > li >a')
        for a in tabs:
            if a.text == tab:
                print(a.text)
                a.click()
                break

    def creat_activity(self, name, type, year):
        """创建cms活动"""
        cms_name = self.find_element(R.cms_activity.cms_name)
        cms_name.send_keys(name)  #输入活动名称
        print('活动名称：', name)

        self.find_element(R.cms_activity.cms_begintime).click()  #点击活动开始时间
        #聚焦开始时间控件
        self.driver.switch_to.frame(self.driver.find_element_by_css_selector('body > div:nth-child(23) > iframe'))
        self.find_element(R.cms_activity.time_dpok).click()  #点击开始时间控件的确定按钮
        print('开始时间：今天')
        self.switch_to_latest_windows()
        self.find_element(R.cms_activity.cms_endtime).click()
        #聚焦结束时间控件
        self.driver.switch_to.frame(self.driver.find_element_by_css_selector('body > div:nth-child(23) > iframe'))
        self.find_element(R.cms_activity.time_year).clear
        self.find_element(R.cms_activity.time_year).send_keys(year)  #输入年
        # self.find_element(R.cms_activity.time_month).send_keys(month)  #输入月
        self.find_element(R.cms_activity.time_dpok).click()  #点击确定按钮
        print('结束时间：', year, '年的今天')
        self.switch_to_latest_windows()

        #活动类型
        if type == '1':
            self.click(R.cms_activity.activity_system)
            print('普通活动：系统')
        else:
            self.click(R.cms_activity.activity_manual)
            print('普通活动：手动')

        self.find_element(R.cms_activity.save_btn).click()
        self.click(R.cms_activity.confirm)
        print('创建活动成功')











