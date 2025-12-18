import pymysql
from pymysql.cursors import DictCursor
from Kuajing.Common.kjMysql import get_db_config
from datetime import datetime

def delete_user_agreement(userno: int, env: str):
    """
    删除用户签署的协议
    
    :param userno: 用户编号 (USER_NO)
    :param env: 环境名称，如 'FAT', 'UAT'
    :return: 字典，包含操作结果信息
    """
    connection = None
    try:
        # 获取数据库配置
        config = get_db_config(env)
        
        # 建立数据库连接
        connection = pymysql.connect(**config)
        
        with connection.cursor() as cursor:
            # 首先查询该用户的协议记录
            query_sql = """
            SELECT * FROM BAOFU_CBCA.T_USER_AGREEMENT 
            WHERE USER_NO = %s 
            ORDER BY ID DESC 
            LIMIT 1000
            """
            cursor.execute(query_sql, (userno,))
            agreements = cursor.fetchall()
            
            if not agreements:
                print(f"❌ 未找到用户 {userno} 的协议记录")
                return {"success": False, "message": "未找到用户协议记录", "count": 0}
            
            print(f"🔍 找到用户 {userno} 的 {len(agreements)} 条协议记录")
            for i, agreement in enumerate(agreements, 1):
                print(f"   {i}. ID: {agreement['ID']}, 签署流水号: {agreement['SIGN_NO']}, 协议名称: {agreement['AGREEMENT_NAME']}, 状态: {agreement['STATUS']}")
            
            # 执行删除操作
            delete_sql = "DELETE FROM BAOFU_CBCA.T_USER_AGREEMENT WHERE USER_NO = %s"
            affected_rows = cursor.execute(delete_sql, (userno,))
            
            # 提交事务
            connection.commit()
            
            print(f"✅ 成功删除用户 {userno} 的 {affected_rows} 条协议记录")
            
            return {
                "success": True,
                "message": f"成功删除{affected_rows}条协议记录",
                "count": affected_rows,
                "user_no": userno
            }
    
    except Exception as e:
        # 发生错误时回滚事务
        if connection:
            connection.rollback()
        print(f"❌ 删除用户协议失败: {str(e)}")
        return {"success": False, "message": f"删除失败: {str(e)}", "count": 0}
    
    finally:
        # 关闭数据库连接
        if connection:
            connection.close()

if __name__ == "__main__":
    # 删除用户签署的协议
    delete_user_agreement(userno=5181240702000026848, env="UAT")