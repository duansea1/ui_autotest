#coding=utf-8
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os
from selenium.common.exceptions import NoSuchElementException
import time;
browser = webdriver.Chrome()#("C:\\Program Files (x86)\\Google\Chrome\\Application\\chromedriver.exe") # C:\ProgramFiles(x86)\Google"
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
second='未收货修改收货地址'
for i in farther:
    if i.text.strip() ==first:
        print("点击一级菜单："+first)
        i.click()
        sleep(1)
        for a in son:
            if a.text.strip()==second:
                print("点击二级菜单："+second)
                a.click()
                sleep(1)
# frame=browser.find_element_by_css_selector("iframe")
# frame=browser.find_elements_by_tag_name("iframe")[0]
frame=browser.find_element_by_css_selector("body > div > div.layui-body > div > div > div > div > iframe")
print("切换frame")
browser.switch_to.frame(frame)
do="7032747874"
print("输入DO单号："+do)
browser.find_element_by_id("layui_input_xx").send_keys(do)
print("清空下单时间")
browser.find_element_by_id("handleTimeStart").clear()
browser.find_element_by_id("handleTimeEnd").clear()
print("点击查询")
browser.find_element_by_id("address_query_btn").click()
sleep(1)
browser.find_element_by_xpath('//*[@id="layui_form_xx"]/div/div[12]/div[1]/div[3]/div[2]/table/tbody/tr/td[2]/div/a').click()
sleep(1)
iframe=browser.find_element_by_xpath('//*[@id="layui-layer-iframe1"]')
print("切换到修改弹窗iframe")
browser.switch_to.frame(iframe)
sleep(1)
print('输入新地址：省')
browser.find_element_by_xpath("/html/body/div/div/form/div/div[1]/div/div/div/input").click()
browser.find_element_by_xpath('//*[@id="layui_form_xx"]/div/div[1]/div/div/dl/dd[2]').click()
sleep(1)
print('输入新地址：市')
browser.find_element_by_xpath('//*[@id="layui_form_xx"]/div/div[2]/div/div/div/input').click()
sleep(1)
browser.find_element_by_xpath('//*[@id="layui_form_xx"]/div/div[2]/div/div/dl/dd[2]').click()
sleep(1)
print('输入新地址：区/县')
browser.find_element_by_xpath('//*[@id="layui_form_xx"]/div/div[3]/div/div/div/input').click()

browser.find_element_by_xpath('//*[@id="layui_form_xx"]/div/div[3]/div/div/dl/dd[2]').click()
print('输入新地址：详细地址')
browser.find_element_by_xpath('//*[@id="layui_form_xx"]/div/div[4]/div/input').send_keys("测试地址")

print('输入新地址：联系人')
browser.find_element_by_xpath('//*[@id="layui_form_xx"]/div/div[5]/div/input').send_keys("测试1")

print('输入新地址：联系电话')
browser.find_element_by_xpath('//*[@id="layui_form_xx"]/div/div[6]/div/input').send_keys("13669099006")

print('点击保存')
sleep(2)
browser.find_element_by_xpath('//*[@id="layui_form_xx"]/div/div[7]/div/button').click()
sleep(1)
browser.switch_to_default_content()#切回主页面
browser.switch_to.frame(frame)#切换到frame
print("点击查询")
browser.find_element_by_id("address_query_btn").click()
sleep(2)
old_province=browser.find_element_by_xpath('//*[@id="layui_form_xx"]/div/div[12]/div[1]/div[2]/table/tbody/tr/td[4]/div').text
old_city=browser.find_element_by_xpath('//*[@id="layui_form_xx"]/div/div[12]/div[1]/div[2]/table/tbody/tr/td[5]/div').text
old_country=browser.find_element_by_xpath('//*[@id="layui_form_xx"]/div/div[12]/div[1]/div[2]/table/tbody/tr/td[6]/div').text
old_address=browser.find_element_by_xpath('//*[@id="layui_form_xx"]/div/div[12]/div[1]/div[2]/table/tbody/tr/td[13]/div').text
old_consignee=browser.find_element_by_xpath('//*[@id="layui_form_xx"]/div/div[12]/div[1]/div[2]/table/tbody/tr/td[14]/div').text
old_phone=browser.find_element_by_xpath('//*[@id="layui_form_xx"]/div/div[12]/div[1]/div[2]/table/tbody/tr/td[15]/div').text
print("老地址为："+old_province+old_city+old_country+old_address)
print(old_consignee+"："+old_phone)
sleep(2)
new_province=browser.find_element_by_xpath('//*[@id="layui_form_xx"]/div/div[12]/div[1]/div[2]/table/tbody/tr/td[16]/div').text
new_city=browser.find_element_by_xpath('//*[@id="layui_form_xx"]/div/div[12]/div[1]/div[2]/table/tbody/tr/td[17]/div').text
new_country=browser.find_element_by_xpath('//*[@id="layui_form_xx"]/div/div[12]/div[1]/div[2]/table/tbody/tr/td[18]/div').text
new_address=browser.find_element_by_xpath('//*[@id="layui_form_xx"]/div/div[12]/div[1]/div[2]/table/tbody/tr/td[19]/div').text
new_consignee=browser.find_element_by_xpath('//*[@id="layui_form_xx"]/div/div[12]/div[1]/div[2]/table/tbody/tr/td[20]/div').text
new_phone=browser.find_element_by_xpath('//*[@id="layui_form_xx"]/div/div[12]/div[1]/div[2]/table/tbody/tr/td[21]/div').text
print("新地址为："+new_province+new_city+new_country+new_address)
print(new_consignee+"："+new_phone)
sleep(2)
browser.quit()

