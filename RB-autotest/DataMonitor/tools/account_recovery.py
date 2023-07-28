'''
# -*- coding: utf-8 -*-
#开发人员:   chenpeng
#开发日期:   2019-06-28
#文件项目:   测试数据管理
#文件名称:   测试数据自动恢复
 '''

from public.files import  read_json
from public.mysql_opr import query_mysql
import os
import time
import datetime

yc_user_dbinfo = {"host" : "mysql2.test.yiyaowang.com","user" : "yc_user","password" : "d41d8cd98f00b204","port" : 3306,"data" : "yc_user"}
yc_mall_dbinfo = {"host" : "10.6.168.14","user" : "b2btest","password" : "b5zUoR4JbcK3emhhUxdL","port" : 3306,"data" : "yihaoyaocheng"}
qateam_dbinfo = {"host" : "yyw-0345","user" : "qauser","password" : "qa_123456","port" : 3306,"data" : "qateam"}
now = datetime.datetime.now ()
current_time = now.strftime ('%Y-%m-%d %H:%M:%S ')
delta = datetime.timedelta (days=366)
#n_days = now + delta  # 获取当前时间的下一年
n_days = (now + delta).strftime('%Y-%m-%d %H:%M:%S ')  # 获取当前时间的下一年


class AccountRecovery:
    '''账号类'''
    def account_recovery_auto(self):
        '''查看数据库保存的密码是否与JOSN文件密码一致，如不一致，则自动更新'''
        username_list=[]
        pwd_list=[]
        login_pwd_list=[]
        use_info=read_json('account_in_db','b2b')
        #use_info=read_json('user_pwdrecovery_test','b2b')
        # pwd=read_json('user_pwdrecovery_test','b2b')
        for a in use_info :
            username_list.append(a['name'] )
            pwd_list.append(a['password'])
            login_pwd_list.append(a['login_pwd'])

        #print('username_list',username_list)
        #print('pwd_list',pwd_list)
        #print(type(username_list))
        username=tuple(username_list)
        print('hh',username)
        #print('username',username)
        #print(type(username))
        args=','.join(username)
        SELECT_SQL = "SELECT id,username,password from t_passport_user where username in %s order by instr(',%s,',CONCAT(',',username,','))" % (username,args,)#查询结果按查询条件顺序排序
        #print(SELECT_SQL)
        result1 = query_mysql (yc_user_dbinfo['host'], yc_user_dbinfo['user'], yc_user_dbinfo['password'], yc_user_dbinfo['port'], yc_user_dbinfo['data'],sql=SELECT_SQL)
        for i in range(0,len(result1['data'])):
            username_db=(result1['data'][i])[1]
            pwd_db=(result1['data'][i])[2]
            username_json=username[i]
            pwd_json=pwd_list[i]
            pwd_login_json=login_pwd_list[i]
            #print('JOSN_DATA:',username_json,pwd_json)
            #print('DB_DATA:',username_db,pwd_db)
            if username_db ==username_json:
                if pwd_db != pwd_json:
                    print('密码异常的账号：'+username_db)
                    UPDATA_SQL = "update t_passport_user set `password`='%s' WHERE username='%s'" %(pwd_json,username_db)
                    #print(UPDATA_SQL)
                    UPDATE = query_mysql (yc_user_dbinfo['host'], yc_user_dbinfo['user'], yc_user_dbinfo['password'],
                                           yc_user_dbinfo['port'], yc_user_dbinfo['data'], sql=UPDATA_SQL)
                    print(username_db+'的密码已更新为：'+pwd_login_json)
                else:
                    print(username_db+'---账号密码正常')
            else:
                print('当前账号异常，请检查JOSN文件')

if __name__ == '__main__':
    print('----------测试数据监控并自动恢复-----------')
    user=AccountRecovery()
    print('一、账号数据监控并恢复')
    #user.account_recovery_auto()  #账号数据
      
