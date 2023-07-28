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

    ASN_type = By.ID, "selectForm:detailTable:0:asnType", "ASN类型"
    ASN_status = By.ID, "selectForm:detailTable:0:asnStatus", "ASN状态"


class Receive:
    ASN_input = By.ID, "searchForm:asnNo", "ASN编号"
    search_button = By.ID, "searchForm:btnQuery1", "查询按钮"
    receive_button = By.ID, "searchForm:receiveBtn", "完成收货按钮"


class Accept:
    ASN_input = By.ID, "searchForm:asnNo", "ASN编号"
    search_button = By.ID, "searchForm:btnQuery1", "查询按钮"
    no_invoice_button = By.ID, "invoiceForm:noInvoiceBtn", "无发票按钮"
    ASN_link = By.XPATH, "//div[@id='searchForm:searchArea']/div[1]/table/tbody/tr[2]/td[2]/div/table/tbody/tr/td/a", "点击ASN超链接"

    product_barcode = By.ID, "searchForm:productBarcode", "产品条码"
    receive_qty = By.ID, "searchForm:qty", "验收数量"
    close_image = By.ID, "searchForm:ajForm:skuImageColse", "关闭图片"
    full_box = By.ID, "fullBox", "整箱"
    close_aduit_window = By.XPATH, "//div[@id='saveForm:operDiv']/input[2]", "审核弹框-关闭"


class OnShelves:
    ASN_input = By.ID, "searchForm:asnNo", "ASN编号"
    search_button = By.ID, "searchForm:btnQuery", "查询按钮"
    onshelves_status = By.XPATH, "//div[@id='selectForm:dataDiv']/table/tbody/tr/td[3]", "上架状态"
    onshelves_num = By.XPATH, "//tr[@class='rich-table-row rich-table-firstrow listTableSingular']/td[2]/div/a", "上架单号"

    all_selected = By.XPATH, "//tr[@class='rich-table-subheader ']/th[1]/div/input", "全选框"
    confirm_onshelves = By.XPATH, "//div[@id='saveForm:operDiv']/input[2]", "确认上架"
    force_onshelves = By.XPATH, "//div[@id='saveForm:operDiv']/input[3]", "强制上架"
    close_onshelves_window = By.XPATH, "//div[@id='saveForm:operDiv']/input[6]", "上架弹框-关闭"


class Aduit:
    ASN_input = By.XPATH, "//form[@id='searchForm']/table/tbody/tr[1]/td[2]/input", "ASN编号"
    search_button = By.ID, "searchForm:btnQuery", "查询按钮"
    ASN_num = By.XPATH, "//tr[@class='rich-table-row rich-table-firstrow listTableSingular']/td[2]/a", "ASN编号"
    aduit_button = By.XPATH, "//div[@id='saveForm:operDiv']/input[3]", "审核弹框-审核"
    close_button = By.XPATH, "//div[@id='saveForm:operDiv']/input[5]", "审核弹框-关闭"
