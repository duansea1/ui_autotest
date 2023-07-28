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
browser.find_element_by_name("password").send_keys("Cp,147258")
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
second='承运商指派'
for i in farther:
    if i.text.strip() ==first:
        print("点击一级菜单："+first)
        i.click()
        sleep(3)
        for a in son:
            if a.text.strip()==second:
                print("点击二级菜单："+second)
                a.click()
                sleep(3)
frame=browser.find_element_by_css_selector("body > div > div.layui-body > div > div > div > div > iframe")
print("切换主界面frame")
browser.switch_to.frame(frame)
print("点击查询")
browser.find_element_by_id("address_query_btn").click()
do="7032748104"
print("输入DO单号："+do)
browser.find_element_by_id("layui_input_xx").send_keys(do)
print("清空下单时间")
browser.find_element_by_id("handleTimeStart").clear()
browser.find_element_by_id("handleTimeEnd").clear()
browser.find_element_by_id("layui_input_xx").click()
print("点击查询")
browser.find_element_by_id("address_query_btn").click()
sleep(1)
# browser.switch_to_default_content()
# sleep(1)
status=browser.find_element_by_xpath('/html/body/div/div[2]/div[2]/div[1]/div[2]/table/tbody/tr/td[10]/div').text
print("状态为："+status)
carrier=browser.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/table/tbody/tr/td[7]/div').text
print("当前承运商为："+carrier)
print("勾选承运商")
browser.find_element_by_xpath('/html/body/div/div[2]/div[2]/div[1]/div[3]/div[1]/table/thead/tr/th[2]/div/div/i').click()
sleep(1)
print("点击指派")
browser.find_element_by_xpath('/html/body/div/div[2]/div[1]/button[2]').click()
print("切换到弹窗frame")
popup_frame=browser.find_element_by_xpath('//*[@id="layui-layer-iframe1"]')
browser.switch_to.frame(popup_frame)
sleep(1)
browser.find_element_by_xpath('//*[@id="layui_form_xx"]/div/div[1]/div/div/div/input').click()
sleep(1)
jd_langfang=browser.find_element_by_xpath('//*[@id="layui_form_xx"]/div/div[1]/div/div/dl/dd[22]')
yt_yaowang=browser.find_element_by_xpath('//*[@id="layui_form_xx"]/div/div[1]/div/div/dl/dd[3]')
special_carrier=browser.find_element_by_xpath('//*[@id="layui_form_xx"]/div/div[1]/div/div/dl/dd[5]')
sleep(1)
if carrier == jd_langfang.text:
    yt_yaowang.click()
elif carrier == yt_yaowang.text:
    jd_langfang.click()
else:
    special_carrier.click()
sleep(2)
print("点击指派")
browser.find_element_by_xpath('//*[@id="layui_form_xx"]/div/div[2]/div/button').click()
sleep(2)
browser.switch_to_default_content()
sleep(1)
print("切换主界面frame")
browser.switch_to.frame(frame)
status=browser.find_element_by_xpath('/html/body/div/div[2]/div[2]/div[1]/div[2]/table/tbody/tr/td[10]/div').text
print("状态为："+status)
carrier=browser.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/table/tbody/tr/td[7]/div').text
print("新承运商为："+carrier)
sleep(2)
browser.quit()