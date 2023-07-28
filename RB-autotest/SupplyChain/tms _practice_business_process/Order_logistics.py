#coding=utf-8
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os
from selenium.common.exceptions import NoSuchElementException
import time;

browser = webdriver.Chrome()
browser.maximize_window() #最大化浏览器
url='http://tms2.111.com.cn/home'
print ("进入%s"%(url))#进入TMS
browser.get(url)
print("输入用户名")
browser.find_element_by_name("username").send_keys("chenpeng")
print("输入密码")
browser.find_element_by_name("password").send_keys("Cp,456789")
print("点击登录")
browser.find_element_by_css_selector("#login-from > span").click()
sleep(3)
title=browser.title
print("页面标题为："+title)
url=browser.current_url
print("当前网址为："+url)
sleep(3)
farther=browser.find_elements_by_css_selector("ul.layui-layout-left>li>a")
son=browser.find_elements_by_css_selector("li.layui-nav-item>dl>dd>a")
sleep(2)
first='订单管理'
second='DO管理（出库报表）'
for i in farther:
    if i.text.strip() ==first:
        print("点击一级菜单："+first)
        i.click()
        sleep(3)
        for a in son:
            if a.text.strip()==second:
                print("点击二级菜单"+second)
                a.click()
                sleep(3)
frame=browser.find_element_by_css_selector("body > div > div.layui-body > div > div > div > div > iframe")
print("切换frame")
browser.switch_to.frame(frame)
# sleep (1)
# print ("输入DO单号：" , 7034541176)
# browser.find_element_by_xpath ("//input[@name='code']").click ()
# sleep (1)
# browser.find_element_by_xpath ("//input[@name='code']").clear ()
# browser.find_element_by_xpath ("//input[@name='code']").send_keys (7034541176)

print("点击查询")
browser.find_element_by_id("address_query_btn").click()
# js="document.getElementsByClassName('layui-table-body layui-table-main').scrollTop=100"
# print("准备右滑")
# browser.execute_script(js)
# print("滑到最右侧")
sleep(5)
target = browser.find_element_by_link_text(u'查看物流')
# #browser.execute_script("arguments[0].scrollIntoView();", target)
target.click()
sleep(3)
browser.switch_to.default_content()
# frame=browser.find_element_by_css_selector("body > div > div.layui-body > div > div > div > div > iframe")
print("切换到父frame")
browser.switch_to.frame(frame)
a=browser.find_element_by_css_selector("#layui-layer-iframe1")
print("切换到物流信息frame")
browser.switch_to.frame(a)
b=browser.find_element_by_xpath("/html/body/div/ul/li/div/h4").text
sleep(2)
c=browser.find_element_by_xpath("/html/body/div/ul/li/div/p").text
print("------物流信息为-------")
print(b+":"+c)
if c.strip() == '':
        print('c is null')
else:
    print("测试通过")

browser.quit()