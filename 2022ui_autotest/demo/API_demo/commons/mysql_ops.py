'''
Created on 2022年8月30日

@author:
sql执行的操作
'''
import pymysql as ms


def query_mysql(host, user, password, port, database, sql):
    '''执行mysql语句，执行完会关闭连接'''
    rsp_data = {}
    try:
        conn = ms.connect(
            host=host,
            user=user,
            port=port,
            passwd=password,
            database=database
        )
    except Exception as e:
        msg = ("获取数据库连接失败：%s" % e)
        rsp_data["code"] = 1
        rsp_data["msg"] = msg
        rsp_data["data"] = None
        rsp_data["rows"] = 0
        return rsp_data

    try:
        cursor = conn.cursor()
        count = cursor.execute(sql)
        # result=cursor.fetchall()
        if sql[:6].lower() == "select":
            result = cursor.fetchall()
            # print(result)
            # print(type(result))
        elif sql[:4].lower() == "show":
            result = cursor.fetchall()
        elif sql[:4].lower() == "desc":
            result = cursor.fetchall()
        else:
            result = None
        conn.commit()
        rsp_data["code"] = 0
        rsp_data["msg"] = None
        rsp_data["data"] = result
        rsp_data["rows"] = count
        # return rsp_data
    except Exception as e:
        msg = ("SQL执行异常：%s" % e)
        rsp_data["code"] = 1
        rsp_data["msg"] = msg
        rsp_data["data"] = None
        rsp_data["rows"] = 0
        # return rsp_data

    finally:
        # print("关闭连接")
        conn.close()
        # print(rsp_data)
        return rsp_data


def get_connection(serverip, port, db_name, account, password):
    """
    @param flat: 0-使用脚本中的ip，1-使用数据库中的ip"""
    print("serverip: ", serverip)
    conn = ms.connect(
        host=serverip,
        port=int(port),
        user=account,
        password=password,
        database=db_name,
        charset="utf8mb4",
        cursorclass=ms.cursors.DictCursor)

    return conn


def get_connection_qadb(db_name):
    """yyw-qa 的数据库"""
    from utils_files import read_json
    datainfo = read_json('yyw-0345', 'mysql')
    # print("datainfo: ",datainfo)
    conn = ms.connect(
        host=datainfo['host'],
        port=int(datainfo['port']),
        user=datainfo['user'],
        password=datainfo['password'],
        database=db_name,
        charset="utf8mb4",
        cursorclass=ms.cursors.DictCursor)

    return conn


def select_from_mysql(conn, sql, total=0, close=False):
    '''select语句
    @param total: 0：全部, 1：返回一条, >1:返回指定的多少条
    @return: rsp_data: code(0-成功，1-失败)'''
    rsp_data = {}
    if sql[:6].lower() != "select":
        rsp_data["code"] = 1
        rsp_data["msg"] = "该方法只支持select语句"
        rsp_data["data"] = None
        rsp_data["rows"] = 0
        return rsp_data

    cursor = conn.cursor()
    try:
        count = cursor.execute(sql)
        if total == 0:
            result = cursor.fetchall()  # list - N条记录
        elif total == 1:
            result = cursor.fetchone()  # tuple - 1条记录
        else:
            result = cursor.fetchmany(total)  # list - total条记录
        conn.commit()
        rsp_data["code"] = 0
        rsp_data["msg"] = None
        rsp_data["data"] = result
        rsp_data["rows"] = count
        # return rsp_data
    except Exception as e:
        msg = ("SQL执行异常：%s" % e)
        rsp_data["code"] = 1
        rsp_data["msg"] = msg
        rsp_data["data"] = None
        rsp_data["rows"] = 0
    finally:
        if close == True:
            print("关闭mysql连接")
            conn.close()
        print('excute mysql code:', rsp_data["code"])
        return rsp_data


def query_mysql2(conn, sql, total=100, close=False):
    """
    @param total: 0：全部, 1：返回一条, >1:返回指定的多少条
    @return: rsp_data{code,msg,data}, code：0-正常，1-异常；
    """
    rsp_data = {}
    try:
        cursor = conn.cursor()
        try:
            count = cursor.execute(sql)
            # result=cursor.fetchall()
            if sql[:6].lower() == "select":
                if total == 0:
                    result = cursor.fetchall()  # list - N条记录
                elif total == 1:
                    result = cursor.fetchone()  # tuple - 1条记录
                else:
                    result = cursor.fetchmany(total)  # list - total条记录
            elif sql[:4].lower() == "show":
                result = cursor.fetchall()
            elif sql[:4].lower() == "desc":
                result = cursor.fetchall()
            else:
                result = None
            conn.commit()
            rsp_data["code"] = 0
            rsp_data["msg"] = None
            rsp_data["data"] = result
            rsp_data["rows"] = count
            # return rsp_data
        except Exception as e:
            msg = ("SQL执行异常：%s" % e)
            rsp_data["code"] = 1
            rsp_data["msg"] = msg
            rsp_data["data"] = None
            rsp_data["rows"] = 0
            # return rsp_data

    finally:
        if close == True:
            print("关闭mysql连接")
            conn.close()
        print('excute mysql code:', rsp_data["code"])
        if rsp_data["code"] == 1:
            print('excute mysql error:', rsp_data["msg"])
        return rsp_data


def query_mysql3(host, user, password, port, database, sql):
    '''执行mysql语句，执行完会关闭连接'''
    rsp_data = {}
    try:
        conn = ms.connect(
            host=host,
            user=user,
            port=port,
            passwd=password,
            database=database,
            charset="utf8mb4",
            cursorclass=ms.cursors.DictCursor
        )
    except Exception as e:
        msg = ("获取数据库连接失败：%s" % e)
        rsp_data["code"] = 1
        rsp_data["msg"] = msg
        rsp_data["data"] = None
        rsp_data["rows"] = 0
        return rsp_data

    try:
        cursor = conn.cursor()
        count = cursor.execute(sql)
        # result=cursor.fetchall()
        if sql[:6].lower() == "select":
            result = cursor.fetchall()
            # print(result)
            # print(type(result))
        elif sql[:4].lower() == "show":
            result = cursor.fetchall()
        elif sql[:4].lower() == "desc":
            result = cursor.fetchall()
        else:
            result = None
        conn.commit()
        rsp_data["code"] = 0
        rsp_data["msg"] = None
        rsp_data["data"] = result
        rsp_data["rows"] = count
        # return rsp_data
    except Exception as e:
        msg = ("SQL执行异常：%s" % e)
        rsp_data["code"] = 1
        rsp_data["msg"] = msg
        rsp_data["data"] = None
        rsp_data["rows"] = 0
        # return rsp_data

    finally:
        print("关闭连接")
        conn.close()
        print(rsp_data)
        return rsp_data


class ZwMysql:
    """
    mysql操作类，实行单例模式
    """
    _instance = None
    _conn = None  # 数据库链接

    def __init__(self, host, user, password, port, db_name):
        ic('开始执行')
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.db_name = db_name
        self._conn = ms.connect(
            host=self.host,
            port=int(self.port),
            user=self.user,
            password=self.password,
            database=self.db_name,
            charset="utf8mb4",
            cursorclass=ms.cursors.DictCursor)

    # def __new__(cls, *args, **kwargs):
    #
    #     if cls._instance is None:
    #         print('已实例化')
    #         _instance = super().__new__(cls)
    #         ic(_instance)
    #     return cls._instance

    def query_mysql(self, sql):
        """执行mysql语句，执行完会关闭连接"""
        rsp_data = {}
        if self._conn is None:
            msg = ("获取数据库连接失败：%s" % e)
            rsp_data["code"] = 1
            rsp_data["msg"] = msg
            rsp_data["data"] = None
            rsp_data["rows"] = 0
            return rsp_data
        try:
            cursor = self.cursor()
            count = cursor.execute(sql)
            # result=cursor.fetchall()
            if sql[:6].lower() == "select":
                result = cursor.fetchall()
                # print(result)
                # print(type(result))
            elif sql[:4].lower() == "show":
                result = cursor.fetchall()
            elif sql[:4].lower() == "desc":
                result = cursor.fetchall()
            else:
                result = None
            self.conn.commit()
            rsp_data["code"] = 0
            rsp_data["msg"] = None
            rsp_data["data"] = result
            rsp_data["rows"] = count
            # return rsp_data
        except Exception as e:
            msg = ("SQL执行异常：%s" % e)
            rsp_data["code"] = 1
            rsp_data["msg"] = msg
            rsp_data["data"] = None
            rsp_data["rows"] = 0
            # return rsp_data

        finally:
            # print("关闭连接")
            self.conn.close()
            # print(rsp_data)
            return rsp_data

    def execute(self, sql, is_close=False):
        """执行mysql语句，执行完不关闭连接
        @param is_close: 是否关闭连接
        """
        rsp_data = {}
        with self._conn.cursor() as cursor:
            count = cursor.execute(sql)
            if sql[:6].lower() == "select":
                result = cursor.fetchall()
                # print(result)
                # print(type(result))
            elif sql[:4].lower() == "show":
                result = cursor.fetchall()
            elif sql[:4].lower() == "desc":
                result = cursor.fetchall()
            else:
                result = None
            self._conn.commit()
            if is_close:
                self._conn.close()
            rsp_data["code"] = 0
            rsp_data["msg"] = None
            rsp_data["data"] = result
            rsp_data["rows"] = count
            return rsp_data

    def close(self):
        """关闭数据库连接"""
        if self._conn:
            self._conn.close()
            self._conn = None


if __name__ == '__main__':
    from icecream import ic
    # sql="UPDATE t_shopping_cart SET check_status = 0 WHERE spu_code !=  '8353YCH20014'"
    # query_mysql("10.6.168.14","b2btest","b5zUoR4JbcK3emhhUxdL",3306,'yihaoyaocheng',sql)
    # res = query_mysql('localhost', 'root', 'root', 3306, 'mydjango', 'select * from auth_group')
    zw = ZwMysql('localhost', 'root', 'root', 3306, 'mydjango')
    ic(zw)
    res2 = zw.execute('select * from auth_group')
    res3 = zw.execute('select * from auth_group')
    zw.close()
    print(res2)
