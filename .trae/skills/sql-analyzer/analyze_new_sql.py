import script

# 用户提供的新 SQL 日志
user_sql_log = '''SELECT p.PARAM_TYPE AS paramType, p.PARAM_CODE AS paramCode, p.PARAM_NAME AS paramName, p.PARAM_DESC AS paramDesc, p.DATA_TYPE AS dataType, p.PARAM_SOURCE AS paramSource, p.STATUS AS status, p.CREATE_BY AS createBy, p.CREATE_AT AS createAt, p.UPDATE_BY AS updateBy, p.UPDATE_AT AS updateAt, p.VERSION AS version, p.REMARKS AS remarks, p.REFERENCE_VALUE as referenceValue FROM ( SELECT PARAM_TYPE, PARAM_CODE, PARAM_NAME, PARAM_DESC, DATA_TYPE, PARAM_SOURCE, STATUS, CREATE_BY, CREATE_AT, UPDATE_BY, UPDATE_AT, VERSION, REMARKS, REFERENCE_VALUE FROM PAYFUL_BRMS.T_PARAMETER UNION ALL SELECT 'in' AS PARAM_TYPE, METRIC_CODE AS PARAM_CODE, METRIC_NAME AS PARAM_NAME, '' AS PARAM_DESC, DATA_TYPE, 'metric_center' AS PARAM_SOURCE, 'normal' AS STATUS, CREATE_BY, CREATE_AT, UPDATE_BY, UPDATE_AT, 'v1.0' AS VERSION, REMARKS, REFERENCE_VALUE FROM PAYFUL_MCCS.T_METRIC_INFO )p LEFT JOIN PAYFUL_BRMS.T_PARAM_RELATION pr on p.PARAM_CODE = pr.CODE and pr.STATUS != 'delete' WHERE p.STATUS != 'delete' ORDER BY p.CREATE_AT DESC LIMIT ? 
 [2026-01-20 16:47:51.928] [DEBUG] [be5e25b7-c2be-42d5-81d7-6588e9e4ae8b] [TID: N/A] c.p.r.c.s.m.P.selectPage 137  ==> Parameters: 10(Integer)'''

# 解析 SQL 日志
print("解析 SQL 日志...")
result = script.parse_sql_log(user_sql_log)

if result['success']:
    print("\n解析成功！")
    print("\n格式化后的 SQL：")
    print(result['formatted_sql'])
    print("\nSQL 功能分析：")
    print(result['analysis'])
    print("\n潜在问题：")
    for issue in result['issues']:
        print(f"- {issue}")
    
    # 输出优化建议
    print("\n优化建议：")
    for suggestion in result.get('optimization_suggestions', []):
        print(f"- {suggestion}")
    
    # 询问用户是否需要优化的 SQL
    print("\n检测到上述问题，是否需要提供优化后的 SQL？(y/n)")
    user_input = input().strip().lower()
    
    if user_input == 'y':
        print("\n优化后的 SQL：")
        # 这里可以进一步优化 SQL，目前使用基本优化
        optimized_sql = result.get('optimized_sql', result['formatted_sql'])
        print(optimized_sql)
    else:
        print("\n已取消优化 SQL 的请求。")
else:
    print(f"解析失败：{result['error']}")
