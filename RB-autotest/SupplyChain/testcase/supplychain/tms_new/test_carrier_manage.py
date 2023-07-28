'''
# -*- coding: utf-8 -*-
#开发人员:   
#开发日期:   
#文件项目:   
#文件名称:   
 '''
import pymysql
from business.tms.MenuPage import Menu
from business.tms.login import Login
from time import sleep
import pytest

@pytest.mark.Carrier_manage
def test_View_Logistics(selenium):
    tms = Login (selenium)
    tms.tms_login ()
    m = Menu (selenium)
    m.menu ('订单管理', 'DO管理')
    frame = selenium.find_element_by_css_selector ("body > div > div.layui-body > div > div > div > div > iframe")
    print ("切换frame")
    selenium.switch_to.frame (frame)
    print ("点击查询")
    selenium.find_element_by_id ("address_query_btn").click ()
    sleep (1)
    target = selenium.find_element_by_link_text (u'查看物流')
    target.click ()
    sleep (3)
    selenium.switch_to.default_content ()
    print ("切换到父frame")
    selenium.switch_to.frame (frame)
    a = selenium.find_element_by_css_selector ("#layui-layer-iframe1")
    print ("切换到物流信息frame")
    selenium.switch_to.frame (a)
    b = selenium.find_element_by_xpath ("/html/body/div/ul/li/div/h4").text
    sleep (2)
    c = selenium.find_element_by_xpath ("/html/body/div/ul/li/div/p").text
    print ("------最新的物流信息为-------")
    print (b + ":" + c)
    assert c.strip () != ''
    print ("物流信息正常")

@pytest.mark.Carrier_manage
def test_carrier_add(selenium):
    tms = Login (selenium)
    tms.tms_login ()
    m = Menu (selenium)
    m.menu ('承运商管理', '承运商管理')
    frame = selenium.find_element_by_css_selector ("body > div > div.layui-body > div > div > div > div > iframe")
    print ("切换主界面frame")
    selenium.switch_to.frame (frame)
    print ("点击查询")
    selenium.find_element_by_id ("query_btn").click ()
    print ('点击新增')
    selenium.find_element_by_xpath ('/html/body/div/div[2]/div[1]/button[1]').click ()
    print ("切换到新增弹窗frame")
    popup_frame = selenium.find_element_by_xpath ('//*[@id="layui-layer-iframe1"]')
    selenium.switch_to.frame (popup_frame)
    print ('输入承运商信息')
    selenium.find_element_by_name ('code').send_keys ('1234567')  # 承运商编码
    selenium.find_element_by_name ('name').send_keys ('自动化测试承运商2')  # 承运商名称
    selenium.find_element_by_name ('carrierPlatformCode').send_keys ('autotest')  # 承运商平台

    selenium.find_element_by_xpath ('//*[@id="address_form"]/div[1]/div/div[4]/div/div/div/input').click ()  # 类型
    selenium.find_element_by_xpath ('//*[@id="address_form"]/div[1]/div/div[4]/div/div/dl/dd[1]').click ()

    selenium.find_element_by_name ('contact').send_keys ('陈鹏')  # 联系人
    selenium.find_element_by_name ('email').send_keys ('chenpeng@111.com.cn')  # 邮箱
    selenium.find_element_by_name ('telephone').send_keys ('11122233344')  # 联系电话
    selenium.find_element_by_name ('address').send_keys ('光谷E城E5栋')  # 地址
    selenium.find_element_by_xpath ('//*[@id="address_form"]/div[1]/div/div[9]/div/div/div/input').click ()  # COD短信
    selenium.find_element_by_xpath ('//*[@id="address_form"]/div[1]/div/div[9]/div/div/dl/dd[1]').click ()

    selenium.find_element_by_name ('msgKeyword').send_keys ('派件人|派件中|派件员|电话')  # 关键字
    selenium.find_element_by_name ('remark').send_keys ('自动化测试')  # 备注
    selenium.find_element_by_xpath ('//*[@id="address_form"]/div[1]/div/div[12]/div/div/div/input').click ()  # 业务类型
    selenium.find_element_by_xpath ('//*[@id="address_form"]/div[1]/div/div[12]/div/div/dl/dd[3]').click ()

    selenium.find_element_by_xpath ('//*[@id="address_form"]/div[1]/div/div[13]/div/div/div/input').click ()  # 仓库
    selenium.find_element_by_xpath ('//*[@id="address_form"]/div[1]/div/div[13]/div/div/dl/dd[2]').click ()

    selenium.find_element_by_name ('codMoneyMin').send_keys (10)
    selenium.find_element_by_name ('codMoneyMax').send_keys (20)

    sleep (1)
    print ('保存')
    selenium.find_element_by_xpath ('//*[@id="address_form"]/div[3]/div/button[1]').click ()
    sleep (1)
    print ("切换主界面frame")
    selenium.switch_to.frame (frame)
    print ("输入承运商名称点击查询")
    selenium.find_element_by_name ('name').send_keys ('自动化测试承运商')  # 输入承运商名称
    selenium.find_element_by_id ("query_btn").click ()
    sleep (1)
    delete1 = selenium.find_element_by_xpath (
        '/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/table/tbody/tr/td[17]/div').text
    sleep (1)
    print ('勾选订单')
    selenium.find_element_by_xpath (
        '/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/div[2]/table/tbody/tr[1]/td[2]/div/div').click ()
    print ('点击删除')
    selenium.find_element_by_xpath ('/html/body/div[1]/div[2]/div[1]/button[2]').click ()
    sleep (1)
    carrie_code = selenium.find_element_by_xpath (
        '/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/table/tbody/tr/td[5]/div').text
    carrie_name = selenium.find_element_by_xpath (
        '/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/table/tbody/tr/td[6]/div').text
    delete2 = selenium.find_element_by_xpath (
        '/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/table/tbody/tr/td[17]/div').text

    print (delete1, delete2)

    if delete1 == '否' :
        if delete2 == '是' :
            print ("新增并删除成功，测试通过")
        else :
            print ("新增并删除失败，测试不通过")
    elif delete1 == '是' :
        if delete2 == '是' :
            print ('当前承运商已新增并删除，测试通过')
        else :
            print ("新增并删除失败，测试不通过")
    else :
        print ("新增并删除失败，测试不通过")

    assert delete2 == '是'
    sleep (1)
    selenium.quit ()
    '''用SQL删除新增的承运商'''
    # -----------------------------------------------------------------
    '''连接数据库查询承运商code'''

    mydb = pymysql.connect (
        host="10.6.84.20",
        user="tms",
        passwd="d41d8cd98f00b204",
        database="tms",
    )
    mycursor = mydb.cursor ()

    query = 'select name FROM tms_carrier  WHERE CODE=%s'
    mycursor.execute (query, (carrie_code,))
    myresult = mycursor.fetchall ()
    b = myresult[0]
    name = ','.join (b)
    print (name)

    delete = 'DELETE FROM tms_carrier  WHERE CODE=%s'
    mycursor.execute (delete, (carrie_code,))
    mydb.commit ()
    print ('删除成功')

if __name__ == '__main__':
    from public import test
    test.runtc(__file__,  tclevel='Carrier_manage', driver='Chrome')  # Firefox，Chrome
