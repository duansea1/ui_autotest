#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2017/12/13
# @Author  : zhangqinqin

from selenium.webdriver.common.by import By
from selenium.webdriver.support.select import Select

class R(object):
    """
    资源定位对象，保存页面资源
    """

    def __init__(self):
        pass

    class Login:
        """
        登录类
        """

        def __init__(self):
            pass

        front_user_name = (By.ID, "loginName")  # 首页用户名框
        front_password = (By.ID, "password")  # 首页密码框
        front_login_button = (By.ID, "loginCheckBtnId")  # 首页登录按钮

    class menu:
        """
        菜单管理类
        """

        def __init__(self):
            pass

        menu_page_link = (By.XPATH, "/html/body/div[1]/div[2]/div[2]/ul/li[1]/ul/li[1]/div/span")  # 首页菜单：菜单管理
        # parentMenu =  (By.XPATH, "/html/body/div/div[2]/form/table/tbody/tr/td[2]/select/option[2]") #菜单管理：父菜单-配送商管理
        parentMenu = (By.ID, "parentId") #菜单管理：父菜单
        search = (By.XPATH,"/html/body/div/div[2]/form/div/div[1]")  #菜单管理：查询
        url = (By.XPATH,"/html/body/div/div[2]/form/table/tbody/tr/td[4]/input") #菜单管理：URL输入框
        menu_name = (By.XPATH,"/html/body/div/div[2]/form/table/tbody/tr/td[6]/input") #菜单管理：菜单名称输入框
        type = (By.XPATH,"/html/body/div/div[2]/form/table/tbody/tr/td[8]/select/option[3]") #菜单管理：类型-按钮
        reset = (By.XPATH,"//*[@id='toolbarButtons']/div[2]/span") #菜单管理：重置
        add = (By.XPATH,'//*[@id="toolbarButtons"]/div[3]/span') #菜单管理：新增按钮
        add_name = (By.XPATH,'//*[@id="add-table"]/tbody/tr[1]/td[2]') #菜单管理：新增菜单名称
        add_cancel = (By.XPATH,'/html/body/div[2]/table/tbody/tr[2]/td[2]/div/div[2]/div/div[1]/div[3]') #菜单管理：新增菜单取消


    class role:
        """
        角色管理类
        """

        def __init__(self):
            pass

        role_page_link = (By.XPATH, "/html/body/div[1]/div[2]/div[2]/ul/li[1]/ul/li[2]/div/span")  # 首页菜单：角色管理
        search = (By.XPATH, '//*[@id="toolbarButtons"]/div[1]/span')  # 角色管理：查询
        role_name = (By.XPATH,'//*[@id="name"]') #角色管理：角色名称输入框
        description = (By.XPATH,'//*[@id="description"]') #角色管理：描述输入框
        reset = (By.XPATH,'//*[@id="toolbarButtons"]/div[2]/span') #角色管理：重置
        add = (By.XPATH, '//*[@id="toolbarButtons"]/div[3]/span')  # 角色管理：新增按钮


    class user:
        """
        用户管理类
        """

        def __init__(self):
            pass

        user_page_link = (By.XPATH, "/html/body/div[1]/div[2]/div[2]/ul/li[1]/ul/li[3]/div/span")  # 首页菜单：用户管理

    class data:
        """
        数据字典类
        """

        def __init__(self):
            pass

        data_page_link = (By.XPATH, "//*[@id='tree']/li[1]/ul/li[4]/div/span")  # 首页菜单：数据字典

    class job:
        """
        定时任务类
        """

        def __init__(self):
            pass

        job_page_link = (By.XPATH, "//*[@id='tree']/li[1]/ul/li[5]/div/span")  # 首页菜单：定时任务


    class tms_menu:
        """tms系统-新菜单"""
        menu_link = 'http://tms2.111.com.cn/home'

        first_menu = (By.CSS_SELECTOR,'ul.layui-layout-left>li>a') # 一级菜单
        second_menu = (By.CSS_SELECTOR,'li.layui-nav-item>dl>dd>a') # 一级菜单
        user=(By.NAME,'username') #域账号用户名
        pwd=(By.NAME,'password') #域账号用户名
        login_button=(By.CSS_SELECTOR,"#login-from > span")
        frame = (By.XPATH,'/html/body/div/div[2]/div/div/div/div/iframe') # iframe输入框
        iframe1=(By.XPATH,'/html/body/div/div[2]/div/div/div/div/iframe') #页面详情frame
        iframe2=(By.XPATH,'//*[@id="layui-layer-iframe1"]') #弹框frame



    class order_management:
        """订单管理"""

        frame = (By.XPATH,'/html/body/div/div[2]/div/div/div/div/iframe') # iframe输入框
        carrier = (By.XPATH,'/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/table/tbody/tr/td[7]/div')  #运营商

        '''承运商指派'''
        do_code = (By.CSS_SELECTOR,'.layui-inline>input[name="code"]') # DO单号
        query_btn = (By.ID,'address_query_btn') # 查询按钮
        time_from = By.ID,'handleTimeStart'#'转DO时间from'
        button = (By.CSS_SELECTOR,'.demoTable>button') #导出&指派按钮
        chose = (By.XPATH,'/html/body/div/div[2]/div[2]/div[1]/div[3]/div[1]/table/thead/tr/th[2]/div') #全选
        status = (By.XPATH,'/html/body/div/div[2]/div[2]/div[1]/div[2]/table/tbody/tr/td[10]/div') # 状态

        """承运商弹窗"""
        chose_carrier = (By.XPATH,'//*[@id="layui_form_xx"]/div/div[1]/div/div/div/input') #弹框-选择
        assign = (By.XPATH,'//*[@id="layui_form_xx"]/div/div[2]/div/button') #弹窗-指派

        yt_yaoguang = (By.XPATH,'//*[@id="layui_form_xx"]/div/div[1]/div/div/dl/dd[4]') #圆通药广
        yt_yaowang = (By.XPATH,'//*[@id="layui_form_xx"]/div/div[1]/div/div/dl/dd[3]')  #圆通药网
        gz_debang=(By.XPATH,'//dd[text()=“广州药城德邦”]')
        cq_debang=(By.XPATH,'//dd[text()=“重庆药城德邦”]')
        cq_yuantong=(By.XPATH,'//dd[text()=“重庆药城圆通”]')
        ks_debang=(By.XPATH,'//dd[text()=“昆山药城德邦”]')
        yw_jingdong=(By.XPATH,'//dd[text()=“京东物流药网”]')
        yw_yuantong=(By.XPATH,'//dd[text()=“圆通药网”]')


    class DO_management:
        '''出库时间'''
        leaveWH_from=(By.ID,"leaveDcTimeStart")
        first_do=(By.XPATH,"/html/body/div/div[2]/div/div[1]/div[2]/table/tbody/tr[1]/td[3]/div")

        tips_nodata=(By.XPATH,"/html/body/div/div[2]/div/div[1]/div[2]/div")

        frame_imput=(By.CSS_SELECTOR,"body > div > div.layui-body > div > div > div > div > iframe")
        do_no=(By.NAME,'code')
    class Carrier_platform_manage:
        '''承运商平平台管理'''

        add_btn=(By.XPATH,'/html/body/div[1]/div[2]/div[1]/button[1]') #新增按钮
        edit=(By.XPATH,'/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/div[2]/table/tbody/tr/td[3]/div/a') #编辑按钮
        query_btn=(By.ID,'query_btn') #查询按钮
        choice_box=(By.XPATH,'/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/div[2]/table/tbody/tr/td[2]/div/div/i') #第一个选项框
        delete_btn=(By.XPATH,'/html/body/div[1]/div[2]/div[1]/button[2]') #删除按钮
        first_code=(By.XPATH,'/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/table/tbody/tr/td[5]/div')  #第一条数据编码
        first_status=(By.XPATH,'/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/table/tbody/tr/td[11]/div') #第一条数据状态

        '''新增页面'''
        add_frame=(By.XPATH,'//*[@id="layui-layer-iframe1"]') #新增窗口frame
        code=(By.NAME,'code') #编码
        name=(By.NAME,'name') #名称
        type=(By.XPATH,'//*[@id="address_form"]/div[1]/div/div[3]/div/div/div/input') #类型
        kyd=(By.XPATH,'//*[@id="address_form"]/div[1]/div/div[3]/div/div/dl/dd[1]')   #快易达
        ldp=(By.XPATH,'//*[@id="address_form"]/div[1]/div/div[3]/div/div/dl/dd[2]')   #落地配
        url=(By.NAME,'reqUrl')  #请求URL
        key_word=(By.NAME,'signWord') #签收关键字
        no_word=(By.NAME,'excludeWord') #排除关键字
        save_btn=(By.CSS_SELECTOR,'#address_form > div:nth-child(3) > div > button')  #保存
        msg=(By.LINK_TEXT,u'插入失败编码重复')
        '''编辑页面'''
        status=(By.XPATH,'//*[@id="address_form"]/div[1]/div/div[7]/div/div/div/input') #状态
        sc=(By.XPATH,'//*[@id="address_form"]/div[1]/div/div[7]/div/div/dl/dd[2]') #已删除
        qy=(By.XPATH,'//*[@id="address_form"]/div[1]/div/div[7]/div/div/dl/dd[1]') #已启用

    class mysz:
        '''免邮设置'''
        frame = (By.XPATH,'/html/body/div/div[2]/div/div/div/div/iframe') # iframe输入框
        add_btn=(By.XPATH,'/html/body/div/div[2]/div[1]/button') #新增按钮
        query_btn=(By.ID,'btn-submit') #查询按钮
        reset_btn=(By.ID,'reset_btn') #重置按钮
        # province=(By.XPATH,'//*[@id="layui_form_xx"]/div/div[1]/div[1]/div/div/input') #省
        # city=(By.XPATH,'//*[@id="layui_form_xx"]/div/div[1]/div[2]/div/div/input') #市
        # BJS=(By.XPATH,'//*[@id="layui_form_xx"]/div/div[1]/div[1]/div/dl/dd[2]') #北京省
        # bjs=(By.XPATH,'//*[@id="layui_form_xx"]/div/div[1]/div[2]/div/dl/dd[2]') #  北京市
        # plat=(By.XPATH,'//*[@id="layui_form_xx"]/div/div[1]/div[3]/div/div/div/input') #平台
        # yc=(By.XPATH,'//*[@id="layui_form_xx"]/div/div[1]/div[3]/div/div/dl/dd[2]') #药城
        # yw=(By.XPATH,'//*[@id="layui_form_xx"]/div/div[1]/div[3]/div/div/dl/dd[3]') #药网
        business_man=(By.NAME,'bussinessId') #商家
        no_data=(By.XPATH,'/html/body/div/div[2]/div[2]/div[1]/div[2]/div') #无数据提示
        switch=(By.XPATH,'/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/table/tbody/tr[1]/td[8]/div/div') #启用/停用
        edit=(By.XPATH,'/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/table/tbody/tr/td[9]/div/a')  #编辑
        id_line1=(By.XPATH,'/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/table/tbody/tr[1]/td[5]/div')
        freefee_line1=(By.XPATH,'/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/table/tbody/tr/td[6]/div')


        '''编辑/新增页面'''
        sheng=(By.XPATH,'/html/body/div/form/div[1]/div[1]/div/div/div/input') #省
        shi=(By.XPATH,'/html/body/div/form/div[1]/div[2]/div/div/div/input') #市
        BJ=(By.XPATH,'/html/body/div/form/div[1]/div[1]/div/div/dl/dd[2]') #北京
        bjshi=(By.XPATH,'/html/body/div/form/div[1]/div[2]/div/div/dl/dd[2]') #北京市
        plat=(By.XPATH,'/html/body/div/form/div[1]/div[3]/div/div/div/input')#平台
        yc=(By.XPATH,'/html/body/div/form/div[1]/div[3]/div/div/dl/dd[2]') #药城
        yw=(By.XPATH,'/html/body/div/form/div[1]/div[3]/div/div/dl/dd[3]') #药网
        free=(By.NAME,'freeMount') #免邮金额
        freight=(By.NAME,'notFreeMount') #邮费
        save_btn=(By.XPATH,'/html/body/div/form/div[2]/div/button[1]') #保存按钮
        reset_btn2=(By.XPATH,'/html/body/div/form/div[2]/div/button[2]') #重置按钮

        tips=(By.XPATH,'//*[@id="layui-layer1"]/div[2]')  #启用/停用提示
        confirm_btn=(By.XPATH,'//*[@id="layui-layer1"]/div[3]/a[1]')  #确定按钮
        cancle=(By.XPATH,'//*[@id="layui-layer1"]/div[3]/a[2]') #取消按钮

    class Psgz:
        '''首页元素'''
        add_btn=(By.XPATH,'/html/body/div/div[2]/div[1]/button[1]')
        query_btn=(By.ID,'btn-submit') #查询按钮
        reset_btn=(By.ID,'reset_btn') #重置按钮
        warehouse1=(By.XPATH,'//*[@id="layui_form_xx"]/div/div[1]/div[1]/div/div/div/input')
        carrier1=(By.XPATH,'//*[@id="layui_form_xx"]/div/div[1]/div[2]/div/div/div/input')
        province1=(By.XPATH,'//*[@id="layui_form_xx"]/div/div[2]/div[1]/div/div/input')
        city1=(By.XPATH,'//*[@id="layui_form_xx"]/div/div[2]/div[2]/div/div/input')
        county1=(By.XPATH,'//*[@id="layui_form_xx"]/div/div[2]/div[3]/div/div/input')
        town1=(By.XPATH,'//*[@id="layui_form_xx"]/div/div[2]/div[4]/div/div/input')

        edit=(By.XPATH,'/html/body/div/div[2]/div[2]/div[1]/div[3]/div[2]/table/tbody/tr[1]/td[1]/div/a[1]')
        delete=(By.XPATH,'/html/body/div/div[2]/div[2]/div[1]/div[3]/div[2]/table/tbody/tr[1]/td[1]/div/a[2]')
        switch=(By.XPATH,'/html/body/div/div[2]/div[2]/div[1]/div[3]/div[2]/table/tbody/tr[1]/td[2]/div/div')
        nodata_tips=(By.XPATH,'/html/body/div/div[2]/div[2]/div[1]/div[2]/div')
        first_carrier=(By.XPATH,'/html/body/div/div[2]/div[2]/div[1]/div[2]/table/tbody/tr[1]/td[4]/div')
        first_Priority=(By.XPATH,'/html/body/div/div[2]/div[2]/div[1]/div[2]/table/tbody/tr[1]/td[14]/div/span')
        first_deliverytime=(By.XPATH,'/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/table/tbody/tr/td[13]/div')
        confirm_btn=(By.XPATH,'//*[@id="layui-layer1"]/div[3]/a[1]')
        '''新增页面'''
        '''-------------下拉框处理---------------'''
        warehouse=(By.XPATH,'/html/body/div/form/div[1]/div[1]/div/div/div/input')
        warehouse_value=(By.XPATH,"//dd[text()='广州药业仓库（新）']")
        orderSource=(By.XPATH,'/html/body/div/form/div[1]/div[3]/div/div/div/input')
        carrier2=(By.XPATH,'/html/body/div/form/div[1]/div[2]/div/div/div/input')
        isCollect=(By.XPATH,'/html/body/div/form/div[1]/div[4]/div/div/div/input')
        province=(By.XPATH,'/html/body/div/form/div[1]/div[5]/div/div/div/input')
        city=(By.XPATH,'/html/body/div/form/div[1]/div[6]/div/div/div/input')
        county=(By.XPATH,'/html/body/div/form/div[1]/div[7]/div/div/div/input')
        town=(By.XPATH,'/html/body/div/form/div[1]/div[8]/div/div/div/input')
        '''-------------下拉框处理---------------'''
        deliveryTime=(By.NAME,'deliveryTime')
        minAccessWeight=(By.NAME,'minAccessWeight')
        maxAccessWeight=(By.NAME,'maxAccessWeight')
        havePriority_=(By.XPATH,'/html/body/div/form/div[3]/div/div')

        save_btn=(By.XPATH,'/html/body/div/form/div[4]/div/button[1]')
        reset_but=(By.XPATH,'/html/body/div/form/div[4]/div/button[2]')

    class Yfmd:
        '''运费模板管理'''
        '''首页元素'''
        warehouse1=(By.XPATH,'/html/body/div[1]/div/div/div[1]/div/div[1]/div/div/input')
        carrier1=(By.XPATH,'/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/input')
        query_btn=(By.ID,'btn-submit')
        add_btn=(By.XPATH,'/html/body/div[1]/div/div/div[2]/button')
        edit_btn=(By.XPATH,'/html/body/div[1]/div/div/div[3]/div[1]/div[2]/table/tbody/tr[1]/td[1]/div/a')
        first_carrier=(By.XPATH,'/html/body/div[1]/div/div/div[3]/div[1]/div[2]/table/tbody/tr[1]/td[3]/div')
        first_area=(By.XPATH,'/html/body/div[1]/div/div/div[3]/div[1]/div[2]/table/tbody/tr[2]/td[4]/div')

        first_allarea=(By.XPATH,'/html/body/div/div/div/div[3]/div[1]/div[2]/table/tbody/tr/td[4]/div')
        '''新增页面元素'''
        warehouse2=(By.XPATH,'//*[@id="dataTable"]/div[1]/div[1]/div/div/input')
        carrier2=(By.XPATH,'//*[@id="dataTable"]/div[1]/div[2]/div/div/input')
        addrow_btn=(By.ID,'btn-addRow')
        submit_btn=(By.XPATH,'/html/body/div/form/div[2]/div/button')
        delete_btn=(By.XPATH,'//*[@id="addTbody"]/tr[2]/td[1]/div/button')

        firstweight=(By.XPATH,'//*[@id="addTbody"]/tr[1]/td[3]/div/input')
        firstFee=(By.XPATH,'//*[@id="addTbody"]/tr[1]/td[4]/div/input')
        secondWeight=(By.XPATH,'//*[@id="addTbody"]/tr[1]/td[5]/div/input')
        secondFee=(By.XPATH,'//*[@id="addTbody"]/tr[1]/td[6]/div/input')
        discount=(By.XPATH,'//*[@id="addTbody"]/tr[1]/td[7]/div/input')
        insuranceRate=(By.XPATH,'//*[@id="addTbody"]/tr[1]/td[8]/div/input')
        minInsurance=(By.XPATH,'//*[@id="addTbody"]/tr[1]/td[9]/div/input')
        paymentFeeRate=(By.XPATH,'//*[@id="addTbody"]/tr[1]/td[10]/div/input')
        paymentFee=(By.XPATH,'//*[@id="addTbody"]/tr[1]/td[11]/div/input')

        Area=(By.ID,'citySel')
        area1=(By.ID,'treeDemo_1_a')
        area2=(By.ID,'treeDemo_2_a')
        area3=(By.ID,'treeDemo_3_a')
        area4=(By.ID,'treeDemo_4_a')
        area5=(By.ID,'treeDemo_5_a')
        area6=(By.ID,'treeDemo_6_a')



        firstweight2 = (By.XPATH, '//*[@id="addTbody"]/tr[2]/td[3]/div/input')
        firstFee2 = (By.XPATH, '//*[@id="addTbody"]/tr[2]/td[4]/div/input')
        secondWeight2 = (By.XPATH, '//*[@id="addTbody"]/tr[2]/td[5]/div/input')
        secondFee2 = (By.XPATH, '//*[@id="addTbody"]/tr[2]/td[6]/div/input')
        discount2 = (By.XPATH, '//*[@id="addTbody"]/tr[2]/td[7]/div/input')
        insuranceRate2 = (By.XPATH, '//*[@id="addTbody"]/tr[2]/td[8]/div/input')
        minInsurance2 = (By.XPATH, '//*[@id="addTbody"]/tr[2]/td[9]/div/input')
        paymentFeeRate2 = (By.XPATH, '//*[@id="addTbody"]/tr[2]/td[10]/div/input')
        paymentFee2 = (By.XPATH, '//*[@id="addTbody"]/tr[2]/td[11]/div/input')

    class delivery_time_template:
        '''首页'''

        tips_nodata=(By.XPATH,"/html/body/div/div[2]/div/div[1]/div[2]/div")

        carrier=(By.XPATH,'//*[@id="layui_form_xx"]/div/div[4]/div/div/div/input')
        query_btn=(By.ID,'address_query_btn')
        upload_btn=(By.ID,'uploadExcel')
        delete_btn=(By.XPATH,'/html/body/div[1]/div[2]/div[1]/button[1]')
        edit_btn=(By.XPATH,'/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/div[2]/table/tbody/tr[1]/td[3]/div/a')
        check_box_all=(By.XPATH,'/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/div[1]/table/thead/tr/th[2]/div/div/i')
        carrier_line1=(By.XPATH,'/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/table/tbody/tr[1]/td[11]/div')
        delivery_time_line1=(By.XPATH,'/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/table/tbody/tr/td[15]/div')
        '''编辑页面'''
        delivery_time=(By.XPATH,'//*[@id="carrierDeliverRegion_form"]/div/div[1]/div[5]/div/div/div/input')
        save_btn=(By.XPATH,'//*[@id="carrierDeliverRegion_form"]/div/div[2]/button')


    class carrier_account_manage:

        '''首页'''
        Carrier_type=(By.NAME,'carrierType')
        query_btn=(By.ID,'address_query_btn')
        add_btn=(By.XPATH,'/html/body/div/div[2]/div[1]/button[1]')
        del_but=(By.XPATH,'/html/body/div/div[2]/div[1]/button[2]')
        check_box=(By.XPATH,'/html/body/div/div[2]/div[2]/div[1]/div[3]/div[1]/table/thead/tr/th[2]/div/div/i')
        edit_btn=(By.XPATH,'/html/body/div/div[2]/div[2]/div[1]/div[3]/div[2]/table/tbody/tr[1]/td[3]/div/a')
        first_carrier=(By.XPATH,'/html/body/div/div[2]/div[2]/div[1]/div[2]/table/tbody/tr[1]/td[5]/div')
        first_cardnumber=(By.XPATH,'/html/body/div/div[2]/div[2]/div[1]/div[2]/table/tbody/tr[1]/td[7]/div')
        first_delete=(By.XPATH,'/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/table/tbody/tr/td[17]/div')

        '''修改窗口'''
        carrie_code=(By.NAME,'carrierCode')
        carrier_type=(By.NAME,'carrierType')
        carrier_cardnumber=(By.NAME,'monthlyCard')
        carrier_account=(By.NAME,'customName')
        carrier_account_pwd=(By.NAME,'customPassword')
        carrier_requesturl=(By.NAME,'requestUrl')
        save_btn=(By.XPATH,'//*[@id="address_form"]/div[3]/div/button[1]')

    class Ckyf:
        '''仓库标准运费配置'''
        '''首页'''
        warehouse_frame1=(By.XPATH,'//*[@id="layui_form_xx"]/div/div[1]/div/div/div/input')
        #carrier_value=(By.XPATH,'//dd[text()="+warehouse+"]')
        query_btn=(By.ID,'btn-submit')
        add_btn=(By.XPATH,'/html/body/div/div[2]/div[1]/button')
        edit_btn=(By.XPATH,'/html/body/div/div[2]/div[2]/div[1]/div[2]/table/tbody/tr[1]/td[1]/div/a')
        warehouse_line1=(By.XPATH,'/html/body/div/div[2]/div[2]/div[1]/div[2]/table/tbody/tr[1]/td[2]/div')
        area_line1=(By.XPATH,'/html/body/div/div[2]/div[2]/div[1]/div[2]/table/tbody/tr/td[3]/div')
        fee_line1=(By.XPATH,'/html/body/div/div[2]/div[2]/div[1]/div[2]/table/tbody/tr/td[4]/div')

        '''编辑页面'''
        warehouse_frame2=(By.XPATH,'//*[@id="dataTable"]/div[1]/div[1]/div/div/div/input')
        fee_percent=(By.ID,'standardRate')
        delete_btn=(By.XPATH,'//*[@id="addTbody"]/tr/td[1]/div/button')

        area_sel=(By.ID,'citySel')
        area_sel2=(By.XPATH,'//*[@id="addTbody"]/tr[2]/td[2]/div[@class="layui-input-inline"]')

        area1=(By.ID,'treeDemo_1_span')
        area2=(By.ID,'treeDemo_2_span')
        area3=(By.ID,'treeDemo_3_span')
        area4=(By.ID,'treeDemo_4_span')
        area5=(By.ID,'treeDemo_5_span')
        area6=(By.ID,'treeDemo_6_span')

        standard_fee1=(By.XPATH,'//*[@id="addTbody"]/tr[1]/td[3]/div/input')
        standard_fee2=(By.XPATH,'//*[@id="addTbody"]/tr[2]/td[3]/div/input')
        addrow_btn=(By.ID,'btn-addRow')
        save_btn=(By.XPATH,'//*[@id="dataTable"]/div[3]/div[2]/button')

    class Yfdz:
        time_from=(By.ID,'leaveDcTimeStart')
        time_to=(By.ID,'leaveDcTimeEnd')
        do_no=(By.NAME,'code')
        status_sel=(By.XPATH,'//*[@id="layui_form_xx"]/div/div[8]/div/div/div/input')
        status='计算完成'
        status_value=(By.XPATH,'//dd[text()="'+status+'"]')
        query_btn=(By.ID,'address_query_btn')
        log_view=(By.XPATH,'/html/body/div/div[2]/div[2]/div[1]/div[3]/div[2]/table/tbody/tr[1]/td[2]/div/a[1]')
        do_line1=(By.XPATH,'/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/table/tbody/tr[1]/td[4]/div')
        carrier_line1=(By.XPATH,'/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/table/tbody/tr[1]/td[7]/div')
        actual_weight_line1=(By.XPATH,'/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/table/tbody/tr[1]/td[17]/div')
        FirstWeight_line1=(By.XPATH,'/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/table/tbody/tr[1]/td[18]/div')
        FirstFee_line1=(By.XPATH,'/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/table/tbody/tr[1]/td[19]/div')
        SecondWeight_line1=(By.XPATH,'/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/table/tbody/tr[1]/td[20]/div')
        SecondFee_line1=(By.XPATH,'/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/table/tbody/tr[1]/td[21]/div')
        discount_line1=(By.XPATH,'/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/table/tbody/tr[1]/td[22]/div')
        insurance_line1=(By.XPATH,'/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/table/tbody/tr[1]/td[23]/div')
        charges_line1=(By.XPATH,'/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/table/tbody/tr[1]/td[24]/div')
        actualfreight_line1=(By.XPATH,'/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/table/tbody/tr[1]/td[26]/div')

        rowCount=(By.XPATH,'//*[@id="layui-laypage-4"]/span[4]')
        Page_num=(By.XPATH,'//*[@id="layui-laypage-1"]/span[2]/input')
        confirm_btn=(By.XPATH,'//*[@id="layui-laypage-2"]/span[2]/button')

    class Czgl:
        '''称重管理'''

        carrier_sel=(By.ID,'carrierCodes')
        code='2222222'
        carrier_value=(By.XPATH,'//dd[@lay-value="'+code+'"]')
        warehouse_sel=(By.ID,'warehouseCodes')
        value = '2222222'
        warehouse_value = (By.XPATH, '//dd[@lay-value="' + code + '"]')
        handoverstate=(By.XPATH,'//*[@id="layui_form_xx"]/div/div[3]/div/div')
        time_from=(By.ID,'createTimeStart')
        time_to=(By.ID,'createTimeEnd')
        type=(By.XPATH,'//*[@id="layui_form_xx"]/div/div[5]/div/div')
        do=(By.NAME,'doCode')
        query_btn=(By.ID,'address_query_btn')
        handover_btn=(By.XPATH,'/html/body/div[1]/div[2]/div[1]/button[2]')
        handoverall_btn=(By.XPATH,'/html/body/div[1]/div[2]/div[1]/button[3]')

        checkall_box=(By.XPATH,'/html/body/div[1]/div[2]/div[2]/div[1]/div[3]/div[1]/table/thead/tr/th[2]/div/div/i')
        check_box1=(By.XPATH,'/html/body/div/div[2]/div[2]/div[1]/div[3]/div[2]/table/tbody/tr[1]/td[2]/div/div/i')
        check_box2=(By.XPATH,'/html/body/div/div[2]/div[2]/div[1]/div[3]/div[2]/table/tbody/tr[2]/td[2]/div/div/i')




        handover_msg=(By.XPATH,'//*[@id="ex_order_form"]/div/h2')
        remark=(By.ID,'associateMark')
        confirm_btn=(By.XPATH,'//*[@id="ex_order_form"]/div/div[2]/button')

        do_line1=(By.XPATH,'/html/body/div/div[2]/div[2]/div[1]/div[2]/table/tbody/tr[1]/td[5]/div')
        status_line1=(By.XPATH,'/html/body/div/div[2]/div[2]/div[1]/div[2]/table/tbody/tr[1]/td[10]/div')
        carrier_page1=(By.XPATH,'/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/table/tbody/tr/td[6]/div')
        warehouse_page1=(By.XPATH,'/html/body/div[1]/div[2]/div[2]/div[1]/div[2]/table/tbody/tr/td[7]/div')


    class COD_Refunds:
        rebateStatus_sel=(By.XPATH, '//*[@id="ra"]/div[2]/div/div/div/input')
        no_upload=(By.XPATH, '//*[@id="ra"]/div[2]/div/div/dl/dd[2]')
        leave_time=(By.ID, 'leaveDcTimeStart')
        do_input=(By.NAME,'code')
        query_btn=(By.ID, 'btn-submit')
        do_line1=(By.XPATH, '/html/body/div/div/div/div[8]/div[1]/div[2]/table/tbody/tr/td[4]/div')
        carrier_line1=(By.XPATH, '/html/body/div/div/div/div[8]/div[1]/div[2]/table/tbody/tr/td[7]/div')
        refunds1=(By.XPATH,'/html/body/div[1]/div/div/div[8]/div[1]/div[2]/table/tbody/tr/td[15]/div')
        status1=(By.XPATH, '/html/body/div[1]/div/div/div[8]/div[1]/div[2]/table/tbody/tr/td[17]/div')
        collect_amout=(By.XPATH,"/html/body/div/div/div/div[8]/div[1]/div[2]/table/tbody/tr/td[14]/div")
        upload_btn_normal=(By.ID,'uploadExcel')
        upload_btn_unusual=(By.ID,'uploadExExcel')


        check_box_1=(By.XPATH,'/html/body/div/div/div/div[8]/div[1]/div[3]/div[1]/table/thead/tr/th/div/div')
        #check_box_1=(By.XPATH,"//div[@class='layui-table-fixed layui-table-fixed-l']/table/thead/tr/th/div/div")

        refunds_btn=(By.ID,'confirm')
        batch_no_input=(By.NAME,'serialNum')

        refunds_onekey_btn=(By.ID,'oneKeyConfirmData')

        batch_no=(By.XPATH,'/html/body/div[1]/div/div/div[8]/div[1]/div[2]/table/tbody/tr[1]/td[18]/div')
        batchno_tips=(By.XPATH,'//div[@type="dialog"]/div[2]')  #一键返款输入批次号提示
        batchno_tips_btn=(By.XPATH,'//div[@type="dialog"]/div[3]/a[1]')

        frame =(By.XPATH,"//iframe")








































