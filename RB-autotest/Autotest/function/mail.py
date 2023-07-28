#!/usr/bin/python3
# -*- coding: utf-8 -*-

import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.header import Header
import sys
import time
from selenium import webdriver

driver = webdriver.PhantomJS()
driver.maximize_window()
driver.implicitly_wait(6)
driver.get(sys.argv[1])
time.sleep(1)
status = driver.find_element_by_xpath('/html/body/span[3]').text
print(status)
if '0 failed' in status:
    driver.quit()
    pass
else:
    driver.get_screenshot_as_file(sys.argv[2] + '.png')
    driver.quit()
    # 第三方 SMTP 服务
    mail_host = "mail.yiyaowang.com"  # 设置服务器
    mail_user = 'qa_manage'  # 用户名
    mail_pass = 'YW_manage'  # 口令

    sender = 'qa_manage@yiyaowang.com'
    receivers = ['qm_dept@111.com.cn']  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱
    # receivers = ['caocheng@111.com.cn;gaoyuhao@111.com.cn']

    msgRoot = MIMEMultipart('related')
    msgRoot['From'] = sender
    msgRoot['To'] = receivers
    # msgRoot['To']=Header("caocheng@111.com.cn;gaoyuhao@111.com.cn",'utf-8')
    subject = sys.argv[3]
    msgRoot['Subject'] = Header(subject, 'utf-8')

    msgAlternative = MIMEMultipart('alternative')
    msgRoot.attach(msgAlternative)

    mail_msg = """
        <p><img src="cid:image1"></p>
        """
    msgAlternative.attach(MIMEText(mail_msg, 'html', 'utf-8'))

    # 指定图片为当前目录
    fp = open(sys.argv[2] + '.png', 'rb')
    msgImage = MIMEImage(fp.read())
    fp.close()

    # 定义图片 ID，在 HTML 文本中引用
    msgImage.add_header('Content-ID', '<image1>')
    msgRoot.attach(msgImage)

    try:
        smtpObj = smtplib.SMTP()
        smtpObj.connect(mail_host, 25)  # 25 为 SMTP 端口号
        smtpObj.login(mail_user, mail_pass)
        smtpObj.sendmail(sender, receivers, msgRoot.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("Error: 无法发送邮件")

    fp = open(sys.argv[6] + '.png', 'rb')
