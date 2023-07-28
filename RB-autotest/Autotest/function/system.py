'''
Created on 2017年8月31日

@author: geqiuli
'''
import time
import os

import pytest
from function import conf
from function import io_

from email.mime.text import MIMEText
from email.header import Header
import smtplib


projname='AutoTest'
root_dir=os.path.abspath(__file__).split(projname)[0]+projname+os.sep
#print(root_dir)

def get_report_path(fileName):
    timeStamp = time.strftime('%Y%m%d_%H%M%S')
    return conf.get_system_path() + '\\report\\' + fileName + "_" + timeStamp + ".html"

def get_latest_file(dirname,*subdirs,**kw):
    '''此处以项目名AutoTest为根目录开始查找
    @param dirname: 一级目录
    @param subdirs: 子目录，可多个
    @param kw:  指定参数名 tclevel : 针对dirname=report时，按用例级别选择report下的目录
    '''
    if dirname=='report':
        if kw['tclevel']==None:
            raise Exception('tclevel is required!')
        #subdir='AllPcTest-'+kw['tclevel']
        #tc_plat=kw['tclevel'].split('_')[0].title()
        #subdir='All'+tc_plat+'Test-'+kw['tclevel']
        subdir=kw['tclevel']
        absdir=root_dir+dirname+os.sep+subdir+os.sep
    else:
        absdir=root_dir+dirname+os.sep
        for sub in subdirs:
            absdir+=sub+os.sep
    print(absdir)
    file_new=''
    if os.path.isdir(absdir):
        lists_all = os.listdir(absdir)
    else:
        return file_new
    list_file=[]
    for f in lists_all:
        if os.path.isfile(absdir+f):
            list_file.append(f)
    list_file.sort(key=lambda fn:os.path.getmtime(absdir+fn))
    
    list_file2=[]
    if 'file_name' in kw:
        for lf in list_file:
            if kw['file_name'] in lf:
                list_file2.append(lf)
        if list_file2:
            file_new = absdir+ list_file2[-1]
            print('file_new: ',file_new)
            return file_new
        else:
            return file_new
    
    if list_file:
        file_new = absdir+ list_file[-1]
        print(file_new)
        return file_new
    else:
        return file_new
    

def screenshot_name_bytclevel(tclevel,n):
    '''返回保存截图的名称
    @param tclevel: 用例级别，如pc_1
    @param n: 数
    '''
    tc_plat=tclevel.split('_')[0].title()
    subdir=tclevel
    #subdir='All'+tc_plat+'Test-'+tclevel
    #subdir='AllPcTest-'+tclevel
    latest_report=get_latest_file('report',tclevel=tclevel)
    if latest_report:
        report_name=latest_report.split(subdir+'-')[1]
        fname=subdir+'-'+str(int(report_name[:-5])+1)
    else:
        fname=subdir+'-1'
    
    abs_fname=root_dir+'report'+os.sep+subdir+os.sep+'screenshot'+os.sep+fname+'-'+str(n)+'.png'
    print(abs_fname)
    return abs_fname

def screenshot_by_module(module,func):
#     latest_file=get_latest_file(module)
#     if latest_file:
#         file_num=latest_file.split(module+'-')[1]   #例如：shopcart-3.png
#         fname=module+'-'+str(int(file_num[:-4])+1)
#     else:
#         fname=module+'-1'
    fname=func+'_'+time.strftime('%Y%m%d_%H%M%S')+'.png'
    abs_fname=root_dir+'report'+os.sep+module+os.sep+fname
    print(abs_fname)
    return abs_fname
    
    
def runtc(tcname,tclevel,driver='Chrome',options=[]):
    '''运行测试用例
    @param tcname: 可以是文件名（名字含.py）、文件夹
    @param tclever: mark标记，筛选用例
    @param driver: 浏览器，不支持Remote'''
    
    #tc_plat=tclevel.split('_')[0].title()
    #subdir='All'+tc_plat+'Test-'+tclevel
    subdir=tclevel
    #subdir='AllPcTest-'+tclevel
    latest_report=get_latest_file('report',tclevel=tclevel)
    if latest_report:
        report_name=latest_report.split(subdir+'-')[1]
        fname=subdir+'-'+str(int(report_name[:-5])+1)+'.html'
    else:
        fname=subdir+'-1.html'
    
    report_name=root_dir+'report'+os.sep+subdir+os.sep+fname
    print(report_name)
    args=[tcname,'-m '+tclevel,'--driver='+driver]
    
    for opt in options:
        args.append(opt)
    args.append('--html=' + report_name)
    args.append('--self-contained-html')
    pytest.main(args)

def run_case(tcname,tclevel,driver='Chrome',env='prd',options=[]):
    '''运行测试用例
    @param tcname: 可以是文件名（名字含.py）、文件夹
    @param driver: 浏览器，不支持Remote'''
    subdir=tclevel
    latest_report=get_latest_file('report',tclevel=tclevel)
    if latest_report:
        report_name=latest_report.split(subdir+'-')[1]
        fname=subdir+'-'+str(int(report_name[:-5])+1)+'.html'
    else:
        fname=subdir+'-1.html'
    
    report_name=root_dir+'report'+os.sep+subdir+os.sep+fname
    print(report_name)
    args=[tcname,'-m '+tclevel,'--exc_env='+env,'--driver='+driver]
    
    for opt in options:
        args.append(opt)
    args.append('--html=' + report_name)
    args.append('--self-contained-html')
    pytest.main(args)

def send_mail_test(subject,content,to_users):
    account=io_.read_txt('local_account', 'yw_local')     
    if account[0]=='qa_manage':
        sender=account[0]+'@yiyaowang.com'
    else:
        sender=account[0]+'@111.com.cn'
    #print(sender)
    
    #cc_user='gusaijun@111.com.cn'
    msg = MIMEText(content, 'html', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = sender
    msg['To'] = ','.join(to_users)
    #msg['Cc'] = cc_user
    
    server = smtplib.SMTP()
    server.connect("mail.yiyaowang.com")
#     server.connect("10.6.8.20")
    server.starttls()  
    server.login(account[0],account[1])  
    #print('邮箱登录成功')
    
    senders=server.sendmail(sender, to_users, msg.as_string())
    print(senders)
    server.quit()
    return True  


def send_mail_test_new(subject, content, to_users):
    account = io_.read_txt('local_account', 'yw_local')
    # if account[0]=='qa_manage':
    #     sender=account[0]+'@yiyaowang.com'
    # else:
    #     sender=account[0]+'@111.com.cn'
    # print('sender:',sender)
    sender = account[0]
    print('sender:', sender)
    # cc_user='gusaijun@111.com.cn's
    msg = MIMEText(content, 'html', 'utf-8')
    msg['Subject'] = Header(subject, 'utf-8')
    msg['From'] = sender
    # msg['To'] = ','.join(to_users)
    msg['To'] = to_users
    # msg['Cc'] = cc_user

    server = smtplib.SMTP()
    # server = smtplib.SMTP_SSL("smtp.exmail.qq.com", 465)
    # server.set_debuglevel(1)
    server.connect("smtp.exmail.qq.com")
    # server.connect("10.6.8.20")
    server.starttls()
    server.login(sender, account[1])
    print('邮箱登录成功')

    senders = server.sendmail(sender, to_users, msg.as_string())
    print(senders)
    server.quit()
    return True

if __name__=='__main__':
    pass
