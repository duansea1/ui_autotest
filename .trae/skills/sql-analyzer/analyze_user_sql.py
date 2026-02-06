import script

# 用户提供的 SQL 日志
user_sql_log = '''SELECT ID, PARAM_TYPE, PARAM_CODE, PARAM_NAME, PARAM_DESC, DATA_TYPE, PARAM_SOURCE, STATUS, CREATE_BY, CREATE_AT, UPDATE_BY, UPDATE_AT, VERSION, REMARKS, REFERENCE_VALUE FROM ( SELECT ID, PARAM_TYPE, PARAM_CODE, PARAM_NAME, PARAM_DESC, DATA_TYPE, PARAM_SOURCE, STATUS, CREATE_BY, CREATE_AT, UPDATE_BY, UPDATE_AT, VERSION, REMARKS, REFERENCE_VALUE FROM PAYFUL_BRMS.T_PARAMETER WHERE PARAM_CODE = ? AND STATUS != 'delete' UNION ALL SELECT mi.ID, 'in' AS PARAM_TYPE, mi.METRIC_CODE AS PARAM_CODE, mi.METRIC_NAME AS PARAM_NAME, mi.REMARKS AS PARAM_DESC, mi.DATA_TYPE, 'metric_center' AS PARAM_SOURCE, 'normal' AS STATUS, si.CREATE_BY, si.CREATE_AT, si.PRO_BY AS UPDATE_BY, si.PRO_AT AS UPDATE_AT, 'v1.0' AS VERSION, si.REMARKS, mi.REFERENCE_VALUE FROM PAYFUL_MCCS.T_METRIC_INFO mi INNER JOIN PAYFUL_MCCS.T_METRIC_SCRIPT_REL msr ON mi.METRIC_CODE = msr.METRIC_CODE INNER JOIN PAYFUL_MCCS.T_SCRIPT_INFO si ON msr.SCRIPT_ID = si.ID AND PRO_STATUS = 'PUBLISHED' WHERE mi.METRIC_CODE = ? ) p LIMIT 1 
 [2026-01-26 13:57:10.892] [DEBUG] [f2ab279d-c60f-4526-a25c-3d2821c54728] [TID: N/A] c.p.r.c.s.m.P.selectByParamCode 137  ==> Parameters: P_IN(String), P_IN(String)'''

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
