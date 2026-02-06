---
name: "sql-analyzer"
description: "分析 SQL 语句，解析 SQL 日志，提取完整 SQL 并分析其功能和潜在问题。当用户需要分析 SQL 相关任务时调用。"
---

# SQL 分析技能

## 功能

此技能用于分析 SQL 语句和日志，包括：
- SQL 日志解析：从日志中提取完整的 SQL 语句
- SQL 格式化：美化 SQL 语句，提高可读性
- SQL 功能分析：解释 SQL 的目的和用途
- SQL 问题检测：识别潜在的性能问题和错误
- SQL 优化建议：提供具体的优化方案
- SQL 知识库：管理表结构和 DDL 文件

## 使用场景

当用户需要：
- 解析日志中的 SQL 语句
- 分析 SQL 的功能和用途
- 检测 SQL 中的潜在问题
- 管理和查询 SQL 知识库中的表结构

## 输入

- SQL 日志文本：包含 SQL 语句和参数的日志
- SQL 语句：原始的 SQL 代码
- 表名：需要查询的表结构

## 输出

- 解析后的完整 SQL 语句（带参数值）
- 格式化的 SQL 语句
- SQL 功能说明
- 潜在问题分析
- 表结构信息（从知识库中获取）

## SQL 知识库

SQL 知识库位于 `sql_knowledge/` 目录下，用于保存：
- 表的 DDL 文件（.sql 格式）
- 表结构信息
- 字段说明和约束

### 知识库文件命名规范

```
sql_knowledge/<schema>_<table>.sql
```

例如：
- `sql_knowledge/PAYFUL_BRMS_T_PARAM_RELATION.sql`
- `sql_knowledge/BAOFU_CRM_T_DECISION_FLOW.sql`

## 使用示例

### 解析 SQL 日志

```bash
# 输入 SQL 日志
# SELECT df.DECISION_FLOW_ID AS bizCode, df.DECISION_NAME AS bizDesc FROM PAYFUL_BRMS.T_PARAM_RELATION pr LEFT JOIN PAYFUL_BRMS.T_RULE_DECISION_RELATION rdr on rdr.RULE_ID COLLATE utf8mb4_unicode_ci = pr.BIZ_ID COLLATE utf8mb4_unicode_ci and rdr.STATUS !='delete' LEFT JOIN BAOFU_CRM.T_DECISION_FLOW df on df.DECISION_FLOW_ID COLLATE utf8mb4_unicode_ci = rdr.DECISION_FLOW_ID COLLATE utf8mb4_unicode_ci and df.STATUS !='delete' WHERE pr.STATUS !='delete' AND pr.SCENE = ? AND pr.CODE = ? AND pr.TARGET_SOURCE = ? 
# [2026-01-27 11:42:31.384] [DEBUG] [0db5daf6-b051-496c-8911-81313a182fec] [TID: N/A] c.p.r.c.s.m.P.selectRelation 137  ==> Parameters: DECISION_FLOW(String), PAYEE_NAME(String), metric_center(String)

# 解析后输出
SELECT
  df.DECISION_FLOW_ID AS bizCode,
  df.DECISION_NAME AS bizDesc
FROM PAYFUL_BRMS.T_PARAM_RELATION pr
LEFT JOIN PAYFUL_BRMS.T_RULE_DECISION_RELATION rdr
  ON rdr.RULE_ID COLLATE utf8mb4_unicode_ci = pr.BIZ_ID COLLATE utf8mb4_unicode_ci
  AND rdr.STATUS != 'delete'
LEFT JOIN BAOFU_CRM.T_DECISION_FLOW df
  ON df.DECISION_FLOW_ID COLLATE utf8mb4_unicode_ci = rdr.DECISION_FLOW_ID COLLATE utf8mb4_unicode_ci
  AND df.STATUS != 'delete'
WHERE
  pr.STATUS != 'delete'
  AND pr.SCENE = 'DECISION_FLOW'
  AND pr.CODE = 'PAYEE_NAME'
  AND pr.TARGET_SOURCE = 'metric_center';

# SQL 功能说明
该 SQL 的目的是：
根据一个参数（CODE = 'PAYEE_NAME'），在特定场景（SCENE = 'DECISION_FLOW'）和来源（TARGET_SOURCE = 'metric_center'）下，查找其关联的决策流（Decision Flow）的 ID 和名称。

具体链路如下：
1. 从 参数关联表 T_PARAM_RELATION 中找到符合条件的记录（非删除、指定场景/参数/来源）；
2. 通过 BIZ_ID（此处应为规则 ID）关联到 规则-决策流关系表 T_RULE_DECISION_RELATION；
3. 再通过 DECISION_FLOW_ID 关联到 决策流主表 T_DECISION_FLOW（位于 BAOFU_CRM 库）；
4. 最终返回决策流的编码（bizCode）和名称（bizDesc）。

📌 典型用途：
在指标或参数配置页面，展示“该参数被哪些决策流引用”

# 潜在问题
- 使用了 COLLATE 子句，可能影响查询性能
- 没有使用索引提示，可能导致全表扫描
- 连接条件复杂，可能影响查询效率
```

### 查询 SQL 知识库

```bash
# 查询表结构
# 输入：PAYFUL_BRMS.T_PARAM_RELATION

# 输出：
表结构：PAYFUL_BRMS.T_PARAM_RELATION

字段列表：
- ID: 主键，自增
- SCENE: 场景类型
- CODE: 参数编码
- BIZ_ID: 业务 ID
- TARGET_SOURCE: 目标来源
- STATUS: 状态
- CREATE_TIME: 创建时间
- UPDATE_TIME: 更新时间

索引信息：
- PRIMARY KEY: ID
- INDEX: IDX_SCENE_CODE (SCENE, CODE)

约束条件：
- STATUS 非空，默认 'active'
```

## 最佳实践

- **知识库维护**：定期更新 SQL 知识库中的表结构信息
- **日志格式**：确保 SQL 日志包含完整的 SQL 语句和参数
- **性能分析**：对复杂 SQL 进行性能分析，优化查询效率
- **安全检查**：检测 SQL 注入等安全问题

## 常见问题

### SQL 解析失败
- **解决方法**：确保输入的日志格式正确，包含完整的 SQL 语句和参数

### 知识库中缺少表结构
- **解决方法**：在 `sql_knowledge/` 目录下添加对应的 DDL 文件

### 分析结果不准确
- **解决方法**：提供更完整的 SQL 上下文和表结构信息

## 工具推荐

- **SQL 格式化工具**：sqlformat、Beautify SQL
- **SQL 分析工具**：EXPLAIN ANALYZE、SQL Profiler
- **数据库工具**：MySQL Workbench、DBeaver、Navicat