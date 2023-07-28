'''
# -*- coding: utf-8 -*-
#开发人员:   chenpeng
#开发日期:   2019-05-13
#文件项目:   TMS
#文件名称:   DO管理
 '''
import pytest
from business.tms.Carrier_management import Carrier_management
from business.tms.MenuPage import Menu
from business.tms.login import Login
from selenium.common.exceptions import NoSuchElementException
from business.tms.Resource import R
from time import sleep
import time

@pytest.mark.DO_manage
def test_do_query(selenium):
    '''查询DO并验证查询结果'''
    tms = Login (selenium)
    tms.tms_login ()
    m = Menu (selenium)
    m.menu ('订单管理', 'DO管理')
    frame = selenium.find_element_by_css_selector ("body > div > div.layui-body > div > div > div > div > iframe")
    print ("切换frame")
    selenium.switch_to.frame (frame)
    print ("点击查询")
    selenium.find_element_by_id ("address_query_btn").click ()
    time_from = "2019-03-01"
    time_to = "2019-03-01"
    do = "7033048299"
    print ("输入出库时间from：" + time_from)
    sleep(1)
    selenium.find_element_by_xpath ("//input[@id='leaveDcTimeStart']").clear ()
    selenium.find_element_by_xpath ("//input[@id='leaveDcTimeStart']").send_keys(time_from)
    sleep (1)
    print ("输入出库时间to：" + time_to)
    selenium.find_element_by_xpath ("//input[@id='leaveDcTimeEnd']").clear ()
    selenium.find_element_by_xpath ("//input[@id='leaveDcTimeEnd']").send_keys (time_to)
    sleep (1)
    print ("输入DO单号：" + do)
    selenium.find_element_by_xpath ("//input[@name='code']").click ()
    sleep (1)
    selenium.find_element_by_xpath ("//input[@name='code']").clear ()
    selenium.find_element_by_xpath ("//input[@name='code']").send_keys (do)
    print ("点击查询")
    selenium.find_element_by_id ("address_query_btn").click ()
    sleep (1)
    # null= selenium.find_element_by_xpath("/html/body/div/div[2]/div/div[1]/div[2]/div").text
    # print(null)
    try :
        assert do == selenium.find_element_by_xpath (
                "/html/body/div/div[2]/div/div[1]/div[2]/table/tbody/tr[1]/td[3]/div").text   # DO单号
        print ("查询结果正确")
    except NoSuchElementException :
        assert "无数据" == selenium.find_element_by_xpath ("/html/body/div/div[2]/div/div[1]/div[2]/div").text
        print ("DO号输入错误，查无数据")

@pytest.mark.DO_manage
def test_assign_error_deal(selenium):

    '''配送异常管理'''
    tms = Login (selenium)
    tms.tms_login ()
    m = Menu (selenium)
    m.menu ('订单管理', '配送异常')
    frame=selenium.find_element_by_css_selector("body > div > div.layui-body > div > div > div > div > iframe")
    print("切换frame")
    selenium.switch_to.frame(frame)
    sleep(1)
    print("清空出库时间")
    selenium.find_element_by_id('leaveDcTimeStart').clear()
    selenium.find_element_by_id('leaveDcTimeEnd').clear()
    print("点击查询")
    selenium.find_element_by_id("btn-submit").click()
    # print('滑至页面底部')
    # js="var q=document.documentElement.scrollTop=100000"
    # selenium.execute_script(js)
    sleep(5)
    print('点击处理')
    selenium.find_element_by_xpath('/html/body/div/div[2]/div[2]/div[1]/div[3]/div[2]/table/tbody/tr[1]/td[2]/div/a[1]').click()
    sleep(1)
    print('切换到弹窗iframe')
    selenium.switch_to.frame(selenium.find_element_by_xpath('//*[@id="layui-layer-iframe1"]'))
    print('选择处理原因')
    selenium.find_element_by_xpath('//*[@id="ex_order_form"]/div/div[6]/div/div/div/div/input').click()
    sleep(1)
    selenium.find_element_by_xpath('//*[@id="ex_order_form"]/div/div[6]/div/div/div/dl/dd[2]').click()
    print('输入备注')
    remarks=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))+'测试'
    selenium.find_element_by_id('exRemark').send_keys(remarks)
    print('保存')
    selenium.find_element_by_xpath('//*[@id="ex_order_form"]/div/div[8]/div/button').click()
    sleep(2)
    selenium.switch_to_default_content()
    sleep(1)
    print("切换主界面frame")
    selenium.switch_to.frame(frame)
    sleep(2)
    print("点击查询")
    selenium.find_element_by_id("btn-submit").click()
    sleep(2)
    print('查看日志详情')
    selenium.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/div[2]/table/tbody/tr[1]/td[2]/div/a[2]').click()
    sleep(2)
    print('切换到日志详情弹窗')
    selenium.switch_to.frame(selenium.find_element_by_xpath('//*[@id="layui-layer-iframe2"]'))
    number=selenium.find_elements_by_xpath('/html/body/div/div/div/div[1]/div[3]/div[2]/table/tbody/tr/td/div')#第一列序号
    reason=selenium.find_elements_by_xpath('/html/body/div/div/div/div[1]/div[2]/table/tbody/tr/td[2]/div')#第2列处理原因
    date=selenium.find_elements_by_xpath('/html/body/div/div/div/div[1]/div[2]/table/tbody/tr/td[3]/div')#第3列处理时间
    operator=selenium.find_elements_by_xpath('/html/body/div/div/div/div[1]/div[2]/table/tbody/tr/td[4]/div')#第4列处理人
    remark=selenium.find_elements_by_xpath('/html/body/div/div/div/div[1]/div[2]/table/tbody/tr/td[5]/div')#第5列备注
    list1=[]
    list2=[]
    list3=[]
    list4=[]
    list5=[]
    for i in number:
        m='第' + i.text + '条日志详情：'
        list1.append(m)
        # print ('第' + i.text + '条日志详情：')
    for a in reason:
        n='处理原因：'+a.text
        list2.append(n)
    for b in date:
        o='处理时间：'+b.text
        list3.append(o)
    for c in operator:
        p='处理人：'+c.text
        list4.append(p)
    for d in remark:
        q="备注："+d.text
        list5.append(q)
    log_list = map(list,zip(list1,list2,list3,list4,list5))
    for j in log_list:
        print(j)
    sleep(2)
    assert list5[0]  == "备注："+ remarks
    print('处理成功')

@pytest.mark.DO_manage
def test_address_change(selenium):
    '''未收货修改收货地址'''
    tms = Login (selenium)
    tms.tms_login ()
    m = Menu (selenium)
    m.menu ('订单管理', '未收货修改收货地址')
    frame = selenium.find_element_by_css_selector ("body > div > div.layui-body > div > div > div > div > iframe")
    print ("切换主界面frame")
    selenium.switch_to.frame (frame)
    do = "7032747874"
    print ("输入DO单号：" + do)
    selenium.find_element_by_id ("layui_input_xx").send_keys (do)
    print ("清空下单时间")
    sleep(1)
    selenium.find_element_by_id ("handleTimeStart").clear ()
    sleep(1)
    selenium.find_element_by_id ("handleTimeEnd").clear ()
    sleep (1)
    print ("点击查询")
    selenium.find_element_by_css_selector ('#address_query_btn').click ()
    sleep (3)
    print('点击修改')
    selenium.find_element_by_xpath (
        '//*[@id="layui_form_xx"]/div/div[12]/div[1]/div[3]/div[2]/table/tbody/tr/td[2]/div/a').click ()
    sleep (1)
    iframe = selenium.find_element_by_xpath ('//*[@id="layui-layer-iframe1"]')
    print ("切换到修改弹窗iframe")
    selenium.switch_to.frame (iframe)
    sleep (1)
    print ('输入新地址：省')
    selenium.find_element_by_xpath ("/html/body/div/div/form/div/div[1]/div/div/div/input").click ()
    selenium.find_element_by_xpath ('//*[@id="layui_form_xx"]/div/div[1]/div/div/dl/dd[2]').click ()
    sleep (1)
    print ('输入新地址：市')
    selenium.find_element_by_xpath ('//*[@id="layui_form_xx"]/div/div[2]/div/div/div/input').click ()
    sleep (1)
    selenium.find_element_by_xpath ('//*[@id="layui_form_xx"]/div/div[2]/div/div/dl/dd[2]').click ()
    sleep (1)
    print ('输入新地址：区/县')
    selenium.find_element_by_xpath ('//*[@id="layui_form_xx"]/div/div[3]/div/div/div/input').click ()

    selenium.find_element_by_xpath ('//*[@id="layui_form_xx"]/div/div[3]/div/div/dl/dd[2]').click ()
    print ('输入新地址：详细地址')
    selenium.find_element_by_xpath ('//*[@id="layui_form_xx"]/div/div[4]/div/input').send_keys ("测试地址")

    print ('输入新地址：联系人')
    selenium.find_element_by_xpath ('//*[@id="layui_form_xx"]/div/div[5]/div/input').send_keys ("测试1")

    print ('输入新地址：联系电话')
    new_phonenumber="13669099006"
    selenium.find_element_by_xpath ('//*[@id="layui_form_xx"]/div/div[6]/div/input').send_keys ("13669099006")

    print ('点击保存')
    sleep (2)
    selenium.find_element_by_xpath ('//*[@id="layui_form_xx"]/div/div[7]/div/button').click ()
    sleep (1)
    selenium.switch_to_default_content ()  # 切回主页面
    selenium.switch_to.frame (frame)  # 切换到frame
    print ("点击查询")
    selenium.find_element_by_id ("address_query_btn").click ()
    sleep (2)
    old_province = selenium.find_element_by_xpath (
        '//*[@id="layui_form_xx"]/div/div[12]/div[1]/div[2]/table/tbody/tr/td[4]/div').text
    old_city = selenium.find_element_by_xpath (
        '//*[@id="layui_form_xx"]/div/div[12]/div[1]/div[2]/table/tbody/tr/td[5]/div').text
    old_country = selenium.find_element_by_xpath (
        '//*[@id="layui_form_xx"]/div/div[12]/div[1]/div[2]/table/tbody/tr/td[6]/div').text
    old_address = selenium.find_element_by_xpath (
        '//*[@id="layui_form_xx"]/div/div[12]/div[1]/div[2]/table/tbody/tr/td[13]/div').text
    old_consignee = selenium.find_element_by_xpath (
        '//*[@id="layui_form_xx"]/div/div[12]/div[1]/div[2]/table/tbody/tr/td[14]/div').text
    old_phone = selenium.find_element_by_xpath (
        '//*[@id="layui_form_xx"]/div/div[12]/div[1]/div[2]/table/tbody/tr/td[15]/div').text
    print ("老地址为：" + old_province + old_city + old_country + old_address)
    print (old_consignee + "：" + old_phone)
    sleep (2)
    new_province = selenium.find_element_by_xpath (
        '//*[@id="layui_form_xx"]/div/div[12]/div[1]/div[2]/table/tbody/tr/td[16]/div').text
    new_city = selenium.find_element_by_xpath (
        '//*[@id="layui_form_xx"]/div/div[12]/div[1]/div[2]/table/tbody/tr/td[17]/div').text
    new_country = selenium.find_element_by_xpath (
        '//*[@id="layui_form_xx"]/div/div[12]/div[1]/div[2]/table/tbody/tr/td[18]/div').text
    new_address = selenium.find_element_by_xpath (
        '//*[@id="layui_form_xx"]/div/div[12]/div[1]/div[2]/table/tbody/tr/td[19]/div').text
    new_consignee = selenium.find_element_by_xpath (
        '//*[@id="layui_form_xx"]/div/div[12]/div[1]/div[2]/table/tbody/tr/td[20]/div').text
    new_phone = selenium.find_element_by_xpath (
        '//*[@id="layui_form_xx"]/div/div[12]/div[1]/div[2]/table/tbody/tr/td[21]/div').text
    print ("新地址为：" + new_province + new_city + new_country + new_address)
    print (new_consignee + "：" + new_phone)
    sleep (2)
    assert new_phonenumber == new_phone
    print ('修改成功')

@pytest.mark.DO_manage
def test_carrier_assign(selenium):
    '''承运商指派'''
    tms = Login (selenium)
    tms.tms_login ()
    m = Menu (selenium)
    m.menu ('订单管理', '承运商指派')
    frame = selenium.find_element_by_css_selector ("body > div > div.layui-body > div > div > div > div > iframe")
    print ("切换主界面frame")
    selenium.switch_to.frame (frame)
    do = "7032748104"
    print ("输入DO单号：" + do)
    selenium.find_element_by_id ("layui_input_xx").send_keys (do)
    print ("清空下单时间")
    sleep(2)
    selenium.find_element_by_id ("handleTimeStart").clear ()
    #selenium.find_element_by_id("handleTimeStart").send_keys('2019-04-13 16:05:00')
    sleep(2)
    selenium.find_element_by_id ("handleTimeEnd").clear ()
    sleep(1)
    selenium.find_element_by_id ("layui_input_xx").click ()
    print ("点击查询")
    sleep(1)
    selenium.find_element_by_id ("address_query_btn").click ()
    sleep (1)
    # selenium.switch_to_default_content()
    # sleep(1)
    status = selenium.find_element_by_xpath ('/html/body/div/div[2]/div[2]/div[1]/div[2]/table/tbody/tr/td[10]/div').text
    print ("状态为：" + status)
    carrier1 = selenium.find_element_by_xpath (
        '/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/table/tbody/tr/td[7]/div').text
    print ("当前承运商为：" + carrier1)
    print ("勾选承运商")
    selenium.find_element_by_xpath (
        '/html/body/div/div[2]/div[2]/div[1]/div[3]/div[1]/table/thead/tr/th[2]/div/div/i').click ()
    sleep (1)
    print ("点击指派")
    selenium.find_element_by_xpath ('/html/body/div/div[2]/div[1]/button[2]').click ()
    print ("切换到弹窗frame")
    popup_frame = selenium.find_element_by_xpath ('//*[@id="layui-layer-iframe1"]')
    selenium.switch_to.frame (popup_frame)
    sleep (1)
    selenium.find_element_by_xpath ('//*[@id="layui_form_xx"]/div/div[1]/div/div/div/input').click ()
    sleep (1)
    jd_langfang = selenium.find_element_by_xpath ('//*[@id="layui_form_xx"]/div/div[1]/div/div/dl/dd[22]')
    yt_yaowang = selenium.find_element_by_xpath ('//*[@id="layui_form_xx"]/div/div[1]/div/div/dl/dd[3]')
    special_carrier = selenium.find_element_by_xpath ('//*[@id="layui_form_xx"]/div/div[1]/div/div/dl/dd[5]')
    sleep (1)
    if carrier1 == jd_langfang.text :
        yt_yaowang.click ()
    elif carrier1 == yt_yaowang.text :
        jd_langfang.click ()
    else :
        special_carrier.click ()
    sleep (2)
    print ("点击指派")
    selenium.find_element_by_xpath ('//*[@id="layui_form_xx"]/div/div[2]/div/button').click ()
    sleep (2)
    selenium.switch_to_default_content ()
    sleep (1)
    print ("切换主界面frame")
    selenium.switch_to.frame (frame)
    sleep(2)
    status = selenium.find_element_by_xpath ('/html/body/div/div[2]/div[2]/div[1]/div[2]/table/tbody/tr/td[10]/div').text
    print ("状态为：" + status)
    carrier2 = selenium.find_element_by_xpath (
        '/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/table/tbody/tr/td[7]/div').text
    print ("新承运商为：" + carrier2)
    assert carrier1 !=carrier2
    print('承运商修改成功')


if __name__ == '__main__':
    from public import test
    test.runtc(__file__,  tclevel='DO_manage', driver='Chrome')  # Firefox，Chrome

