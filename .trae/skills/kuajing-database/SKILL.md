---
name: "kuajing-database"
description: "提供跨境支付系统数据库查询的标准引用方式。当用户需要在新增文件中添加数据库链接时，可使用此技能快速引用跨境数据库配置。"
---

# 跨境数据库查询技能

## 功能说明

此技能用于简化跨境支付系统数据库查询的引用过程，提供标准化的数据库连接配置和使用方法。

## 使用场景

当您需要在新增文件中添加数据库链接时，可使用此技能快速引用跨境数据库配置，无需手动查找数据库基本文件。

## 标准引用方式

### 1. 导入数据库模块

在需要使用数据库的文件中，添加以下导入语句：

```python
from Kuajing.Common.kjMysql import execute_db
```

### 2. 环境参数配置

将环境参数提取为可配置变量，推荐放置在文件末尾的示例用法部分：

```python
# 示例用法
if __name__ == "__main__":
    # 可配置参数
    env = 'FAT'  # 数据库环境参数 (FAT/UAT/FAT_DATA)
    # 其他参数...
```

### 3. 数据库操作示例

```python
# 执行查询
sql = "SELECT * FROM table_name WHERE condition = %s"
params = (value,)
result = execute_db(env, sql, params=params)

# 执行更新
sql = "UPDATE table_name SET column = %s WHERE condition = %s"
params = (new_value, condition_value)
affected_rows = execute_db(env, sql, params=params)
```

## 支持的环境

- **FAT**: 测试环境
- **UAT**: 预生产环境
- **FAT_DATA**: 数据仓库环境

## 完整示例

```python
# 导入数据库模块
from Kuajing.Common.kjMysql import execute_db

# 业务逻辑函数
def get_data(env, user_id):
    sql = "SELECT * FROM users WHERE id = %s"
    result = execute_db(env, sql, params=(user_id,))
    return result

# 示例用法
if __name__ == "__main__":
    # 可配置参数
    env = 'FAT'  # 数据库环境参数
    user_id = '123456'
    
    # 测试函数
    data = get_data(env, user_id)
    print(data)
```

## 使用提示

1. 当您需要数据库链接时，只需说："数据库链接，参考【跨境数据库】"
2. 确保环境参数正确设置，根据实际需求选择合适的环境
3. 对于复杂查询，建议使用参数化查询以避免SQL注入风险
4. 所有数据库操作都会自动处理连接的建立和关闭，无需手动管理连接

## 故障排查

- 如果出现数据库连接失败，请检查环境参数是否正确
- 如果出现SQL执行错误，请检查SQL语句是否正确
- 如果需要连接不同的数据库，请在调用execute_db时指定database参数