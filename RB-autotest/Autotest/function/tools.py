#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Created on 2017年11月3日

@author: geqiuli
'''
from email.mime.text import MIMEText
from email.header import Header
import smtplib
import time


def send_mail(file_new,mail_to):
    with open(file_new,'rb') as f:
        mail_body = f.read()
    
    users=""
    with open(mail_to,'r') as f:
        for line in f.readlines():
            users+=line.strip()+";"
        
    timestamp=time.strftime('%Y-%m-%d')    
    mail_info = {
        "from": "uiautomationreport@111.com.cn",
        "to": users,
        "mail_subject": "【UI自动化测试报告  "+timestamp+'】',
        "mail_encoding": "utf-8"
    }
    msg = MIMEText(mail_body, "html", mail_info["mail_encoding"])
    msg["Subject"] = Header(mail_info["mail_subject"], mail_info["mail_encoding"])
    msg["From"] = mail_info["from"]
    msg["To"] = mail_info["to"] 
    
    smtp = smtplib.SMTP()
    smtp.connect("10.6.8.16")
    smtp.sendmail(msg['From'], msg['To'], msg.as_string())
    smtp.quit()
    print('email has send out !')

if __name__ == '__main__':
    pass