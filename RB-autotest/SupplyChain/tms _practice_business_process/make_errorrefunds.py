#coding=utf-8
from selenium import webdriver
from time import sleep
import os
import openpyxl
import random
import mysql.connector
'''异常订单通过异常导入功能导入返款数据'''
m=1
while m< 2:
    m+=1
    browser = webdriver.Chrome()
    browser.maximize_window() #最大化浏览器
    url='http://tms2.111.com.cn/home'
    print ("进入%s"%(url))#进入TMS
    browser.get(url)
    # login()
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
    first='费用结算'
    second='COD订单管理'
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
    print("切换frame")
    browser.switch_to.frame(frame)
    sleep(1)
    browser.find_element_by_xpath('//*[@id="ra"]/div[2]/div/div/div/input').click()
    sleep(1)
    # print('选择全部')
    # browser.find_element_by_xpath('//*[@id="ra"]/div[2]/div/div/dl/dd[1]').click()
    print('选择异常订单')
    browser.find_element_by_xpath('//*[@id="ra"]/div[2]/div/div/dl/dd[5]').click()
    sleep(1)
    print("输入出库时间")
    browser.find_element_by_id('leaveDcTimeStart').clear()
    sleep(1)
    browser.find_element_by_id('leaveDcTimeStart').send_keys('2017-04-01 00:00:00')
    browser.find_element_by_id("btn-submit").click()#点击查询
    sleep(2)
    do=browser.find_element_by_xpath('/html/body/div/div/div/div[8]/div[1]/div[2]/table/tbody/tr/td[4]/div').text
    carrier=browser.find_element_by_xpath('/html/body/div/div/div/div[8]/div[1]/div[2]/table/tbody/tr/td[7]/div').text
    #-----------------------------------------------------------------
    '''连接数据库查询承运商code'''
    mydb = mysql.connector.connect(
            host="10.6.84.20",
            user="tms",
            passwd="d41d8cd98f00b204",
            database="tms",
    )
    mycursor = mydb.cursor()
    query='SELECT code from tms_carrier where name=%s'
    mycursor.execute(query,(carrier,))
    myresult = mycursor.fetchall()
    b=myresult[0]
    carrie_code = ','.join(b)
    #----------------------------------------------------------
    refunds1=browser.find_element_by_xpath('/html/body/div[1]/div/div/div[8]/div[1]/div[2]/table/tbody/tr/td[15]/div').text
    status1=browser.find_element_by_xpath('/html/body/div[1]/div/div/div[8]/div[1]/div[2]/table/tbody/tr/td[17]/div').text
    print('当前DO：'+do)
    print('当前承运商CODE：'+carrie_code)
    print('当前返款金额：'+refunds1)
    print('当前返款状态：'+status1)
    sleep(2)
    '''正常导入返款数据'''
    # browser.find_element_by_xpath('//*[@id="uploadExcel"]/button').click()
    '''异常导入'''
    browser.find_element_by_xpath('//*[@id="uploadExExcel"]/button').click()
    sleep(5)
    print('--------------修改Excel返款金额开始-----------')
    wb=openpyxl.load_workbook(r'C:\Users\chenpeng\Desktop\test_file\cod_refunds.xlsx')
    print(wb.sheetnames)
    sheet=wb['返款对账']
    i=random.randint(1,1000)
    sheet['C2'] =i  # 修改返款金额
    sheet['B2'] =do  # 修改承运商
    sheet['A2'] =carrie_code  # 修改do
    wb.save(r'C:\Users\chenpeng\Desktop\test_file\cod_refunds.xlsx')
    print('--------------修改Excel返款金额完成-----------')
    sleep(1)
    print('--------------上传返款数据开始----------------')
    os.system(r'C:\Users\chenpeng\Desktop\test_file\upload.exe')
    print('--------------上传返款数据完成----------------')
    sleep (1)
    print(m)
    browser.quit()