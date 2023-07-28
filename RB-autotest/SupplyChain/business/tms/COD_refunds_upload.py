'''
# -*- coding: utf-8 -*-
#开发人员:   
#开发日期:   
#文件项目:   
#文件名称:   
 '''
from time import sleep
import os
import openpyxl
import random
import pymysql
from business.tms import BasePage
from selenium.webdriver.common.by import By
from business.tms.Resource import R
from business.tms.Carrier_management import Carrier_management



from business.tms.MenuPage import Menu
from business.tms.login import Login


class Cod_refunds(BasePage.Base):
    def switch_to_iframe1(self) :
        print ('切换到iframe1')
        b = self.find_element (R.tms_menu.iframe1)
        self.driver.switch_to.frame (b)

    def switch_to_iframe2(self) :
        print ('切换到iframe2')
        b = self.find_element (R.tms_menu.iframe2)
        self.driver.switch_to.frame (b)

    def query_order(self, order_status,Do) :
        '''查询订单'''
        self.switch_to_iframe1()
        sleep(1)
        if order_status == '请选择':
            print ('选择【全部】订单')
        else:
            print ('选择【'+order_status+'】订单')

        self.find_element(R.COD_Refunds.rebateStatus_sel).click()
        sleep(1)
        no_upload=(By.XPATH,'//dd[text()="'+order_status+'"]')
        self.find_element(no_upload).click()
        leave_time='2017-04-01 00:00:00'
        print ("输入出库时间",leave_time)
        self.send_keys(R.COD_Refunds.leave_time,leave_time)
        sleep(1)
        print('输入DO:'+Do)
        self.send_keys(R.COD_Refunds.do_input,Do)
        print('点击查询')
        self.find_element(R.COD_Refunds.query_btn).click()
        do=self.find_element(R.COD_Refunds.do_line1).text
        carrier=self.find_element(R.COD_Refunds.carrier_line1).text
        collect_amout=self.find_element(R.COD_Refunds.collect_amout).text
        refunds1=self.find_element(R.COD_Refunds.refunds1).text
        status1=self.find_element(R.COD_Refunds.status1).text
        batch_no=self.find_element(R.COD_Refunds.batch_no).text
        return do,carrier,refunds1,status1,collect_amout,batch_no

    def query_carriercode_by_carriername(self,carrier):
        '''连接数据库查询承运商code'''
        mydb = pymysql.connect (
            host="10.6.84.20",
            user="tms",
            passwd="d41d8cd98f00b204",
            database="tms",
        )
        mycursor = mydb.cursor ()
        query = 'SELECT code from tms_carrier where name=%s'
        mycursor.execute (query, (carrier,))
        myresult = mycursor.fetchall ()
        b = myresult[0]
        carrier_code = ','.join (b)
        sleep (2)
        return carrier_code
    
    def query_file_path(self):
        '''查找文件路径'''
        a_path = (os.path.abspath (os.path.join (os.getcwd (), "../../..")))  # 获取SuppluChain目录
        excel_path = os.path.join (a_path, r"file\tms\cod_refunds.xlsx")  # 拼接出导入文件路径
        exe_path = os.path.join (a_path, r"file\tms\cod_refunds_1.exe %s")  # 拼接出导入文件路径
        return excel_path,exe_path

    def excel_edit(self,do,carrier_code,excel_path):
        wb = openpyxl.load_workbook (r'C:\Users\chenpeng\Desktop\test_file\cod_refunds.xlsx')
        sheet = wb['返款对账']
        i = random.randint (1, 100)
        sheet['C2'] = i  # 修改返款金额
        sheet['B2'] = do  # 修改承运商
        sheet['A2'] = carrier_code  # 修改do
        wb.save (excel_path)
        print ('--------------修改Excel返款金额完成-----------')

    def upload_excel_normal(self,exe_path,excel_path):
        '''上传返款数据'''
        self.find_element(R.COD_Refunds.upload_btn_normal).click()
        # os.system(r'C:\Users\chenpeng\Desktop\test_file\upload.exe')
        os.system (exe_path % excel_path)  # 对excel文件路径参数化执行exe上传文件
        print ('--------------上传返款数据完成----------------')

    def upload_excel_unusual(self,exe_path,excel_path):
        '''上传返款数据'''
        self.find_element(R.COD_Refunds.upload_btn_unusual).click()
        print ('--------------上传返款数据开始----------------')
        # os.system(r'C:\Users\chenpeng\Desktop\test_file\upload.exe')
        os.system (exe_path % excel_path)  # 对excel文件路径参数化执行exe上传文件
        print ('--------------上传返款数据完成----------------')
    
    def Refunds_confirm(self):
        print ('勾选订单')
        self.find_element(R.COD_Refunds.check_box_1).click()
        sleep (1)
        print ('点击返款')
        self.find_element(R.COD_Refunds.refunds_btn).click()
        sleep (1)
        print('返款成功')
        refunds2 = self.find_element(R.COD_Refunds.refunds1).text
        status2 = self.find_element(R.COD_Refunds.status1).text
        collect_amout = self.find_element (R.COD_Refunds.collect_amout).text
        return refunds2,status2,collect_amout

    def Upload_Refunds_firsttime(self,status):
        query_result1 = self.query_order(status,'')
        do = query_result1[0]
        carrier = query_result1[1]
        carrier_code = self.query_carriercode_by_carriername (carrier)
        excel_path = self.query_file_path ()[0]
        exe_path = self.query_file_path ()[1]
        print ('修改Excel返款金额')
        self.excel_edit (do, carrier_code, excel_path)
        print ('点击上传返款数据')
        self.upload_excel_normal (exe_path, excel_path)
        return do

    def refunds_onekey(self):
        '''一键返款'''
        print('点击一键返款')
        self.find_element(R.COD_Refunds.refunds_onekey_btn).click()

        self.driver.switch_to.default_content ()
        frame=self.find_element(R.COD_Refunds.frame)
        self.driver.switch_to.frame(frame)

        warning=self.find_element(R.COD_Refunds.batchno_tips).text
        print(warning)
        self.find_element(R.COD_Refunds.batchno_tips_btn).click()
        sleep(1)
        batch_no=self.find_element(R.COD_Refunds.batch_no).text
        print ('输入批次号:'+batch_no)
        self.send_keys(R.COD_Refunds.batch_no_input,batch_no)
        print('点击查询')
        self.find_element(R.COD_Refunds.query_btn).click()
        sleep (1)
        print('点击一键返款')
        self.find_element(R.COD_Refunds.refunds_onekey_btn).click()
        sleep (1)

        self.driver.switch_to.default_content ()
        self.driver.switch_to.frame (frame)

        warning2 = self.find_element (R.COD_Refunds.batchno_tips).text
        print(warning2)
        print ('点击确定')
        self.find_element(R.COD_Refunds.batchno_tips_btn).click()
        print('一键返款成功')




