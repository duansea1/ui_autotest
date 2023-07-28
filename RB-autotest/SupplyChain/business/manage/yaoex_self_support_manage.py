'''
Created on 2018年11月20日

@author: liya
'''
from selenium.webdriver.common.by import By
# from business.HomePage import Home
from business import BasePage
from time import sleep
from business.manage import resources as R
from selenium.webdriver.support.select import Select
from public.files import read_txt
from symbol import except_clause

class YaoexMenu(BasePage.Base):
    
    def __int__(self):
        pass   
        
    def father_menu(self,father_menu):
        """药城商家后台，左侧父菜单"""
#         father_name = self.find_elements_by_link_text(R.Yaoex_sp_manage.father_menu)
        father_name = self.find_elements(R.Yaoex_sp_manage.father_menu)
        for a in father_name:
            if a.text.strip() == father_menu:
                print('当前菜单：', a.text.strip())
                a.click()
                break
        sleep(3)
        self.switch_to_latest_windows()
        self.driver.implicitly_wait(10)
        
        
    def child_menu(self, child_menu):
        """
        药城商家后台，左侧父菜单下的子菜单"""
#         child_name = self.find_elements(R.Yaoex_sp_manage.child_menu)
        child_name = self.find_elements(R.Yaoex_sp_manage.child_menu)
        for c in child_name:
            if c.text.strip() == child_menu:
#                 flag=False
                print('当前菜单：', c.text.strip())
                c.click()
                break
        sleep(3)
        self.switch_to_latest_windows()
        
    def select_merchant(self, id='125476'):
        '''
        选择自营公司
        @param id：125476-重庆药业；8353-广东药业；95859-四川药业；104169-安徽药业...'''
        self.wait_until_display(R.Yaoex_sp_manage.merchants_id)
        if id !='125476':
            Select(self.find_element(R.Yaoex_sp_manage.merchants_id)).select_by_value(id)
            
    def choose_promotion_tab(self, tab):
        """
        选择活动tab
        @param tab: 特价活动，满减活动，满赠活动，套餐活动，优惠券设置"""  
#         tabs = self.find_elements(R.Yaoex_sp_manage.promotion_tab)
        tabs = self.driver.find_element_by_partial_link_text(tab)
        tabs.click()
        sleep(3)
        self.switch_to_latest_windows()
#         tabs = self.find_elements(R.Yaoex_sp_manage.promotion_tab)

    def creat_promotion(self): 
        """
        新增活动 """ 
        self.find_element(R.Yaoex_sp_manage.creat_promotin).click()  #新增活动按钮
        sleep(3)
        title = self.find_element(R.Yaoex_sp_manage.title)
        print('当前页面:', title.text.strip())
        
    def promotion_name(self, name):
        """输入活动名称"""
        self.find_element(R.Yaoex_sp_manage.promotion_Name).send_keys(name) #活动名称输入框
        sleep(1)     #选择活动开始-结束时间
#         self.switch_to_latest_windows()
#         self.driver.switch_to.active_element  #聚焦页面活动元素
#         self.driver.find_element_by_class_name('form-horizontal').click() 
#         sleep(1)
#         self.chose_custm(custm)  #选择客户组
#         self.find_element(R.Yaoex_sp_manage.upload).click() #点击上传按钮
#         self.chose_use_coupon('1') #选择不可用券
#         self.price_to_custm('1') #价格对未登录客户不展示
#         self.driver.switch_to.active_element
#         self.driver.find_element_by_class_name('main-content').click()

    def creat_promotion_btn(self):
        """提交活动"""
        self.find_element(R.Yaoex_sp_manage.createPromotion_btn).click() #点击创建活动按钮,提交活动
        sleep(1)
        
        
    def promotion_time(self, endyear,endmonth):
        """选择活动开始时间，结束时间
        @param endyear:结束-xx年
        @param endmonth:结束-xx月  """
        self.find_element(R.Yaoex_sp_manage.beginTime).click() #点击活动开始时间控件
#         self.driver.switch_to.frame('iframe')
#         self.driver.switch_to.frame(0)
        self.driver.switch_to.frame(self.driver.find_element_by_css_selector('body > div:nth-child(3) > iframe'))
        #聚焦开始时间控件弹窗
#         sleep(10)
#         self.driver.find_element_by_css_selector('.WdateDiv > #dpControl >#dpTodayInput').click()  
        self.find_element(R.Yaoex_sp_manage.time_dptoday).click() #选择开始时间，今天按钮
        sleep(3)
        self.switch_to_latest_windows()
        #跳出时间控件选择框
        self.find_element(R.Yaoex_sp_manage.endTime).click()  #点击活动结束时间控件
        self.driver.switch_to.frame(self.driver.find_element_by_css_selector('body > div:nth-child(3) > iframe'))
        #聚焦结束时间控件弹窗
#         self.driver.find_element_by_css_selector(R.Yaoex_sp_manage.time_year).clear() #点击清空XXXX年
        self.find_element(R.Yaoex_sp_manage.time_year).clear()
#         self.driver.find_element_by_css_selector(R.Yaoex_sp_manage.time_year).send_keys(endyear) 
        self.find_element(R.Yaoex_sp_manage.time_year).send_keys(endyear)
        #输入结束时间-XXX年
#         self.driver.find_element_by_css_selector(R.Yaoex_sp_manage.time_month).clear()
        self.find_element(R.Yaoex_sp_manage.time_month).clear()
#         self.driver.find_element_by_css_selector(R.Yaoex_sp_manage.time_month).send_keys(endmonth) 
        self.find_element(R.Yaoex_sp_manage.time_month).send_keys(endmonth)
        #输入结束时间--月份
        self.find_element(R.Yaoex_sp_manage.time_dpok).click()  #选择结束时间，确定按钮
        self.switch_to_latest_windows()
#         self.driver.switch_to_active_element()
        #跳出结束时间控件选择框
        self.driver.switch_to.active_element  #聚焦页面活动元素
        self.driver.find_element_by_class_name('form-horizontal').click() #点击旁边空白的页面
        sleep(3)
        
    def chose_custm(self, group):
        """选择客户组"""
#         custms = self.find_elements("#lefttable1 > tbody >tr")
        self.find_element(R.Yaoex_sp_manage.chose_customer_group).click()  #选择客户组 按钮
        self.find_element(R.Yaoex_sp_manage.input_group).send_keys(group) #输入客户组名称
        self.find_element(R.Yaoex_sp_manage.search_btn).click()   #搜索按钮
        sleep(3)
        self.find_element(R.Yaoex_sp_manage.customer_group).click()  #选中客户组
        self.find_element(R.Yaoex_sp_manage.submit_btn).click()   #确定按钮，提交
        print('选择客户组：', group)
        sleep(3)
        
    def chose_use_coupon(self,value='1'):
        """
        选择可用券，不可用券
        @param value: 0-可用，1-不可用"""
        
        coupon_value = self.driver.find_element_by_css_selector('.radio-inline> input[value="'+ str(value) +'"]')
        coupon_value.click()
        if value =='0':
            print('是否可用券：可用')
        else:
            print('是否可用券：不可用券')
        sleep(1)
        
    def price_to_custm(self, price='0'):
        """
        价格对未登录用户展示
        @param price:0-价格对未登录用户不展示, 1-对未登录用户展示 """
        if price == '1':
            self.find_element(R.Yaoex_sp_manage.priceVisible).click()
            print('价格对未登录用户展示')
        else:
            print('价格对未登录用户不展示')
            
    def search_promotion_name(self, name):
        """搜索促销活动名称"""
        self.find_element(R.Yaoex_sp_manage.promotion_Name).send_keys(name)
        self.find_element(R.Yaoex_sp_manage.search_btn).click()
        sleep(1)
        
    def operate_promotion(self, action):
        """操作促销活动
        @action：编辑，取消，编辑商品，导出活动商品，日志，销售数据导出"""
        if action =='编辑':
            print('操作促销活动： ', action)
            self.find_element(R.Yaoex_sp_manage.editor_promotion).click()
            title = self.find_element(R.Yaoex_sp_manage.title)
            print('当前页面:', title.text.strip())
        else:
            actions = self.find_elements(R.Yaoex_sp_manage.editor_merchant)
#             actions = self.driver.find_elements_by_css_selector('#promotionBody > tr:nth-child(1) > td:nth-child(6) > button')
            for a in actions:
                if a.text == action:
                    print('操作促销活动： ', a.text)
                    a.click()
                    title = self.find_element(R.Yaoex_sp_manage.title)
                    print('当前页面:', title.text.strip())
                    break
                sleep(3)
    
    def add_product(self, productcode):
        """
        添加活动商品
        @param productcode:本公司编码 """
        self.find_element(R.Yaoex_sp_manage.productCode).send_keys(productcode)  #输入本公司商品编码
        self.find_element(R.Yaoex_sp_manage.search_tab1).click() #查询按钮
        sleep(1)
        self.find_element(R.Yaoex_sp_manage.all_check_tab1).click()  #全选-复选框
        self.find_element(R.Yaoex_sp_manage.all_add_btn).click()     #外层的添加按钮
        self.find_element(R.Yaoex_sp_manage.confirm).click() #弹框确认，接受
#         self.driver.switch_to.alert()  #弹框确认，接受
#         self.driver.switch_to_alert().accept()
        sleep(1)
#         self.find_element(R.Yaoex_sp_manage.already_add_tab).click()
#         assert productcode in self.driver.page.source
                

                                       
        
        
            
                
        