import script

# 测试获取表结构
print("测试获取表结构...")

# 测试 PAYFUL_BRMS.T_PARAM_RELATION
result1 = script.get_table_schema('PAYFUL_BRMS.T_PARAM_RELATION')
print("\n1. PAYFUL_BRMS.T_PARAM_RELATION 表结构：")
if result1['success']:
    print(f"表名：{result1['table_name']}")
    print("字段列表：")
    for field in result1['fields']:
        print(f"- {field['name']}: {field['type']} {'NOT NULL' if field['not_null'] else 'NULL'} {'DEFAULT ' + field['default'] if field['default'] else ''} {'COMMENT ' + field['comment'] if field['comment'] else ''}")
else:
    print(f"错误：{result1['error']}")

# 测试 BAOFU_CRM.T_DECISION_FLOW
result2 = script.get_table_schema('BAOFU_CRM.T_DECISION_FLOW')
print("\n2. BAOFU_CRM.T_DECISION_FLOW 表结构：")
if result2['success']:
    print(f"表名：{result2['table_name']}")
    print("字段列表：")
    for field in result2['fields']:
        print(f"- {field['name']}: {field['type']} {'NOT NULL' if field['not_null'] else 'NULL'} {'DEFAULT ' + field['default'] if field['default'] else ''} {'COMMENT ' + field['comment'] if field['comment'] else ''}")
else:
    print(f"错误：{result2['error']}")

# 测试不存在的表
result3 = script.get_table_schema('NON_EXISTENT.TABLE')
print("\n3. 不存在的表：")
if result3['success']:
    print(f"表名：{result3['table_name']}")
else:
    print(f"错误：{result3['error']}")
