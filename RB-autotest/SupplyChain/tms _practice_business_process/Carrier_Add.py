#coding=utf-8
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import os
from selenium.common.exceptions import NoSuchElementException
import mysql.connector
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
farther=browser.find_elements_by_css_selector("ul.layui-layout-left>li>a")
son=browser.find_elements_by_css_selector("li.layui-nav-item>dl>dd>a")
first='承运商管理'
second='承运商管理'
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
frame=browser.find_element_by_css_selector("body > div > div.layui-body > div > div > div > div > iframe")
print("切换主界面frame")
browser.switch_to.frame(frame)
print("点击查询")
browser.find_element_by_id("query_btn").click()
print('点击新增')
browser.find_element_by_xpath('/html/body/div/div[2]/div[1]/button[1]').click()
print("切换到新增弹窗frame")
popup_frame=browser.find_element_by_xpath('//*[@id="layui-layer-iframe1"]')
browser.switch_to.frame(popup_frame)
print('输入承运商信息')
browser.find_element_by_name('code').send_keys('1234567')#承运商编码
browser.find_element_by_name('name').send_keys('自动化测试承运商2')#承运商名称
browser.find_element_by_name('carrierPlatformCode').send_keys('autotest')#承运商平台

browser.find_element_by_xpath('//*[@id="address_form"]/div[1]/div/div[4]/div/div/div/input').click()#类型
browser.find_element_by_xpath('//*[@id="address_form"]/div[1]/div/div[4]/div/div/dl/dd[1]').click()

browser.find_element_by_name('contact').send_keys('陈鹏')#联系人
browser.find_element_by_name('email').send_keys('chenpeng@111.com.cn')#邮箱
browser.find_element_by_name('telephone').send_keys('11122233344')#联系电话
browser.find_element_by_name('address').send_keys('光谷E城E5栋')#地址
browser.find_element_by_xpath('//*[@id="address_form"]/div[1]/div/div[9]/div/div/div/input').click()#COD短信
browser.find_element_by_xpath('//*[@id="address_form"]/div[1]/div/div[9]/div/div/dl/dd[1]').click()

browser.find_element_by_name('msgKeyword').send_keys('派件人|派件中|派件员|电话')#关键字
browser.find_element_by_name('remark').send_keys('自动化测试')#备注
browser.find_element_by_xpath('//*[@id="address_form"]/div[1]/div/div[12]/div/div/div/input').click()#业务类型
browser.find_element_by_xpath('//*[@id="address_form"]/div[1]/div/div[12]/div/div/dl/dd[3]').click()

browser.find_element_by_xpath('//*[@id="address_form"]/div[1]/div/div[13]/div/div/div/input').click()#仓库
browser.find_element_by_xpath('//*[@id="address_form"]/div[1]/div/div[13]/div/div/dl/dd[2]').click()

browser.find_element_by_name('codMoneyMin').send_keys(10)
browser.find_element_by_name('codMoneyMax').send_keys(20)



sleep(1)
print('保存')
browser.find_element_by_xpath('//*[@id="address_form"]/div[3]/div/button[1]').click()
sleep(1)
print("切换主界面frame")
browser.switch_to.frame(frame)
print("输入承运商名称点击查询")
browser.find_element_by_name('name').send_keys('自动化测试承运商')#输入承运商名称
browser.find_element_by_id("query_btn").click()
sleep(1)
delete1=browser.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/table/tbody/tr/td[17]/div').text
sleep(1)
print('勾选订单')
browser.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/div[2]/table/tbody/tr[1]/td[2]/div/div').click()
print('点击删除')
browser.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/button[2]').click()
sleep(1)
carrie_code=browser.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/table/tbody/tr/td[5]/div').text
carrie_name=browser.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/table/tbody/tr/td[6]/div').text
delete2=browser.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/table/tbody/tr/td[17]/div').text

print(delete1,delete2)

if delete1 == '否':
    if delete2 == '是':
        print("新增并删除成功，测试通过")
    else:
        print ("新增并删除失败，测试不通过")
elif delete1 == '是':
    if delete2 == '是':
        print('当前承运商已新增并删除，测试通过')
    else:
        print("新增并删除失败，测试不通过")
else :
    print ("新增并删除失败，测试不通过")

assert delete2 == '是'
sleep(1)
browser.quit()
'''用SQL删除新增的承运商'''
#-----------------------------------------------------------------
'''连接数据库查询承运商code'''

mydb = mysql.connector.connect(
                host="10.6.84.20",
                user="tms",
                passwd="d41d8cd98f00b204",
                database="tms",
)
mycursor = mydb.cursor()

query='select name FROM tms_carrier  WHERE CODE=%s'
mycursor.execute(query,(carrie_code,))
myresult = mycursor.fetchall()
b=myresult[0]
name = ','.join(b)
print(name)

delete='DELETE FROM tms_carrier  WHERE CODE=%s'
mycursor.execute(delete,(carrie_code,))
mydb.commit()
print('删除成功')
