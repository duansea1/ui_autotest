'''
# -*- coding: utf-8 -*-
#开发人员:   chenpeng
#开发日期:   2019-04-28
#文件项目:   TMS
#文件名称:   称重管理
 '''

from business.tms import BasePage
from business.tms.Resource import R
from time import sleep
from business.tms.TMS_mysql import TMS_mysql
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
import os

class Weighing_management (BasePage.Base):
    '''称重管理'''
    class switch_frame(BasePage.Base):
        '''切换frame'''
        def switch_to_iframe1(self):
            print ('切换到iframe1')
            b = self.find_element (R.tms_menu.iframe1)
            self.driver.switch_to.frame (b)

        def switch_to_iframe2(self) :
            print ('切换到iframe2')
            b = self.find_element (R.tms_menu.iframe2)
            self.driver.switch_to.frame(b)

    class freight_checkout (switch_frame, BasePage.Base) :
        '''运费对账'''

        def do_query(self):
            self.switch_to_iframe1()
            sleep(1)
            print('输入查询条件')
            self.send_keys(R.Yfdz.time_from,' ')
            self.send_keys(R.Yfdz.time_to,' ')
            self.click(R.Yfdz.do_no)
            self.click(R.Yfdz.status_sel)
            self.click(R.Yfdz.status_value)
            print('点击查询')
            self.click(R.Yfdz.query_btn)
            print('获取第一个DO')
            first_do=self.find_element(R.Yfdz.do_line1).text
            actual_freight=self.find_element(R.Yfdz.actualfreight_line1).text
            print('Do为：'+first_do,'实际运费为：'+actual_freight)
        def freight_calculate(self):
            #AcutalWeight=self.find_element(R.Yfdz.actual_weight_line1).text
            #FirstWeight=self.find_element(R.Yfdz.actual_weight_line1).text
            FirstFee= self.find_element(R.Yfdz.FirstFee_line1).text
            #SecondWeight=self.find_element(R.Yfdz.actual_weight_line1).text
            SecondFee=self.find_element(R.Yfdz.SecondFee_line1).text
            Discount=self.find_element(R.Yfdz.discount_line1).text
            Insurance=self.find_element(R.Yfdz.insurance_line1).text
            Charge=self.find_element(R.Yfdz.charges_line1).text
            Acutalfreight=self.find_element(R.Yfdz.actualfreight_line1).text
            calculate_freight=float(FirstFee)+float(SecondFee)-float(Discount)+float(Insurance)+float(Charge)
            #calculate_freight=eval("'FirstFee+SecondFee+(-Discount)+Insurance+Charge'")
            return calculate_freight,Acutalfreight

    class weighing_management(switch_frame,BasePage.Base):
        '''称重管理'''
        def query(self,time_from,state,type):
            self.switch_to_iframe1()
            print('输入查询条件')
            sleep(1)
            self.send_keys(R.Czgl.time_from,time_from)
            self.click(R.Czgl.handoverstate)
            self.find_element((By.XPATH,'//dd[text()="'+state+'"]')).click()

            self.click(R.Czgl.type)
            self.find_element((By.XPATH,'//dd[text()="'+type+'"]')).click()
            print('点击查询')
            self.click(R.Czgl.query_btn)

        def handover_bysel(self,remarks):
            import time
            print('勾选当前页订单')
            #self.click(R.Czgl.checkall_box)
            self.click(R.Czgl.check_box1)
            self.click(R.Czgl.check_box2)

            print('点击交接')
            self.click(R.Czgl.handover_btn)
            self.switch_to_iframe2()
            print(self.find_element(R.Czgl.handover_msg).text)
            print('输入备注信息:'+remarks+ '   自动化测试交接')
            self.send_keys(R.Czgl.remark,remarks+ '   自动化测试交接')
            print('点击确认交接')
            self.click(R.Czgl.confirm_btn)

        def handover_all(self,remarks):
            print('点击交接全部')
            self.click(R.Czgl.handoverall_btn)
            self.switch_to_iframe2 ()
            print (self.find_element (R.Czgl.handover_msg).text)
            print ('输入备注信息:' + remarks + '   自动化测试交接')
            self.send_keys (R.Czgl.remark, remarks + '   自动化测试交接')
            print ('点击确认交接')
            self.click (R.Czgl.confirm_btn)


        def carrier_check(self):
            '''当前页承运商个数'''
            carrier_page1=self.find_elements(R.Czgl.carrier_page1)
            a=[]
            for i in carrier_page1:
                a.append(i.text)
            b=set(a)
            carrier_number=len(b)
            return carrier_number

        def warehouse_check(self):
            '''当前页仓库个数'''
            warehouse_page1=self.find_elements(R.Czgl.warehouse_page1)
            m=[]
            for i in warehouse_page1:
                m.append(i.text)
            n=set(m)
            warehouse_number=len(n)
            return warehouse_number
        def do_handover_state_query(self,state,do):
            self.switch_to_iframe1()
            self.click(R.Czgl.handoverstate)
            self.find_element((By.XPATH,'//dd[text()="'+state+'"]')).click()
            self.send_keys(R.Czgl.do,do)
            self.click(R.Czgl.query_btn)

        def samedata_query(self,carrier,warehouse,time_from,state,type):
            self.switch_to_iframe1()
            print ('输入查询条件')
            sleep (1)
            self.click(R.Czgl.carrier_sel)
            self.find_element((By.XPATH,'//dd/div/span[text()="'+carrier+'"]')).click()
            self.click(R.Czgl.warehouse_sel)
            self.find_element((By.XPATH,'//dd/div/span[text()="'+warehouse+'"]')).click()
            self.send_keys (R.Czgl.time_from, time_from)
            self.click (R.Czgl.handoverstate)
            self.find_element ((By.XPATH, '//dd[text()="' + state + '"]')).click ()
            self.click (R.Czgl.type)
            self.find_element ((By.XPATH, '//dd[text()="' + type + '"]')).click ()
            print ('点击查询')
            self.click (R.Czgl.query_btn)













