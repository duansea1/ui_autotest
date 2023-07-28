'''
# -*- coding: utf-8 -*-
#开发人员:   
#开发日期:   
#文件项目:   
#文件名称:   
 '''
#coding=utf-8
from selenium import webdriver
from time import sleep
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.action_chains import ActionChains


browser = webdriver.Chrome()
browser.maximize_window() #最大化浏览器
url='http://tms2.111.com.cn/home'
print ("进入%s"%(url))#进入TMS
browser.get(url)
print("输入用户名")
browser.find_element_by_name("username").send_keys("chenpeng")
print("输入密码")
browser.find_element_by_name("password").send_keys("Cp,147258")
print("点击登录")
browser.find_element_by_css_selector("#login-from > span").click()
sleep(3)
farther=browser.find_elements_by_css_selector("ul.layui-layout-left>li>a")
son=browser.find_elements_by_css_selector("li.layui-nav-item>dl>dd>a")
first='承运商管理'
second='配送规则管理'
'''菜单方法'''
#browser.implicitly_wait (20)
mouse = browser.find_element_by_link_text ("承运商管理")
ActionChains (browser).move_to_element (mouse).perform ()
sleep(1)
browser.find_element_by_link_text ("配送规则管理").click ()

frame=browser.find_element_by_css_selector("body > div > div.layui-body > div > div > div > div > iframe")
print("切换主界面frame")
browser.switch_to.frame(frame)
print("点击查询")
browser.find_element_by_id("btn-submit").click()
print("选择承运商")
sleep(1)
browser.find_element_by_xpath('//*[@id="layui_form_xx"]/div/div[1]/div[1]/div/div/div/input').click()
sleep(5)
#browser.find_element_by_link_text('自动化测试承运商').click()
a=['自动化测试承运商']
b="//dd[text()='自动化测试承运商']"
a=1
browser.find_element_by_xpath("//dd[text()='%s'%(a)").click()
browser.find_element_by_xpath("//dd[text()='"+a+"']").click()

print(222)
#browser.find_element_by_xpath(b).click()


# caiier=browser.find_elements_by_xpath('//*[@id="layui_form_xx"]/div/div[1]/div[2]/div/div/dl')
#
# for a in caiier:
#     print(a.text,type(a.text))
#     if a.text.strip() == '自动化测试承运商':
#         print(a.text)
#         a.click()
    #if a.text.strip()=='广东EMS':
        # print(a.text)
        # a.click()
# r = browser.find_element_by_id('carrierCode')
# sleep(2)
# print('选择')
# Select(r).select_by_value ('2222222')
sleep(3)
browser.quit()


