"""
Created on 2019.1.10

@author: whb

"""

from selenium.webdriver.common.by import By

user_name = 'admin'
user_password = 'admin123'


class Normal:
    message = By.CLASS_NAME, "rich-messages-label", "返回消息"


class Login:
    user_name = By.ID, "loginForm:userName", "用户名"
    password = By.ID, "loginForm:password", "用户密码"
    warehouse = By.ID, "loginForm:warehouse", "仓库选择框"
    login_button = By.ID, "loginForm:submitBtn", "登录按钮"


class ASNQuery:
    ASN_input = By.XPATH, "//form[@id='searchForm']/table/tbody/tr[1]/td[2]/input", "ASN编号"
    search_button = By.ID, "searchForm:btnQuery", "查询按钮"
    result = By.XPATH, "//tbody[@id='selectForm:detailTable:tb']/tr", "查询结果"

    ASN_type = By.ID, "selectForm:detailTable:0:asnType", "ASN类型"
    ASN_status = By.ID, "selectForm:detailTable:0:asnStatus", "ASN状态"


class Receive:
    ASN_input = By.ID, "searchForm:asnNo", "ASN编号"
    search_button = By.ID, "searchForm:btnQuery1", "查询按钮"
    receive_button = By.ID, "searchForm:receiveBtn", "完成收货按钮"
    result = By.XPATH, "//tbody[@id='selectForm:detailTable:tb']/tr", "查询结果"
    batch_no = By.ID, "selectForm:detailTable:0:batchNo", "批号"
    production_date = By.XPATH, "//div[@class='myCalendar' and starts-with(@style,'display: block')]/div/div[2]/div[2]/span[@class='focusCell']", "生产日期"
    expiration_date = By.XPATH, "//div[@class='myCalendar' and starts-with(@style,'display: block')]/div/div[2]/div[2]/span[@class='focusCell']", "有效期至"
    expected_qty = By.ID, "selectForm:detailTable:0:exptQty", "订货量"
    received_qty = By.ID, "selectForm:detailTable:0:qty", "实收数"
    consignment_no = By.ID, "selectForm:detailTable:0:consignmentNo", "随货同行单号"
    refer_price = By.ID, "searchForm:referPrice", "随货同行单金额"


class Accept:
    ASN_input = By.ID, "searchForm:asnNo", "ASN编号"
    search_button = By.ID, "searchForm:btnQuery1", "查询按钮"
    no_invoice_button = By.ID, "invoiceForm:noInvoiceBtn", "无发票按钮"
    ASN_link = By.XPATH, "//div[@id='searchForm:searchArea']/div[1]/table/tbody/tr[2]/td[2]/div/table/tbody/tr/td/a", "点击ASN超链接"

    product_barcode = By.ID, "searchForm:productBarcode", "产品条码"
    receive_qty = By.ID, "searchForm:qty", "验收数量"
    close_image = By.ID, "searchForm:ajForm:skuImageColse", "关闭图片"
    batch_no = By.CLASS_NAME, "batchNo", "批号"
    refer_no = By.ID, "searchForm:referNo", "随货同行单"
    comment = By.XPATH, "//div[@id='searchForm:notesDiv']/input", "备注"
    lpn_no = By.ID, "searchForm:lpn", "LPN"
    full_box = By.ID, "fullBox", "整箱"
    close_aduit_window = By.XPATH, "//div[@id='saveForm:operDiv']/input[2]", "审核弹框-关闭"
    release_button = By.ID, "searchForm:releaseBtn", "上架发布"


class OnShelves:
    ASN_input = By.ID, "searchForm:asnNo", "ASN编号"
    search_button = By.ID, "searchForm:btnQuery", "查询按钮"
    result = By.XPATH, "//div[@id='selectForm:dataDiv']/table/tbody/tr", "查询结果"
    onshelves_status = By.XPATH, "//div[@id='selectForm:dataDiv']/table/tbody/tr/td[3]", "上架状态"
    onshelves_num = By.XPATH, "//tr[@class='rich-table-row rich-table-firstrow listTableSingular']/td[2]/div/a", "上架单号"

    all_selected = By.XPATH, "//tr[@class='rich-table-subheader ']/th[1]/div/input", "全选框"
    confirm_onshelves = By.XPATH, "//div[@id='saveForm:operDiv']/input[2]", "确认上架"
    onshelves_message = By.XPATH, "//tr[@class='rich-table-subheader']/th[1]/div/input", "上架记录checkbox"
    force_onshelves = By.XPATH, "//div[@id='saveForm:operDiv']/input[3]", "强制上架"
    close_onshelves_window = By.XPATH, "//div[@id='saveForm:operDiv']/input[6]", "上架弹框-关闭"


class Aduit:
    ASN_input = By.XPATH, "//form[@id='searchForm']/table/tbody/tr[1]/td[2]/input", "ASN编号"
    search_button = By.ID, "searchForm:btnQuery", "查询按钮"
    result = By.XPATH, "//tbody[@id='selectForm:detailTable:tb']/tr", "查询结果"
    ASN_num = By.XPATH, "//tr[@class='rich-table-row rich-table-firstrow listTableSingular']/td[2]/a", "ASN编号"
    aduit_button = By.XPATH, "//div[@id='saveForm:operDiv']/input[3]", "审核弹框-审核"
    aduit_button_purchasing = By.XPATH, "//div[@id='saveForm:operDiv']/input[4]", "审核弹框-审核"
    close_button = By.XPATH, "//div[@id='saveForm:operDiv']/input[5]", "审核弹框-关闭"
    close_button_purchasing = By.XPATH, "//div[@id='saveForm:operDiv']/input[6]", "审核弹框-关闭"
