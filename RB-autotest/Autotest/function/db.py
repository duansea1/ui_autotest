'''
Created on 2017年8月3日

@author: caocheng
'''

import pymysql

from function.conf import get_system_value

address = get_system_value('db', 'address')
username = get_system_value('db', 'username')
password = get_system_value('db', 'password')
db_name = get_system_value('db', 'db_name')


def select(sql):
    try:
        db = pymysql.connect(address, username, password, db_name)
        cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
        # 执行SQL语句
        cursor.execute(sql)
        # 获取所有记录列表
        results = cursor.fetchall()
        return results
    except Exception:
        return 0
    finally:
        db.close()


def update(sql):
    try:
        db = pymysql.connect(address, username, password, db_name)
        cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
        # 执行SQL语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        return True
    except Exception:
        # 发生错误时回滚
        db.rollback()
        return False
    finally:
        db.close()


def insert(sql):
    try:
        db = pymysql.connect(address, username, password, db_name)
        cursor = db.cursor(cursor=pymysql.cursors.DictCursor)
        # 执行SQL语句
        cursor.execute(sql)
        # 提交到数据库执行
        db.commit()
        return True
    except Exception as e:
        # 发生错误时回滚
        db.rollback()
        print(e)
        return False
    finally:
        db.close()

if __name__ == '__main__':
    pass
#     orderid='00998765'
#     tclevl='pc_1'
#     sql="INSERT INTO orders (order_id,status,tclevel) VALUES ('"+orderid+"','0','"+tclevl+"')"
#     sql1="INSERT INTO orders (order_id,status,tclevel) VALUES ('00009988','0','pc_1')"
#     insert(sql)