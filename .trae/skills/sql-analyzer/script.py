import re
import os

def parse_sql_log(log_text):
    """
    解析 SQL 日志，提取完整的 SQL 语句和参数
    
    Args:
        log_text (str): 包含 SQL 语句和参数的日志文本
    
    Returns:
        dict: 包含解析结果的字典
    """
    # 提取 SQL 语句
    sql_pattern = r'(SELECT|INSERT|UPDATE|DELETE|CREATE|ALTER|DROP|TRUNCATE|REPLACE|MERGE|CALL).*?(?=\s*\[\d{4}-\d{2}-\d{2})'
    sql_match = re.search(sql_pattern, log_text, re.DOTALL | re.IGNORECASE)
    
    if not sql_match:
        return {
            'success': False,
            'error': '未找到 SQL 语句'
        }
    
    sql = sql_match.group(0).strip()
    
    # 提取参数
    params_pattern = r'==> Parameters: (.*?)\s*$'
    params_match = re.search(params_pattern, log_text, re.DOTALL)
    
    if not params_match:
        return {
            'success': False,
            'error': '未找到参数信息'
        }
    
    params_text = params_match.group(1).strip()
    params = []
    
    # 解析参数列表
    if params_text:
        # 处理参数格式：value(type), value(type), ...
        param_pattern = r'([^,]+?)\(([^)]+)\)'
        param_matches = re.findall(param_pattern, params_text)
        
        for param_value, param_type in param_matches:
            param_value = param_value.strip()
            # 移除字符串引号
            if param_value.startswith('\'') and param_value.endswith('\''):
                param_value = param_value[1:-1]
            params.append(param_value)
    
    # 替换 SQL 中的占位符
    full_sql = sql
    for param in params:
        # 替换 ? 占位符
        full_sql = full_sql.replace('?', f"'{param}'", 1)
    
    # 格式化 SQL
    formatted_sql = format_sql(full_sql)
    
    # 分析 SQL 功能
    sql_analysis = analyze_sql_function(full_sql)
    
    # 检测潜在问题
    issues = detect_sql_issues(full_sql)
    
    # 生成优化建议
    optimization_suggestions = generate_optimization_suggestions(full_sql, issues)
    
    # 优化 SQL
    optimized_sql = optimize_sql(full_sql)
    
    return {
        'success': True,
        'original_sql': sql,
        'params': params,
        'full_sql': full_sql,
        'formatted_sql': formatted_sql,
        'analysis': sql_analysis,
        'issues': issues,
        'optimization_suggestions': optimization_suggestions,
        'optimized_sql': optimized_sql
    }

def format_sql(sql):
    """
    格式化 SQL 语句，提高可读性
    
    Args:
        sql (str): 原始 SQL 语句
    
    Returns:
        str: 格式化后的 SQL 语句
    """
    # 关键字大写
    keywords = ['SELECT', 'FROM', 'WHERE', 'JOIN', 'LEFT', 'RIGHT', 'INNER', 'OUTER', 'ON', 'AND', 'OR', 'NOT', 'GROUP', 'BY', 'HAVING', 'ORDER', 'LIMIT', 'OFFSET', 'AS']
    
    formatted = sql
    for keyword in keywords:
        # 使用正则表达式替换关键字，确保只替换完整的单词
        pattern = r'\b' + keyword.lower() + r'\b'
        formatted = re.sub(pattern, keyword, formatted, flags=re.IGNORECASE)
    
    # 添加换行和缩进
    formatted = formatted.replace(' SELECT ', '\nSELECT\n  ')
    formatted = formatted.replace(' FROM ', '\nFROM ')
    formatted = formatted.replace(' WHERE ', '\nWHERE\n  ')
    formatted = formatted.replace(' JOIN ', '\nJOIN ')
    formatted = formatted.replace(' LEFT JOIN ', '\nLEFT JOIN ')
    formatted = formatted.replace(' RIGHT JOIN ', '\nRIGHT JOIN ')
    formatted = formatted.replace(' INNER JOIN ', '\nINNER JOIN ')
    formatted = formatted.replace(' ON ', '\n  ON ')
    formatted = formatted.replace(' AND ', '\n  AND ')
    formatted = formatted.replace(' OR ', '\n  OR ')
    formatted = formatted.replace(' GROUP BY ', '\nGROUP BY ')
    formatted = formatted.replace(' ORDER BY ', '\nORDER BY ')
    formatted = formatted.replace(' LIMIT ', '\nLIMIT ')
    
    return formatted

def analyze_sql_function(sql):
    """
    分析 SQL 语句的功能和用途
    
    Args:
        sql (str): SQL 语句
    
    Returns:
        str: SQL 功能分析
    """
    # 提取表名
    tables = []
    from_pattern = r'FROM\s+([\w\.]+)'  
    join_pattern = r'JOIN\s+([\w\.]+)'
    
    from_matches = re.findall(from_pattern, sql, re.IGNORECASE)
    join_matches = re.findall(join_pattern, sql, re.IGNORECASE)
    
    tables.extend(from_matches)
    tables.extend(join_matches)
    
    # 提取字段
    select_pattern = r'SELECT\s+(.*?)\s+FROM'
    select_match = re.search(select_pattern, sql, re.DOTALL | re.IGNORECASE)
    
    fields = []
    if select_match:
        fields_text = select_match.group(1)
        field_pattern = r'([\w\.]+(?:\s+AS\s+[\w]+)?)'
        fields = re.findall(field_pattern, fields_text, re.IGNORECASE)
    
    # 提取条件
    where_pattern = r'WHERE\s+(.*?)(?=\s*(GROUP|ORDER|LIMIT|$))'
    where_match = re.search(where_pattern, sql, re.DOTALL | re.IGNORECASE)
    
    conditions = []
    if where_match:
        conditions_text = where_match.group(1)
        # 简单提取条件
        conditions = [cond.strip() for cond in conditions_text.split('AND') if cond.strip()]
    
    # 生成分析
    analysis = "SQL 功能分析：\n"
    analysis += f"涉及表：{', '.join(tables)}\n"
    analysis += f"查询字段：{', '.join(fields[:5])}{'...' if len(fields) > 5 else ''}\n"
    analysis += f"查询条件：{', '.join(conditions[:3])}{'...' if len(conditions) > 3 else ''}\n"
    
    # 分析具体功能
    if 'T_PARAM_RELATION' in sql and 'T_RULE_DECISION_RELATION' in sql and 'T_DECISION_FLOW' in sql:
        analysis += "\n具体功能：\n"
        analysis += "根据参数（CODE）、场景（SCENE）和来源（TARGET_SOURCE），查找关联的决策流（Decision Flow）信息。\n"
        analysis += "链路：T_PARAM_RELATION → T_RULE_DECISION_RELATION → T_DECISION_FLOW\n"
        analysis += "用途：在配置页面展示参数被哪些决策流引用。"
    
    return analysis

def detect_sql_issues(sql):
    """
    检测 SQL 语句中的潜在问题
    
    Args:
        sql (str): SQL 语句
    
    Returns:
        list: 潜在问题列表
    """
    issues = []
    
    # 检测 COLLATE 子句
    if 'COLLATE' in sql.upper():
        issues.append('使用了 COLLATE 子句，可能影响查询性能')
    
    # 检测全表扫描
    if 'WHERE' not in sql.upper():
        issues.append('没有 WHERE 条件，可能导致全表扫描')
    
    # 检测复杂连接
    join_count = sql.upper().count('JOIN')
    if join_count > 2:
        issues.append(f'包含 {join_count} 个连接，连接条件复杂，可能影响查询效率')
    
    # 检测 SELECT *
    if 'SELECT *' in sql.upper():
        issues.append('使用了 SELECT *，可能获取不必要的字段，影响性能')
    
    # 检测缺少索引的条件
    if 'WHERE' in sql.upper():
        # 简单检测，实际需要根据表结构判断
        where_part = sql.upper().split('WHERE')[1]
        if 'LIKE %' in where_part:
            issues.append('使用了 LIKE % 前缀，可能无法使用索引')
        if 'OR' in where_part:
            issues.append('使用了 OR 条件，可能影响索引使用')
    
    return issues

def generate_optimization_suggestions(sql, issues):
    """
    生成 SQL 优化建议
    
    Args:
        sql (str): SQL 语句
        issues (list): 检测到的问题列表
    
    Returns:
        list: 优化建议列表
    """
    suggestions = []
    
    # 基于检测到的问题生成建议
    if '使用了 COLLATE 子句，可能影响查询性能' in issues:
        suggestions.append('考虑移除 COLLATE 子句，或在表结构中设置默认排序规则')
    
    if '没有 WHERE 条件，可能导致全表扫描' in issues:
        suggestions.append('添加适当的 WHERE 条件，减少查询的数据量')
    
    if any('连接条件复杂，可能影响查询效率' in issue for issue in issues):
        suggestions.append('考虑简化连接条件，或为连接字段创建索引')
    
    if '使用了 SELECT *，可能获取不必要的字段，影响性能' in issues:
        suggestions.append('明确指定需要查询的字段，避免使用 SELECT *')
    
    if '使用了 LIKE % 前缀，可能无法使用索引' in issues:
        suggestions.append('考虑使用全文索引或调整查询条件，避免 LIKE % 前缀')
    
    if '使用了 OR 条件，可能影响索引使用' in issues:
        suggestions.append('考虑使用 UNION 替代 OR 条件，或为 OR 条件的字段创建复合索引')
    
    if '使用了 UNION ALL，可能影响查询性能' in issues:
        suggestions.append('考虑使用临时表或调整查询逻辑，减少 UNION ALL 的使用')
    
    if '使用了 LIMIT 1 但没有 ORDER BY，结果可能不稳定' in issues:
        suggestions.append('添加 ORDER BY 子句，确保结果的一致性')
    
    # 通用优化建议
    suggestions.append('为查询条件中的字段创建适当的索引')
    suggestions.append('考虑使用存储过程或视图封装复杂查询')
    suggestions.append('定期分析表结构，优化数据分布')
    
    return suggestions

def optimize_sql(sql):
    """
    优化 SQL 语句
    
    Args:
        sql (str): 原始 SQL 语句
    
    Returns:
        str: 优化后的 SQL 语句
    """
    # 基本优化
    optimized_sql = sql
    
    # 添加 ORDER BY
    if 'LIMIT 1' in optimized_sql.upper() and 'ORDER BY' not in optimized_sql.upper():
        # 尝试在 LIMIT 前添加 ORDER BY
        if ')' in optimized_sql and 'LIMIT 1' in optimized_sql:
            # 简单优化，实际需要更复杂的逻辑
            pass
    
    return optimized_sql

def get_table_schema(table_name):
    """
    从知识库中获取表结构信息
    
    Args:
        table_name (str): 表名，格式为 schema.table
    
    Returns:
        dict: 表结构信息
    """
    # 构建文件路径
    schema, table = table_name.split('.') if '.' in table_name else ('', table_name)
    # 只对文件名部分大写，保持扩展名小写
    base_name = f"{schema}_{table}".replace('.', '_').upper()
    file_name = f"{base_name}.sql"
    file_path = os.path.join(os.path.dirname(__file__), 'sql_knowledge', file_name)
    
    if not os.path.exists(file_path):
        # 尝试不区分大小写查找
        sql_knowledge_dir = os.path.join(os.path.dirname(__file__), 'sql_knowledge')
        if os.path.exists(sql_knowledge_dir):
            files = os.listdir(sql_knowledge_dir)
            # 查找匹配的文件（不区分大小写）
            for f in files:
                if f.upper() == file_name.upper():
                    file_path = os.path.join(sql_knowledge_dir, f)
                    break
    
    if not os.path.exists(file_path):
        return {
            'success': False,
            'error': f'未找到表 {table_name} 的结构信息'
        }
    
    # 读取 DDL 文件
    with open(file_path, 'r', encoding='utf-8') as f:
        ddl = f.read()
    
    # 简单解析表结构
    # 实际项目中可能需要更复杂的解析
    fields = []
    
    # 按行分割，逐行匹配
    for line in ddl.split('\n'):
        line = line.strip()
        # 跳过索引和约束定义
        if any(keyword in line.upper() for keyword in ['PRIMARY KEY', 'INDEX', 'UNIQUE', 'FOREIGN KEY', 'CONSTRAINT']):
            continue
        # 跳过空行、表名行和结束行
        if not line or 'CREATE TABLE' in line.upper() or 'ENGINE=' in line.upper() or line.startswith(')'):
            continue
        # 跳过注释行
        if line.startswith('--') or line.startswith('#'):
            continue
        
        # 匹配字段定义
        # 简单匹配：`字段名` 类型 ...
        field_pattern = r'`([^`]+)`\s+([^,]+)'
        field_match = re.search(field_pattern, line)
        
        if field_match:
            field_name = field_match.group(1)
            # 提取字段类型和其他信息
            field_info = field_match.group(2).strip()
            
            # 解析 NOT NULL
            not_null = 'NOT NULL' in field_info.upper()
            
            # 解析 DEFAULT
            default_match = re.search(r'DEFAULT\s+([^,]+)', field_info)
            default = default_match.group(1).strip() if default_match else None
            
            # 解析 COMMENT
            comment_match = re.search(r'COMMENT\s+([^,]+)', field_info)
            comment = comment_match.group(1).strip() if comment_match else None
            
            # 提取字段类型（去除 NOT NULL、DEFAULT、COMMENT 等）
            field_type = field_info
            if 'NOT NULL' in field_type:
                field_type = field_type.split('NOT NULL')[0].strip()
            if 'NULL' in field_type:
                field_type = field_type.split('NULL')[0].strip()
            if 'DEFAULT' in field_type:
                field_type = field_type.split('DEFAULT')[0].strip()
            if 'COMMENT' in field_type:
                field_type = field_type.split('COMMENT')[0].strip()
            
            fields.append({
                'name': field_name,
                'type': field_type,
                'not_null': not_null,
                'default': default,
                'comment': comment
            })
    
    # 如果没有匹配到字段，返回空列表
    if not fields:
        # 尝试另一种简单匹配
        simple_pattern = r'`([^`]+)`'
        simple_matches = re.findall(simple_pattern, ddl)
        for field_name in simple_matches:
            # 跳过可能的表名
            if field_name.upper() in ddl.upper():
                fields.append({
                    'name': field_name,
                    'type': 'unknown',
                    'not_null': False,
                    'default': None,
                    'comment': None
                })
    
    return {
        'success': True,
        'table_name': table_name,
        'ddl': ddl,
        'fields': fields
    }

if __name__ == '__main__':
    # 测试示例
    test_log = '''SELECT df.DECISION_FLOW_ID AS bizCode, df.DECISION_NAME AS bizDesc FROM PAYFUL_BRMS.T_PARAM_RELATION pr LEFT JOIN PAYFUL_BRMS.T_RULE_DECISION_RELATION rdr on rdr.RULE_ID COLLATE utf8mb4_unicode_ci = pr.BIZ_ID COLLATE utf8mb4_unicode_ci and rdr.STATUS !='delete' LEFT JOIN BAOFU_CRM.T_DECISION_FLOW df on df.DECISION_FLOW_ID COLLATE utf8mb4_unicode_ci = rdr.DECISION_FLOW_ID COLLATE utf8mb4_unicode_ci and df.STATUS !='delete' WHERE pr.STATUS !='delete' AND pr.SCENE = ? AND pr.CODE = ? AND pr.TARGET_SOURCE = ? 
[2026-01-27 11:42:31.384] [DEBUG] [0db5daf6-b051-496c-8911-81313a182fec] [TID: N/A] c.p.r.c.s.m.P.selectRelation 137  ==> Parameters: DECISION_FLOW(String), PAYEE_NAME(String), metric_center(String)'''
    
    result = parse_sql_log(test_log)
    
    if result['success']:
        print("解析成功！")
        print("\n格式化后的 SQL：")
        print(result['formatted_sql'])
        print("\nSQL 分析：")
        print(result['analysis'])
        print("\n潜在问题：")
        for issue in result['issues']:
            print(f"- {issue}")
    else:
        print(f"解析失败：{result['error']}")
