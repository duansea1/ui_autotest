"""
@Author    : duansea
@Date      : 2025/8/27 10:46
@Description: [B2B权限配置]
"""
from Kuajing.Common.kjMysql import get_db_config
import pymysql
from pymysql.cursors import DictCursor

# 定义平台对应的 role_type 值
PLATFORM_ROLE_TYPE = {
    'b2b': 202508071326000001,
    'gep': 202105311518000001
}


def get_user_menu_permissions(userno: str, platform: str, env: str = 'FAT', role_name: str = None):
    """
    获取指定用户在 B2B 或 GEP 平台下的菜单权限（resource_name, resource_url），可选择限定角色名称

    :param userno: 用户编号，用于匹配 t_role.parent_no，必须传入
    :param platform: 平台类型 'b2b' 或 'gep'，必须传入
    :param env: 环境 'FAT' 或 'UAT'
    :param role_name: 角色名称，用于匹配 t_role.role_name，传入则查询该用户下指定角色的权限，未传入则查询该用户所有角色的权限
    :return: dict 包含权限数量和权限列表
    """
    # 获取数据库配置
    db_config = get_db_config(env)

    # 校验参数
    if not userno or not platform:
        raise ValueError("必须指定userno和platform")
    if platform not in PLATFORM_ROLE_TYPE:
        raise ValueError("platform must be 'b2b' or 'gep'")
    role_type = PLATFORM_ROLE_TYPE[platform]

    connection = None
    try:
        connection = pymysql.connect(**db_config)
        with connection.cursor() as cursor:
            # Step 1: 查询角色信息
            if role_name:
                # 根据userno、role_name和platform查询角色
                sql_role = """
                    SELECT role_id, role_name
                    FROM BAOFU_CBPM.t_role
                    WHERE parent_no = %s
                      AND role_name = %s
                      AND role_type = %s
                      AND is_delete = 0
                      AND enabled = 1
                """
                cursor.execute(sql_role, (userno, role_name, role_type))
                roles = cursor.fetchall()
                if not roles:
                    print(f"未找到 userno={userno} 在 {platform.upper()} 端对应的 role_name={role_name} 有效角色")
                    return {
                        "userno": userno,
                        "role_name": role_name,
                        "platform": platform.upper(),
                        "total_permissions": 0,
                        "permissions": []
                    }
                print(f"找到角色: {[(r['role_id'], r['role_name']) for r in roles]}")
            else:
                # 原逻辑：根据userno查询角色
                sql_role = """
                    SELECT role_id, role_name
                    FROM BAOFU_CBPM.t_role
                    WHERE parent_no = %s
                      AND role_type = %s
                      AND is_delete = 0
                      AND enabled = 1
                """
                cursor.execute(sql_role, (userno, role_type))
                roles = cursor.fetchall()

            if not roles:
                print(f"未找到 userno={userno} 在 {platform.upper()} 端对应的有效角色")
                return {
                    "userno": userno,
                    "platform": platform.upper(),
                    "total_permissions": 0,
                    "permissions": []
                }

            # 收集所有 role_id
            role_ids = [role['role_id'] for role in roles]
            if not role_name:
                print(f"找到 {len(roles)} 个角色: {[(r['role_id'], r['role_name']) for r in roles]}")

            # Step 2: 查询这些 role_id 对应的未禁用的 resource_id（去重）
            placeholders = ','.join(['%s'] * len(role_ids))
            sql_role_resource = f"""
                SELECT DISTINCT rr.resource_id
                FROM BAOFU_CBPM.t_role__resource rr
                WHERE rr.role_id IN ({placeholders})
                  AND rr.enabled = 1
                  AND rr.is_delete = 0  -- 注意：表结构未提供 is_delete 字段，如果实际存在需启用
            """
            # 如果 t_role__resource 没有 is_delete 字段，请移除该条件
            # 假设该表没有 is_delete 字段，则只判断 enabled
            sql_role_resource = f"""
                SELECT DISTINCT rr.resource_id
                FROM BAOFU_CBPM.t_role__resource rr
                WHERE rr.role_id IN ({placeholders})
                  AND rr.enabled = 1
            """
            cursor.execute(sql_role_resource, role_ids)
            resource_ids_result = cursor.fetchall()
            resource_ids = [item['resource_id'] for item in resource_ids_result]

            if not resource_ids:
                print(f"角色未绑定任何启用的资源")
                return {
                    "userno": userno,
                    "platform": platform,
                    "total_permissions": 0,
                    "permissions": []
                }

            print(f"关联到 {len(resource_ids)} 个 resource_id")

            # Step 3: 查询 resource_id 对应的 resource_name 和 resource_url
            r_placeholders = ','.join(['%s'] * len(resource_ids))
            sql_resource = f"""
                SELECT resource_name, resource_url
                FROM BAOFU_CBPM.t_resource
                WHERE resource_id IN ({r_placeholders})
                  AND is_delete = 0
                  AND enabled = 1
            """
            cursor.execute(sql_resource, resource_ids)
            resources = cursor.fetchall()

            # 构造返回结果
            permission_list = [
                {"resource_name": res['resource_name'], "resource_url": res['resource_url']}
                for res in resources
            ]

            # 构造返回结果
            if role_name:
                result = {
                    "userno": userno,
                    "role_name": role_name,
                    "platform": platform.upper(),
                    "total_permissions": len(permission_list),
                    "permissions": permission_list
                }
            else:
                result = {
                    "userno": userno,
                    "platform": platform.upper(),
                    "total_permissions": len(permission_list),
                    "permissions": permission_list
                }

            # 打印权限信息
            print(f"\n=== {platform.upper()} 端菜单权限 ===")
            for item in permission_list:
                print(f"菜单: {item['resource_name']} -> URL: {item['resource_url']}")
            
            if role_name:
                print(f"✅{userno}-{role_name}-{platform.upper()}端,总计: {len(permission_list)} 个权限\n")
            else:
                print(f"✅{userno}-{platform.upper()}端,总计: {len(permission_list)} 个权限\n")

            return result

    except Exception as e:
        print(f"查询过程中发生错误: {e}")
        raise
    finally:
        if connection:
            connection.close()


# ============= 使用示例 =============
if __name__ == "__main__":
    userno = "5181240821000008798"  # 替换为实际的 userno
    env = "FAT"  # 或 "UAT"
    
    # ==== 示例1: 通过用户编号查询权限（原有功能） ====
    # # 查询 B2B 端权限
    # result_b2b = get_user_menu_permissions(userno, platform='b2b', env=env)

    # # 查询 GEP 端权限
    # result_gep = get_user_menu_permissions(userno, platform='gep', env=env)
    
    # ==== 示例2: 通过角色名称查询权限（新增功能） ====
    # 注意：这里需要替换为实际存在的角色名称
    # 查询 B2B 端指定角色的权限  role_name='B2B端-只有一个菜单角色'
    result_b2b_by_role = get_user_menu_permissions(userno,platform='b2b', env=env, role_name='')
    
    # 查询 GEP 端指定角色的权限
    # result_gep_by_role = get_user_menu_permissions(userno, platform='gep', env=env, role_name='GEP端角色名称')