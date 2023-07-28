'''
# -*- coding: utf-8 -*-
#开发人员:   chenpeng
#开发日期:   2019-04-16 16:48:01
#文件项目:   TMS
#文件名称:   承运商管理
 '''

from business.tms import BasePage
from business.tms.Resource import R
from time import sleep
from business.tms.TMS_mysql import TMS_mysql
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.by import By
import os

class Carrier_management(BasePage.Base):

    class switch_frame(BasePage.Base):
        '''切换frame'''
        def switch_to_iframe1(self):
            print ('切换到iframe1')
            b = self.find_element (R.tms_menu.iframe1)
            self.driver.switch_to.frame (b)

        def switch_to_iframe2(self) :
            print ('切换到iframe2')
            b = self.find_element (R.tms_menu.iframe2)
            self.driver.switch_to.frame (b)

    '''承运商管理'''
    class carrier_platform_management(BasePage.Base):
        '''承运商平台管理'''
        def add(self,code,name,type,url,key_word,no_word):
            #self.driver.switch_to.frame (R.tms_menu.frame)  #切换到页面frame
            #sleep(1)
            iframe = self.find_element (R.DO_management.frame_imput)
            print ('切换至页面详情iframe')
            self.driver.switch_to.frame (iframe)
            sleep(1)
            self.click(R.Carrier_platform_manage.add_btn)   #点击新增
            add_frame=self.find_element(R.Carrier_platform_manage.add_frame)
            print('切换到新增frame')
            self.driver.switch_to.frame(add_frame) #切换到新增frame
            print('输入承运商平台信息：',code,name,type,url,key_word,no_word)
            self.send_keys(R.Carrier_platform_manage.code,code)     #编码
            self.send_keys(R.Carrier_platform_manage.name,name)     #名称
            self.click(R.Carrier_platform_manage.type)              #类型
            sleep(1)
            self.click(R.Carrier_platform_manage.kyd,type)          #配送类型
            self.send_keys(R.Carrier_platform_manage.url,url)       #请求URL
            self.send_keys(R.Carrier_platform_manage.key_word,key_word) #签收关键字
            self.send_keys(R.Carrier_platform_manage.no_word,no_word)   #排除关键字
            self.click(R.Carrier_platform_manage.save_btn)              #保存
            sleep(1)
            # assert '插入失败' in self.driver.page_source,print('保存成功')
            # print('保存失败，编码重复')


        def query(self,code):
            iframe = self.find_element (R.DO_management.frame_imput)
            print ('切换至页面详情iframe')
            self.driver.switch_to.frame (iframe)
            self.send_keys(R.Carrier_platform_manage.code,code)
            print ('查询新增的承运商')
            self.click(R.Carrier_platform_manage.query_btn)
            sleep(1)
            # result=self.find_element(R.Carrier_platform_manage.first_code).text
            # assert code==result,print('查询结果错误')
            # print('保存成功，查询结果为：'+result+'，正确')

        def delete(self,code):
            self.query(code)
            self.click(R.Carrier_platform_manage.choice_box)
            self.click(R.Carrier_platform_manage.delete_btn)
            # sleep(1)
            # assert '修改成功' in self.driver.page_source,print('删除失败')
            # print('删除成功')

        def edit(self,code):
            # self.query(code)
            # sleep(1)
            status_first=self.find_element(R.Carrier_platform_manage.first_status).text
            self.click(R.Carrier_platform_manage.edit)
            sleep(1)
            iframe=self.find_element(R.Carrier_platform_manage.add_frame)
            print('切换到编辑frame')
            self.driver.switch_to.frame(iframe) #切换到编辑frame
            # print('当前状态：'+status_first)
            self.click(R.Carrier_platform_manage.status)
            sleep(1)
            if status_first == '已删除' :
                self.click(R.Carrier_platform_manage.qy)
                print('已更改为启用')
            else:
                self.click (R.Carrier_platform_manage.sc)
                print('已更改为删除')

            self.click(R.Carrier_platform_manage.save_btn)
            # print('保存成功')
            sleep(1)
            iframe = self.find_element (R.DO_management.frame_imput)
            print ('切换至页面详情iframe')
            self.driver.switch_to.frame (iframe)
            sleep(1)
            # status_end=self.find_element(R.Carrier_platform_manage.first_status).text
            # assert status_first != status_end,print('编辑失败')
            # print('编辑成功')

        def mysql_delete(self,sql,parameter):
            TMS_mysql.sql_excute(sql,parameter)
            print('删除成功')

    class freight_free_setup(BasePage.Base):
        '''免邮接口设置'''
        def add(self,id,free,notfree):

            iframe = self.find_element (R.DO_management.frame_imput)
            self.driver.switch_to.frame (iframe)
            print ('切换iframe1')
            sleep(1)
            print('点击新增')
            self.click(R.mysz.add_btn)
            iframe=self.find_element(R.Carrier_platform_manage.add_frame)
            self.driver.switch_to.frame(iframe)
            print ('切换iframe2')
            sleep(1)
            print('输入免邮规则信息')
            self.click(R.mysz.sheng)
            self.click(R.mysz.BJ)
            self.click(R.mysz.shi)
            self.click(R.mysz.bjshi)
            self.click(R.mysz.plat)
            self.click(R.mysz.yc)
            self.send_keys(R.mysz.business_man,id)
            self.send_keys(R.mysz.free,free)
            self.send_keys(R.mysz.freight,notfree)
            print('点击保存')
            self.click(R.mysz.save_btn)

        def query(self,id):
            print('切换iframe1')
            iframe=self.find_element(R.mysz.frame)
            sleep(1)
            self.driver.switch_to.frame(iframe)
            print('查询新增数据')
            self.send_keys(R.mysz.business_man,id)
            self.click(R.mysz.query_btn)

        def edit(self,free,notfree):
            print('点击编辑')
            self.click(R.mysz.edit)
            print ('切换iframe2')
            iframe2=self.find_element(R.Carrier_platform_manage.add_frame)
            sleep(1)
            self.driver.switch_to.frame(iframe2)
            print('输入编辑信息:free='+free+' notfree='+notfree)
            self.send_keys(R.mysz.free,free)
            self.send_keys(R.mysz.freight,notfree)
            print('点击保存')
            self.click(R.mysz.save_btn)

        def onoff(self):
            print('点击启/停用')
            self.click(R.mysz.switch)
            alert=self.find_element(R.mysz.tips).text
            print(alert)
            print('点击确认')
            self.click(R.mysz.confirm_btn)

    class  Delivery_rules_manage(BasePage.Base):

        def add(self,warehouse,carrier,orderSource,isCollect,province,
                city,county,town,deliveryTime,minAccessWeight,maxAccessWeight):
            '''新增配送规则'''
            print('切换到iframe1')
            a=self.find_element(R.tms_menu.iframe1)
            self.driver.switch_to.frame(a)
            print('点击新增')
            self.click(R.Psgz.add_btn)
            sleep(1)
            print('切换到iframe2')
            b=self.find_element(R.tms_menu.iframe2)
            self.driver.switch_to.frame(b)
            print('输入配送规则信息')
            self.click(R.Psgz.warehouse)
            self.find_element((By.XPATH,"//dd[text()='"+warehouse+"']")).click()
            #self.click(By.XPATH,"//dd[text()='广州药业仓库（新）']")
            #self.click(R.Psgz.warehouse_value)

            self.click(R.Psgz.carrier2)
            self.find_element((By.XPATH,"//dd[text()='"+carrier+"']")).click()

            self.click(R.Psgz.orderSource)
            self.find_element((By.XPATH,"//dd[text()='"+orderSource+"']")).click()

            self.click(R.Psgz.isCollect)
            self.find_element((By.XPATH,"//dd[text()='"+isCollect+"']")).click()

            self.click(R.Psgz.province)
            self.find_element((By.XPATH,"//dd[text()='"+province+"']")).click()

            self.click(R.Psgz.city)
            self.find_element((By.XPATH,"//dd[text()='"+city+"']")).click()

            self.click(R.Psgz.county)
            self.find_element((By.XPATH,"//dd[text()='"+county+"']")).click()

            self.click(R.Psgz.town)
            self.find_element((By.XPATH,"//dd[text()='"+town+"']")).click()

            self.send_keys(R.Psgz.deliveryTime,deliveryTime)
            self.send_keys(R.Psgz.minAccessWeight,minAccessWeight)
            self.send_keys(R.Psgz.maxAccessWeight,maxAccessWeight)
            self.click(R.Psgz.havePriority_)
            print('点击保存')
            self.click(R.Psgz.save_btn)

        def query(self,warehouse,carriername,province,city,country,town):
            '''查询配送规则'''
            print('切换到iframe1')
            a=self.find_element(R.tms_menu.iframe1)
            self.driver.switch_to.frame(a)
            print('选择查询条件')
            sleep(1)
            self.click(R.Psgz.warehouse1)

            self.find_element((By.XPATH,"//dd[text()='"+warehouse+"']")).click()

            self.click(R.Psgz.carrier1)
            self.find_element((By.XPATH,"//dd[text()='"+carriername+"']")).click()

            self.click(R.Psgz.province1)
            self.find_element((By.XPATH,"//dd[text()='"+province+"']")).click()

            self.click(R.Psgz.city1)
            self.find_element((By.XPATH,"//dd[text()='"+city+"']")).click()

            self.click(R.Psgz.county1)
            self.find_element((By.XPATH,"//dd[text()='"+country+"']")).click()

            self.click(R.Psgz.town1)
            self.find_element((By.XPATH,"//dd[text()='"+town+"']")).click()

            print('点击查询')
            self.click(R.Psgz.query_btn)
            print('查询成功')

        def delete(self):
            '''删除配送规则'''
            print('点击删除')
            self.click(R.Psgz.delete)
            print('点击确认')
            self.click(R.Psgz.confirm_btn)
            print('删除成功')

        def edit(self,deliveryTime,minAccessWeight,maxAccessWeight):
            '''编辑配送规则'''
            print('点击编辑')
            self.click(R.Psgz.edit)
            sleep(1)
            print('切换到iframe2')
            b=self.find_element(R.tms_menu.iframe2)
            self.driver.switch_to.frame(b)
            print('输入编辑信息')
            self.send_keys(R.Psgz.deliveryTime,deliveryTime)
            self.send_keys(R.Psgz.minAccessWeight,minAccessWeight)
            self.send_keys(R.Psgz.maxAccessWeight,maxAccessWeight)
            self.click(R.Psgz.havePriority_)
            print('点击保存')
            self.click(R.Psgz.save_btn)

        def onoff(self):
            '''配送规则启用/停用'''
            print('点击启用/停用')
            self.click(R.Psgz.switch)

    class freight_templates_manage(switch_frame,BasePage.Base):
        '''运费模板管理'''
        def add(self,warehouse,carrier,
                firstweight,firstFee,secondWeight,secondFee,discount,insuranceRate,minInsurance,paymentFeeRate,paymentFee,
                firstweight1, firstFee1, secondWeight1, secondFee1, discount1,insuranceRate1,minInsurance1, paymentFeeRate1, paymentFee1):
            self.switch_to_iframe1()
            print('点击新增')
            self.click(R.Yfmd.add_btn)
            self.switch_to_iframe2()
            print('输入全国运费模板信息')
            self.click(R.Yfmd.warehouse2)
            self.find_element((By.XPATH,"//dd[text()='"+warehouse+"']")).click()

            self.click(R.Yfmd.carrier2)
            self.find_element ((By.XPATH, "//dd[text()='" + carrier + "']")).click()

            self.send_keys(R.Yfmd.firstweight,firstweight)
            self.send_keys(R.Yfmd.firstFee,firstFee)
            self.send_keys (R.Yfmd.secondWeight, secondWeight)
            self.send_keys (R.Yfmd.secondFee, secondFee)
            self.send_keys (R.Yfmd.discount, discount)
            self.send_keys (R.Yfmd.insuranceRate, insuranceRate)
            self.send_keys (R.Yfmd.minInsurance, minInsurance)
            self.send_keys (R.Yfmd.paymentFeeRate, paymentFeeRate)
            self.send_keys (R.Yfmd.paymentFee, paymentFee)

            print('添加一行')
            self.click(R.Yfmd.addrow_btn)
            print('输入区域运费模板信息')
            self.click(R.Yfmd.Area)
            self.click(R.Yfmd.area1)
            self.click(R.Yfmd.area2)
            self.click(R.Yfmd.area3)

            self.send_keys(R.Yfmd.firstweight2,firstweight1)
            self.send_keys(R.Yfmd.firstFee2,firstFee1)
            self.send_keys (R.Yfmd.secondWeight2, secondWeight1)
            self.send_keys (R.Yfmd.secondFee2, secondFee1)
            self.send_keys (R.Yfmd.discount2, discount1)
            self.send_keys (R.Yfmd.insuranceRate2, insuranceRate1)
            self.send_keys (R.Yfmd.minInsurance2, minInsurance1)
            self.send_keys (R.Yfmd.paymentFeeRate2, paymentFeeRate1)
            self.send_keys (R.Yfmd.paymentFee2, paymentFee1)

            print('提交')
            self.click(R.Yfmd.submit_btn)

        def query(self,warehouse,carrier):
            self.switch_to_iframe1()
            print('输入查询条件')
            self.click(R.Yfmd.warehouse1)
            self.find_element((By.XPATH,'//dd[text()="'+warehouse+'"]')).click()

            self.click(R.Yfmd.carrier1)
            self.find_element((By.XPATH,'//dd[text()="'+carrier+'"]')).click()
            sleep(1)
            print('点击查询')
            self.click(R.Yfmd.query_btn)

        def edit(self,firstweight1, firstFee1, secondWeight1, secondFee1, discount1,insuranceRate1,minInsurance1, paymentFeeRate1, paymentFee1):
            print('点击编辑')
            self.click(R.Yfmd.edit_btn)

            self.switch_to_iframe2()
            print ('输入区域运费模板信息')
            self.click (R.Yfmd.Area)
            self.click (R.Yfmd.area4)
            self.click (R.Yfmd.area5)
            self.click (R.Yfmd.area6)

            self.send_keys (R.Yfmd.firstweight2, firstweight1)
            self.send_keys (R.Yfmd.firstFee2, firstFee1)
            self.send_keys (R.Yfmd.secondWeight2, secondWeight1)
            self.send_keys (R.Yfmd.secondFee2, secondFee1)
            self.send_keys (R.Yfmd.discount2, discount1)
            self.send_keys (R.Yfmd.insuranceRate2, insuranceRate1)
            self.send_keys (R.Yfmd.minInsurance2, minInsurance1)
            self.send_keys (R.Yfmd.paymentFeeRate2, paymentFeeRate1)
            self.send_keys (R.Yfmd.paymentFee2, paymentFee1)

            print('提交')
            self.click(R.Yfmd.submit_btn)
        def delete(self):

            print('点击编辑')
            self.click(R.Yfmd.edit_btn)
            self.switch_to_iframe2()
            print('点击删除')
            self.click(R.Yfmd.delete_btn)
            print('点击提交')
            self.click(R.Yfmd.submit_btn)



        def sql_delete(self,sql,parameter):
             TMS_mysql.sql_excute(sql,parameter)
             print('删除成功')


    class delivery_time_manage(switch_frame,BasePage.Base):
        '''配送时效管理'''
        def upload(self):
            '''导入配送规则'''
            self.switch_to_iframe1()
            print('点击导入')
            self.click(R.delivery_time_template.upload_btn)
            sleep(2)
            print('导入时效规则')
            a_path=(os.path.abspath(os.path.join(os.getcwd(), "../../.."))) #获取SuppluChain目录
            excel_path=os.path.join(a_path,r"file\tms\delivery_time_template.xls") #拼接出导入文件路径
            exe_path=os.path.join(a_path,r"file\tms\delivery_time_template_1.exe %s") #拼接出导入文件路径
            os.system(exe_path % excel_path)  #对excel文件路径参数化执行exe上传文件
            #os.system(r"D:\9\test-autotest\SupplyChain\file\tms\delivery_time_template_1.exe %s" % excel_path)  #绝对路径也可以实现
            print("完成导入")
            sleep(2)

        def query(self,carrier):
            self.switch_to_iframe1()
            sleep(1)
            print('输入承运商：'+carrier)
            self.click(R.delivery_time_template.carrier)
            self.find_element((By.XPATH,'//dd[text()="'+carrier+'"]')).click()
            print('点击查询')
            self.click(R.delivery_time_template.query_btn)

        def delete(self):
            print('选择数据')
            self.click(R.delivery_time_template.check_box_all)
            print('点击删除')
            self.click(R.delivery_time_template.delete_btn)
            print('点击确认')
            self.click(R.Psgz.confirm_btn)

        def edit(self,carrier,deliver_time):
            print('点击修改')
            self.click(R.delivery_time_template.edit_btn)
            self.switch_to_iframe2()
            print('输入修改内容')
            self.click(R.delivery_time_template.delivery_time)

            self.find_element((By.XPATH,'//dd[text()="'+deliver_time+'"]')).click()

            print('点击保存')
            self.click(R.delivery_time_template.save_btn)

    class carrier_account_manage(switch_frame,BasePage.Base):
        '''配送商账号管理'''

        def add(self,code,type,cardnumber,account,password,url):
            self.switch_to_iframe1()
            print("点击新增")
            self.click(R.carrier_account_manage.add_btn)
            sleep(1)
            self.switch_to_iframe2()
            print('输入配送商账户信息')
            self.send_keys(R.carrier_account_manage.carrie_code,code)
            self.send_keys(R.carrier_account_manage.carrier_type,type)
            self.send_keys(R.carrier_account_manage.carrier_cardnumber,cardnumber)
            self.send_keys(R.carrier_account_manage.carrier_account,account)
            self.send_keys(R.carrier_account_manage.carrier_account_pwd,password)
            self.send_keys(R.carrier_account_manage.carrier_requesturl,url)
            print('点击保存')
            self.click(R.carrier_account_manage.save_btn)


        def query(self,type):
            self.switch_to_iframe1()
            print('输入承运商类型')
            self.send_keys(R.carrier_account_manage.carrier_type,type)
            print('点击查询')
            self.click(R.carrier_account_manage.query_btn)

        def edit(self,cardnumber):
            print('点击编辑')
            self.click(R.carrier_account_manage.edit_btn)
            sleep(1)
            self.switch_to_iframe2()
            print('修改承运商账户信息')
            self.send_keys(R.carrier_account_manage.carrier_cardnumber,cardnumber)
            print('点击保存')
            self.click(R.carrier_account_manage.save_btn)

        def delete(self):
            print('选择数据')
            self.click(R.carrier_account_manage.check_box)
            print('点击删除')
            self.click(R.carrier_account_manage.del_but)
            print('点击确认')
            self.click(R.Psgz.confirm_btn)

        def sql_del(self,sql,parameter):
            TMS_mysql.sql_excute(sql,parameter)
            print('承运商账户物理删除成功')

    class Warehouse_standard_freight_allocation(switch_frame,BasePage.Base):
        '''仓库标准运费配置'''

        def add(self,warehouse,fee_percent,fee_standard1,fee_standard2):
            self.switch_to_iframe1()
            print('点击新增')
            self.click(R.Ckyf.add_btn)
            sleep(1)
            self.switch_to_iframe2()
            self.click(R.Ckyf.warehouse_frame2)
            self.find_element((By.XPATH,"//dd[text()='"+warehouse+"']")).click()

            self.send_keys(R.Ckyf.fee_percent,fee_percent)

            self.click(R.Ckyf.area_sel)
            self.click(R.Ckyf.area1)
            self.click(R.Ckyf.area2)
            self.click(R.Ckyf.area3)

            self.send_keys(R.Ckyf.standard_fee1,fee_standard1)
            print('添加一行')
            self.click(R.Ckyf.addrow_btn)
            self.click(R.Ckyf.area_sel2)
            self.click(R.Ckyf.area4)
            self.click(R.Ckyf.area5)
            self.click(R.Ckyf.area6)

            self.send_keys(R.Ckyf.standard_fee2,fee_standard2)
            print('点击保存')
            self.click(R.Ckyf.save_btn)
            sleep(1)

        def query(self,warehouse):
            self.switch_to_iframe1()
            sleep(1)
            print('选择仓库')
            self.click(R.Ckyf.warehouse_frame1)

            self.find_element((By.XPATH,'//dd[text()="'+warehouse+'"]')).click()
            print('点击查询')
            self.click(R.Ckyf.query_btn)

        def edit(self,fee_percent,fee_standard):
            print('点击编辑')
            self.click(R.Ckyf.edit_btn)
            sleep(1)
            self.switch_to_iframe2()
            print('输入编辑内容')
            self.send_keys(R.Ckyf.fee_percent,fee_percent)

            self.click(R.Ckyf.area_sel)
            self.click(R.Ckyf.area1)

            self.send_keys(R.Ckyf.standard_fee1,fee_standard)
            print('点击提交')
            self.click(R.Ckyf.save_btn)
            sleep(1)

        def delete(self):
            print ('点击编辑')
            self.click (R.Ckyf.edit_btn)
            sleep (1)
            self.switch_to_iframe2 ()
            print('点击删除')
            self.click(R.Ckyf.delete_btn)
            print('点击提交')
            self.click(R.Ckyf.save_btn)
            sleep(1)

        def sql_del(self,sql,parameter):
             TMS_mysql.sql_excute(sql,parameter)
             print('删除成功')

























