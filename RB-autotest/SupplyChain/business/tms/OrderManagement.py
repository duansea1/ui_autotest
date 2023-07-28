'''
Created on 2019/3/6

@author: liya
'''
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

from business.tms import BasePage
from business.tms.Resource import R
from time import sleep

class OrderManagement(BasePage.Base):
    """订单管理"""

    def query_do_code(self,do_code):
        """do单号查询"""
        iframe = self.find_element(R.order_management.frame)
        # print('点击页面空白页')
        # self.click(R.order_management.frame)
        print('切换iframe')
        self.driver.switch_to.frame(iframe)
        print('输入DO单号：' + do_code)
        self.send_keys(R.order_management.do_code,do_code)
        sleep(1)
        print('清空转DO时间from')
        self.find_element(R.order_management.time_from).clear()
        print('查询')
        self.click(R.order_management.query_btn)
        sleep(1)

    def do_status(self):
        """DO单号的状态"""
        status = self.find_element(R.order_management.status).text
        print('DO状态:' + status)
        return status


    def chose_button(self,i=1):
        """
        导出或指派按钮
        :param i: 0-导出，1-指派
        :return:
        """
        buttons = self.find_elements(R.order_management.button)
        buttons[i].click()

    def assign_carrier(self):
        """指派承运商"""
        carrier = self.find_element(R.order_management.carrier).text
        print('原承运商：%s' % carrier)
        print('勾选do单')
        self.click(R.order_management.chose)
        print('点击指派按钮')
        self.chose_button()
        # self.click()
        print('切换到承运商弹窗')
        iframe = self.driver.find_element_by_xpath('//*[@id="layui-layer-iframe1"]')
        self.driver.switch_to.frame(iframe)
        sleep(1)
        print('点击承运商')
        self.click(R.order_management.chose_carrier)
        sleep(1)
        # self.driver.find_element_by_xpath('//*[@id="layui_form_xx"]/div/div[1]/div/div/div/input').click()
        if carrier == '圆通药网':
            print('选择承运商-广东药网京东')
            self.find_element(R.order_management.yt_yaoguang).click()
        else:
            print('选择承运商-圆通药网')
            # self.driver.find_element_by_xpath('//*[@id="layui_form_xx"]/div/div[1]/div/div/dl/dd[3]').click()
            self.find_element(R.order_management.yt_yaowang).click()
            sleep(1)
        print('指派')
        self.click(R.order_management.assign)
        # self.driver.find_element_by_xpath('//*[@id="layui_form_xx"]/div/div[2]/div/button').click()
        sleep(1)

    def query_do_code_byleavetime(self,do_code,time_from):
        iframe = self.find_element(R.DO_management.frame_imput)
        print('切换至页面详情iframe')
        self.driver.switch_to.frame(iframe)
        #self.driver.switch_to.frame (R.DO_management.frame_imput)
        self.click(R.order_management.query_btn)   #点击查询按钮刷新页面
        sleep(1)
        #time_from = "2018-03-01"
        print("输入出库时间from：" + time_from)
        #self.driver.clear(R.DO_management.leaveWH_from)
        self.send_keys(R.DO_management.leaveWH_from,time_from)
        sleep(1)
        print("输入DO单号：" + do_code)
        #self.driver.clear (R.order_management.do_code)
        self.send_keys(R.DO_management.do_no,do_code)
        print("点击查询")
        self.click(R.order_management.query_btn)
        sleep (2)
        # result1 = self.find_element (R.DO_management.first_do).text  # DO单号
        # assert do_code == result1, "查询结果不正确，测试不通过"
        # # if do_code == result1:
        # print ('查询结果DO为：' + result1 + "，测试通过")

        '''
    # # def do_query_result_assert(self,do_code):
    #     try :
    #         result1=self.find_element(R.DO_management.first_do).text  # DO单号
    #         assert do_code==result1,"查询结果不正确，测试不通过"
    #         # if do_code == result1:
    #         print ('查询结果DO为：'+result1+"，测试通过")
    #         # else :
    #         #     print ("查询结果不正确，测试不通过")
    #         sleep(2)
    #     except TimeoutException :
    #         result2 = self.find_element (R.DO_management.tips_nodata).text  # DO单号
    #         assert '无数据'== result2
    #         print('DO号输入错误，查无数据')
    #         # result2 = self.find_element(R.DO_management.tips_nodata).text  # DO单号
    #         # if "无数据" == result2 :
    #         #     print ("DO号输入错误，查"+result2)
                '''

    def assign_new_carrier_by_warehouse(self,warehouse_id):
        """指派承运商"""
        carrier = self.find_element(R.order_management.carrier).text
        print('原承运商：%s' % carrier)
        print('勾选do单')
        self.click(R.order_management.chose)
        print('点击指派按钮')
        self.chose_button()
        # self.click()
        print('切换到承运商弹窗')
        iframe = self.driver.find_element_by_xpath('//*[@id="layui-layer-iframe1"]')
        self.driver.switch_to.frame(iframe)
        sleep(1)
        print('点击承运商')
        self.click(R.order_management.chose_carrier)
        sleep(1)
        # self.driver.find_element_by_xpath('//*[@id="layui_form_xx"]/div/div[1]/div/div/div/input').click()
        if warehouse_id == '13':#广州仓
            print('选择承运商-广州药城德邦')
            self.find_element(R.order_management.yt_yaoguang).click()
        elif warehouse_id == '30' :#昆山药城
            print ('选择承运商-昆山药城德邦')
            self.find_element (R.order_management.ks_debang).click ()
        elif warehouse_id == '20' :#重庆仓
            print ('选择承运商-重庆药城德邦')
            self.find_element (R.order_management.cq_debang).click ()
        elif warehouse_id == '15':#昆山药网
            print ('选择承运商-京东物流药网')
            self.find_element (R.order_management.cq_debang).click ()
        elif warehouse_id == '10':#天津仓
            print('选择承运商-圆通药网')
            self.find_element(R.order_management.yw_yuantong).click()
        else:
            print('选择承运商-圆通药网')
            self.find_element(R.order_management.yw_yuantong).click()
            sleep(1)
        print('指派')
        self.click(R.order_management.assign)
        sleep(1)



