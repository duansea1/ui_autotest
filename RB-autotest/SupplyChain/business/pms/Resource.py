#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/3/7
# @Author  : wanghui

from selenium.webdriver.common.by import By

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

        # front_user_name = (By.ID, "username")  # 集成管理系统登录页用户名框
        # front_password = (By.ID, "password")  # 集成管理系统登录页密码框
        # front_login_button = (By.XPATH, '//*[@id="loginForm"]/div[5]/button')  # 集成管理系统登录页登录按钮
        front_user_name  = (By.NAME,'username')
        front_password = (By.NAME,'password')
        front_login_button = (By.XPATH,'//*[@id="login-from"]/span')
        manager_login_button=(By.XPATH,'//*[@id="loginForm"]/div[2]/button')

    class platform:
        """
        平台管理类
        """
        menus = (By.XPATH,'/html/body/div/div[2]/div/div/a/div/p[2]')
        def __init__(self):
            pass
        #pms_platform = (By.XPATH,'/html/body/div/div[2]/div/div/a[24]/div/p[1]')#采购管理平台

    class supplier_manager_check:
        """
        菜单：质管负责人审核
        """
        def __init__(self):
            pass
        menu_link = 'http://pms.111.com.cn/service/supplier/supplierQualiPersonExamine'
        search = (By.XPATH,'//*[@id="toolbar2"]/div[1]/span')#供应商质管负责人审核：查询
        reset_button = (By.XPATH,'//*[@id="toolbar2"]/div[2]/span')#重置按钮
        supplier_name = (By.ID,'supplierCompanyName') #供应商名称（简称）输入框
        supplier_code = (By.ID,'supplierCode') #供应商编号输入框
        supplier_status = (By.ID,'supplierStatus_txt')#供应商状态下拉框

    class supplier_check:
        """菜单：质管审核"""
        def __init__(self):
            pass
        menu_link = 'http://pms.111.com.cn/service/supplier/supplierQualiExamine'
        search = (By.XPATH,'//*[@id="toolbar2"]/div[1]/span')#查询按钮
        reset_button= (By.XPATH,'//*[@id="toolbar2"]/div[2]/span')#重置按钮
        supplier_name = (By.ID,'supplierCompanyName')
        supplier_code = (By.ID,'supplierCode')
        supplier_status = (By.ID,'supplierStatus_txt')

    class supplier:
        """
        菜单：供应商管理
        """
        def __init__(self):
            pass
        menu_link = 'http://pms.111.com.cn/service/supplier/management'
        search = (By.XPATH, '//*[@id="toolbar2"]/div[2]/span')  # 供应商管理:查询
        reset_button = (By.XPATH, '//*[@id="toolbar2"]/div[3]/span')  # 重置按钮
        supplier_name = (By.ID, 'supplierCompanyName')  # 供应商名称（简称）输入框
        supplier_code = (By.ID, 'supplierCode')  # 供应商编号输入框
        supplier_status = (By.ID, 'supplierStatus_txt')  # 供应商状态下拉框

    class qualification_check:
        """
        菜单：供应商资质管理
        """
        def __init__(self):
            pass
        menu_link ='http://pms.111.com.cn/service/supplier/qualifications/toList'
        search = (By.XPATH,'//*[@id="page-inner"]/div[1]/div/div/div/form/div[12]/button')#查询按钮
        create_time = (By.ID, 'createTime')  # 创建时间
        start_time = (By.NAME, 'daterangepicker_start')  # 创建时间的开始时间
        end_time = (By.NAME, 'daterangepicker_end')  # 创建时间的结束时间
        time_confirm_button = (By.XPATH, '/html/body/div[2]/div[3]/div/button[1]')  # 创建时间内的确认按钮
        table_items = (By.ID, 'supplierQualificationsList')  # 查询结果列表
        supplier_code = (By.ID, 'supplierCode')  # 供应商编号
        supplier_name = (By.ID, 'companyName')  # 供应商名称

    class po_order:
        """
        菜单：自动po--自动po订单
        """
        def __init__(self):
            pass
        
        menu_link = 'http://pms.111.com.cn/service/autoposet/autopoManagement'
        po_begin_time = (By.NAME,'supplierContactFax')
        po_end_time = (By.NAME,'inventoryKeeper')
        search = (By.XPATH,'//*[@id="toolbar2"]/div[2]/span')#查询按钮
        reset_button = (By.XPATH,'//*[@id="toolbar2"]/div[1]/span')#重置按钮
        table_items = (By.CSS_SELECTOR,'.l-grid-body-table>tbody') #查询结果列表
        supplier_code = (By.ID,'expressNo')#供应商编号
        supplier_name= (By.ID,'supplierName')#供应商注册名称
        po_code = (By.ID,'poCodes')#po编码

    class auto_po_sales_predic_management:
        """
        菜单：日销量预测
        """
        def __init__(self):
            pass
        menu_link='http://pms.111.com.cn/service/autopoSalesPredic/autoPoSalesPredicManagement'
        search = (By.XPATH,'//*[@id="page-inner"]/div[1]/div/div/div/form/div[4]/button[1]')#查询按钮
        table_items= (By.ID,'autopoSalesPredic')#查询列表，包含表头

    class po_argument_set:
        """
        菜单：自动po--采购优化参数设置
        """
        def __init__(self):
            pass
        menu_link = 'http://pms.111.com.cn/service/autopoPmp/merchantAutopoPmpManagement.do'
        search = (By.CSS_SELECTOR,'#toolbar2>.l-toolbar-item>span') #查询按钮
        product_code = (By.ID,'skuNosStr')#产品编码输入框
        warehourse = (By.ID,'warehouseId')#仓库下拉框
        table_items= (By.CSS_SELECTOR,'.l-grid-body-table>tbody')#查询结果列表，包含表头
        edit_button = (By.XPATH,'//*[@id="autopopmp"]/tbody/tr[1]/td[1]/a[1]')#编辑按钮
        warehourse_day = (By.ID,'autopoT')#编辑界面--目标仓库天数T
        safe_stock=(By.ID,'autopoK')#编辑界面--安全库存波动参数K
        submit_button= (By.ID,'btn_submit')#编辑界面--提交按钮

    class auto_po_management:
        """
        菜单：自动po--自动PO
        """
        def __init__(self):
            pass
        menu_link ='http://pms.111.com.cn/service/autopo/autoPoManagement.do'
        search = (By.CSS_SELECTOR,'#toolbar2>div.l-panel-btn>span')#查询按钮
        product_code = (By.ID,'skuno')#产品编码输入框
        table_items= (By.CSS_SELECTOR,'.l-grid-body-table>tbody')#查询结果列表，包含表头

    class po_set:
        """
        菜单：自动PO-设置
        """
        def __init__(self):
            pass
        menu_link ='http://pms.111.com.cn/service/autoposet/autopoSetManagment'
        search = (By.CSS_SELECTOR,'#toolbar2>.l-toolbar-item>span')#查询按钮
        product_code=(By.ID,'productCode')#产品编码输入框
        table_items = (By.CSS_SELECTOR,'.l-grid-body-table>tbody')#查询结果列表，包含表头

    class po_lack_management:
        """
        PO缺货清单管理
        """
        def __init__(self):
            pass
        menu_link = 'http://pms.111.com.cn/jsp/lack/poLackManagement.jsp'
        search = (By.XPATH,'//*[@id="toolbar2"]/div[2]')#查询按钮
        table_items = (By.XPATH,'//*[@id="maingrid4"]/div[3]/div/div/div[4]/div[2]/div/table')#查询结果列表，包含表头

    class product_Coms_Rate_search:
        """
        产品佣金比率查询
        """
        def __init__(self):
            pass
        menu_link ='http://pms.111.com.cn/jsp/merchant/productComsRate.jsp'
        search = (By.CSS_SELECTOR,'#toolbarButtons>.l-panel-btn>span')#查询按钮
        product_code =(By.ID,'productCodes')#产品编码输入框
        table_items = (By.XPATH,'//*[@id="productComsGrid"]/div[3]/div/div/div[4]/div[2]/div/table')#查询结果列表，不包含表头

    class merchant_coms_management:
        """
        商家佣金管理
        """
        def __init__(self):
            pass
        menu_link = 'http://pms.111.com.cn/jsp/merchant/mecComsManagement.jsp'
        search = (By.XPATH,'//*[@id="toolbarButtons"]/div[1]/span')#查询按钮
        product_code = (By.ID,'productCodes')#产品编码输入框
        apply_code = (By.ID,'comsApplyCode')#申请编码输入框
        table_items = (By.CSS_SELECTOR,'.l-grid-body-table>tbody')#查询结果列表，不包含表头

    class merchant_coms_check:
        """
        商家佣金审核
        """
        def __init__(self):
            pass
        menu_link = 'http://pms.111.com.cn/jsp/merchant/mecComsApplyCheck.jsp'
        search = (By.XPATH,'//*[@id="toolbarButtons"]/div[1]/span')#查询按钮
        apply_code = (By.ID,'comsApplyCode')#申请编号输入框
        table_items=(By.CSS_SELECTOR,'.l-grid-body-table>tbody')#查询结果列表，不包含表头

    class contract_sync:
        """
        合同返利
        """
        def __init__(self):
            pass
        menu_link = 'http://pms.111.com.cn/service/rebate/contractSync/toList'
        search = (By.XPATH,'//*[@id="page-inner"]/div[1]/div/div/div/form/div[3]/button')#查询按钮
        contract_code=(By.ID,'contractCode')#合同编号输入框
        table_items=(By.XPATH,'//*[@id="rebateContractSyncList"]')#查询结果列表，包含表头

    class contract_manage:
        """
        合同管理
        """
        def __init__(self):
            pass
        menu_link ='http://pms.111.com.cn/service/cons/cons_manage'
        search = (By.ID,'query')#查询按钮
        contract_code = (By.ID,'contract_code')#合同编号输入框
        table_items= (By.XPATH,'//*[@id="grid-table"]')#查询结果列表，不包含表头

    class contract_examine:
         """
         合同审批
         """
         def __init__(self):
             pass
         menu_link ='http://pms.111.com.cn/service/cons/cons_examine'
         search = (By.XPATH,'//*[@id="query"]/i') #查询按钮
         contract_code = (By.ID,'contract_code')#合同编号输入框
         table_items = (By.ID,'grid-table')#查询结果列表，不包含表头

    class brand_manage:
        """
        品牌方管理
        """
        def __init__(self):
            pass
        menu_link = 'http://pms.111.com.cn/service/cons/brand_manage'
        search = (By.ID,'query')#查询按钮
        brand_name = (By.ID,'name')#品牌方名称
        table_items = (By.ID,'grid-table')#查询结果列表，不包含表头

    class deposit_examine:
        """
        保证金审核
        """
        def __init__(self):
            pass
        menu_link = 'http://pms.111.com.cn/service/supplier/deposit_examine.do'
        search = (By.ID,'buttonQueryButton')#查询按钮
        supplier_name = (By.ID,'supplierCompanyName')#供应商名称
        table_items = (By.XPATH,'//*[@id="maingrid4"]/div[3]/div/div/div[4]/div[2]/div/table')#查询结果列表，不包含表头

    class supplier_product_inPrice_check:
        """
        进价一审
        """
        def __init__(self):
            pass
        menu_link = 'http://pms.111.com.cn/jsp/product/supplierProductInPriceCheck.jsp'
        search = (By.XPATH,'//*[@id="toolbar2"]/div[4]/span')
        table_items = (By.XPATH,'//*[@id="maingrid4"]/div[3]/div/div/div[4]/div[2]/div/table')#查询结果列表，不包含表头

    class supplier_product_inPrice_check2:
        """
        进价二审
        """
        def __init__(self):
            pass
        menu_link = 'http://pms.111.com.cn/jsp/product/supplierProductInPriceCheck2.jsp'
        search = (By.XPATH,'//*[@id="toolbar2"]/div[4]/span')#查询按钮
        table_items = (By.XPATH,'//*[@id="maingrid4"]/div[3]/div/div/div[4]/div[2]/div/table')#查询结果列表，不包含表头

    class supplier_product_quality_check_audit:
        """
        质量档案(首营品种审核)
        """
        def __init__(self):
            pass
        menu_link = 'http://pms.111.com.cn/jsp/product/supplierProductQualityCheckAudit.jsp'
        search = (By.XPATH,'//*[@id="toolbar2"]/div[1]/span')#查询按钮
        reset_button=(By.XPATH,'//*[@id="toolbar2"]/div[2]/span')#重置按钮
        product_codes=(By.ID,'productCodes')#产品编码输入框
        product_name=(By.ID,'productCname')#产品名称输入框
        table_items = (By.XPATH,'//*[@id="maingrid4"]/div[3]/div/div/div[4]/div[2]/div/table')#查询结果列表，不包含表头

    class supplier_product_quality_check_list:
        """
        质量管理
        """
        def __init__(self):
            pass
        menu_link = 'http://pms.111.com.cn/jsp/product/supplierProductQualityCheckList.jsp'
        reset_button = (By.XPATH,'//*[@id="toolbar2"]/div[2]/span')#重置按钮
        search = (By.XPATH,'//*[@id="toolbar2"]/div[1]/span')#查询按钮
        product_codes = (By.ID,'productCodes')#产品编码输入框
        product_name = (By.ID,'productCname')#产品名称输入框
        table_items = (By.XPATH,'//*[@id="maingrid4"]/div[3]/div/div/div[4]/div[2]/div/table')#查询结果列表，不包含表头

    class inner_tran_order_management:
        """
        TO内采内退管理
        """
        def __init__(self):
            pass
        menu_link ='http://pms.111.com.cn/jsp/to/innerTranOrderManagement.jsp'
        search = (By.XPATH,'//*[@id="toolbar2"]/div[2]')#查询按钮
        tranOrder_codes = (By.ID,'tranOrderCodes')#单据号输入框
        table_items = (By.CSS_SELECTOR,'.l-grid-body-table>tbody')#查询结果列表，不包含表头

    class inner_po_management:
        """
        历史po内采
        """
        def __init__(self):
            pass
        menu_link = 'http://pms.111.com.cn/jsp/po/innerPoManagement.jsp'
        search = (By.XPATH,'//*[@id="toolbar2"]/div[2]')#查询按钮
        po_codes=(By.ID,'poCodes')# PO编码

    class warehouse_management:
        """
        仓库管理
        """
        def __init__(self):
            pass
        menu_link='http://pms.111.com.cn/service/warehouse/whIndex'
        search = (By.ID,'qryBtn')
        table_items = (By.ID,'grid-table')

    class request_bill:
        """
        请货单
        """
        def __init__(self):
            pass
        menu_link = 'http://pms.111.com.cn/service/kb/requestBill/toList'
        search = (By.CSS_SELECTOR,'#requestBillForm>#toolbar2>.l-toolbar-item>span')#查询按钮
        bill_no=(By.ID,'billNo')#请货单编码输入框
        store_name = (By.ID,'storeName')#门店名称输入框
        store_code=(By.ID,'storeCode')#门店编码输入框
        table_items = (By.CSS_SELECTOR,'.l-grid-body-table>tbody')   #查询结果

    class product_mapper:
        """
        客户对码管理
        """
        def __init__(self):
            pass
        menu_link = 'http://pms.111.com.cn/service/scm/productMapper/toList'
        search = (By.CSS_SELECTOR,'#customerCodePair>#toolbar2>.l-panel-btn>span')#查询按钮
        product_code = (By.ID,'productCode')#产品编码输入框
        customer_product_code = (By.ID,'customerProductCode')#客户产品编码输入框
        product_name = ( By.ID,'productName')#产品名称输入框
        table_items = (By.ID,'customerCodePair')

    class kingbos_inner_tran_order_management:
        """
        门店内采内退管理
        """
        def __init__(self):
            pass
        menu_link = 'http://pms.111.com.cn/jsp/to/kingbosInnerTranOrderManagement.jsp'
        search = (By.XPATH,'//*[@id="toolbar2"]/div[1]') #查询按钮
        tran_order_codes=(By.NAME,'tranOrderCodes')#单据号输入框
        table_items=(By.XPATH,'//*[@id="maingrid4"]/div[3]/div/div/div[4]/div[2]/div/table')

    class product_stock:
        """
        客户库存管理
        """
        def __init__(self):
            pass
        menu_link = 'http://pms.111.com.cn/service/scm/productStock/toList'
        search = (By.CSS_SELECTOR,'#requestBillForm>#toolbar2>.l-panel-btn>span')#查询按钮
        table_items= (By.CSS_SELECTOR,'.l-grid-body-table>tbody')

    class imnormal_stock:
        """
        非备管理
        """
        def __init__(self):
            pass
        menu_link='http://pms.111.com.cn/service/imnormal/imnormalStock/toManagementList'
        search = (By.XPATH,'//*[@id="toolbar2"]/div[1]/span')#查询按钮
        reset_button= (By.XPATH,'//*[@id="toolbar2"]/div[2]/span')#重置按钮
        demand_code = (By.ID,'demandCode')#需求编号
        applicants = (By.ID,'applicants')#申请人
        supplier_name = (By.ID,'supplierName')#供应商名称
        supplier_code = (By.ID,'supplierCode')#供应商编码
        table_items = (By.XPATH,'//*[@id="maingrid4"]/div[3]/div/div/div[4]/div[2]/div/table')#不包含表头

    class imnormal_stock_to_caikong:
        """
        非备-采控管理
        """
        def __init__(self):
            pass
        menu_link ='http://pms.111.com.cn/service/imnormal/imnormalStock/toCaikongList'
        reset_button = (By.XPATH,'//*[@id="toolbar2"]/div[2]')#重置按钮
        search = (By.XPATH,'//*[@id="toolbar2"]/div[1]')#查询按钮
        demand_code = (By.ID, 'demandCode')  # 需求编号
        applicants = (By.ID, 'applicants')  # 申请人
        supplier_name = (By.ID, 'supplierName')  # 供应商名称
        supplier_code = (By.ID, 'supplierCode')  # 供应商编码
        table_items = (By.XPATH, '//*[@id="maingrid4"]/div[3]/div/div/div[4]/div[2]/div/table')  # 不包含表头

    class po_management:
        """PO管理"""
        menu_link = 'http://pms.111.com.cn/jsp/po/purchaseOrderManagement.jsp'

        product_code = (By.NAME,'productCodes') #产品编码
        po_code = (By.NAME,'poCodes') #'po编码'
        po_createdate = (By.ID,'createStartDate') #'po生成时间'
        query_btn = (By.XPATH,'//*[@id="toolbar2"]/div[2]/span') #'查询按钮'
        copy_rtv = (By.XPATH,'//*[@id="maingrid4|2|r1001|c102"]/div/a[2]') #复制rtv
        # copy_po = (By.XPATH,'//*[@id="maingrid4|2|r1001|c102"]/div/a') #'复制po'
        copy_po = (By.CSS_SELECTOR,'.l-grid-body > div > table > tbody > tr:nth-child(1) > td:nth-child(1) > div > a') #'复制po'
        copy_yes_btn = (By.XPATH,'/html/body/div[6]/table/tbody/tr[2]/td[2]/div/div[3]/div/div[2]/div[3]') #'复制-弹窗-是'
        # send_yes_btn = (By.CLASS_NAME,'l-dialog-btn-inner') #'是'
        send_yes_btn = (By.XPATH,'/html/body/div[8]/table/tbody/tr[2]/td[2]/div/div[3]/div/div[2]/div[3]') #'是'
        confirm_btn = (By.CLASS_NAME,'l-dialog-btn-inner') #'确定'
        # confirm_btn = (By.XPATH,'/html/body/div[6]/table/tbody/tr[2]/td[2]/div/div[2]/div/div[1]/div[3]') #'确认'

        chose = (By.XPATH,'//*[@id="maingrid4|1|r1001|c101"]/div/span') #'勾选po'

        approve = (By.XPATH,'//*[@id="toolbar2"]/div[3]/span') #'批准'

        # close = (By.XPATH,'/html/body/div[7]/table/tbody/tr[1]/td[2]/div/div[3]') #'关闭弹窗'
        close = (By.CLASS_NAME,'l-dialog-close') #'关闭弹窗'
        confirm_send = (By.XPATH,'//*[@id="toolbar2"]/div[4]/span') #'确认发货'

        negative_po_create_rtv_btn = (By.XPATH,'//*[@id="toolbar2"]/div[5]/span') #'负po生成RTV-按钮'
        negative_po_close_btn = (By.CLASS_NAME,'l-dialog-btn-inner') #负po生成RTV-弹窗

    class to_management:
        """to管理"""
        menu_link = "http://pms.111.com.cn/jsp/to/tranOrderManagement.jsp"

        to_code = (By.NAME,'tranOrderCodes') #to编码
        to_createdate = (By.ID,'createDateStart') #to生成时间
        #reset_btn =(By.XPATH,'//*[@id="toolbar2"]/div[4]/span') #重置按钮
        reset_btn = By.XPATH,"//div[@class='l-toolbar-item l-panel-btn']/span[text()='重置']"
        query_btn = (By.XPATH,'//*[@id="toolbar2"]/div[3]/span') #查询按钮

        to_approve = (By.XPATH,'//*[@id="toolbar2"]/div[5]/span') #批准选中的调拨单

        approve_yes_btn = (By.XPATH,'/html/body/div[6]/table/tbody/tr[2]/td[2]/div/div[3]/div/div[2]/div[3]') #批准-弹窗-是
        close = (By.CLASS_NAME,'l-dialog-btn-inner') #批准-弹窗-关闭按钮














