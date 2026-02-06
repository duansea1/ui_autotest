/*
 Navicat Premium Dump SQL

 Source Server         : 跨境-Fat环境
 Source Server Type    : MySQL
 Source Server Version : 50721 (5.7.21-log)
 Source Host           : 10.0.19.206:3306
 Source Schema         : PAYFUL_MCCS

 Target Server Type    : MySQL
 Target Server Version : 50721 (5.7.21-log)
 File Encoding         : 65001

 Date: 03/02/2026 10:35:23
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for T_METRIC_GROUP
-- ----------------------------
DROP TABLE IF EXISTS `T_METRIC_GROUP`;
CREATE TABLE `T_METRIC_GROUP`  (
  `ID` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '分组ID',
  `GROUP_CODE` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '分组代码',
  `GROUP_NAME` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '分组名称',
  `REMARKS` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `DELETE_FLAG` tinyint(1) NULL DEFAULT 0,
  `CREATE_AT` timestamp NOT NULL,
  `CREATE_BY` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `UPDATE_AT` timestamp NULL DEFAULT NULL,
  `UPDATE_BY` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`ID`) USING BTREE,
  UNIQUE INDEX `UNIQUE_GROUP_CODE`(`GROUP_CODE`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 30 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '指标分组表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for T_METRIC_GROUP_REL
-- ----------------------------
DROP TABLE IF EXISTS `T_METRIC_GROUP_REL`;
CREATE TABLE `T_METRIC_GROUP_REL`  (
  `ID` bigint(20) NOT NULL AUTO_INCREMENT,
  `METRIC_CODE` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '指标代码',
  `GROUP_CODE` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '分组代码',
  `STATUS` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '状态',
  `REMARKS` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `DELETE_FLAG` tinyint(1) NOT NULL DEFAULT 0,
  `CREATE_AT` timestamp NOT NULL,
  `CREATE_BY` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `UPDATE_AT` timestamp NULL DEFAULT NULL,
  `UPDATE_BY` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`ID`) USING BTREE,
  UNIQUE INDEX `UNIQ_CODE`(`METRIC_CODE`, `GROUP_CODE`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 185 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '指标分组关系表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for T_METRIC_GROUP_ROLE
-- ----------------------------
DROP TABLE IF EXISTS `T_METRIC_GROUP_ROLE`;
CREATE TABLE `T_METRIC_GROUP_ROLE`  (
  `ID` bigint(20) NOT NULL AUTO_INCREMENT,
  `GROUP_CODE` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '分组CODE',
  `ROLE_TYPE` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '角色类型',
  `ROLE_ID` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '角色ID',
  `REMARKS` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `DELETE_FLAG` tinyint(1) NOT NULL DEFAULT 0,
  `CREATE_AT` timestamp NULL DEFAULT NULL,
  `CREATE_BY` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `UPDATE_AT` timestamp NULL DEFAULT NULL,
  `UPDATE_BY` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`ID`) USING BTREE,
  UNIQUE INDEX `UNIQUE_ROLE`(`GROUP_CODE`, `ROLE_TYPE`, `ROLE_ID`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 212 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '指标分组角色' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for T_METRIC_INFO
-- ----------------------------
DROP TABLE IF EXISTS `T_METRIC_INFO`;
CREATE TABLE `T_METRIC_INFO`  (
  `ID` bigint(20) NOT NULL AUTO_INCREMENT,
  `METRIC_CODE` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '指标代码',
  `METRIC_NAME` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '指标名称',
  `METRIC_TYPE` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '归属类型',
  `DATA_TYPE` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '数据类型',
  `REFERENCE_VALUE` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '参考值',
  `REMARKS` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `CREATE_AT` timestamp NOT NULL,
  `CREATE_BY` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `UPDATE_AT` timestamp NULL DEFAULT NULL,
  `UPDATE_BY` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`ID`) USING BTREE,
  UNIQUE INDEX `IDX_METIRC_CODE`(`METRIC_CODE`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 66 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '指标信息表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for T_METRIC_REQUEST_LOG
-- ----------------------------
DROP TABLE IF EXISTS `T_METRIC_REQUEST_LOG`;
CREATE TABLE `T_METRIC_REQUEST_LOG`  (
  `ID` bigint(20) NOT NULL AUTO_INCREMENT,
  `REQUEST_ID` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '请求ID',
  `REQUEST_BY` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '请求方',
  `REQUEST_AT` timestamp NOT NULL COMMENT '请求时间',
  `REQUEST_REASON` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '请求原因',
  `REQUEST_CODES` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '请求CODE',
  `REQUEST_PARAMS` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '请求参数',
  `RUN_SCRIPT` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '执行脚本',
  `RUN_RESULT` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '执行结果',
  `RUN_TIME` int(11) NULL DEFAULT NULL COMMENT '执行耗时',
  `RUN_IP` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '执行IP',
  `REMARKS` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `CREATE_AT` timestamp NOT NULL,
  `CREATE_BY` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  PRIMARY KEY (`ID`) USING BTREE,
  INDEX `IDX_RUN_IP`(`RUN_IP`) USING BTREE,
  INDEX `IDX_REQUEST_ID`(`REQUEST_ID`) USING BTREE,
  INDEX `IDX_REQUEST_AT`(`REQUEST_AT`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5961 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '指标调用履历表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for T_METRIC_SCRIPT_REL
-- ----------------------------
DROP TABLE IF EXISTS `T_METRIC_SCRIPT_REL`;
CREATE TABLE `T_METRIC_SCRIPT_REL`  (
  `ID` bigint(20) NOT NULL AUTO_INCREMENT,
  `METRIC_CODE` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '指标CODE',
  `SCRIPT_ID` bigint(20) NOT NULL COMMENT '脚本ID',
  `STATUS` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '状态',
  `REMARKS` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `DELETE_FLAG` tinyint(1) NOT NULL DEFAULT 0,
  `CREATE_AT` timestamp NOT NULL,
  `CREATE_BY` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `UPDATE_AT` timestamp NULL DEFAULT NULL,
  `UPDATE_BY` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`ID`) USING BTREE,
  UNIQUE INDEX `UNIQUE_METRIC_CODE`(`METRIC_CODE`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 76 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '指标脚本关系表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for T_PARAM_INFO
-- ----------------------------
DROP TABLE IF EXISTS `T_PARAM_INFO`;
CREATE TABLE `T_PARAM_INFO`  (
  `ID` bigint(20) NOT NULL AUTO_INCREMENT,
  `PARAM_CODE` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '参数CODE',
  `PARAM_NAME` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '参数名称',
  `REMARKS` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `DELETE_FLAG` tinyint(1) NULL DEFAULT 0,
  `CREATE_AT` timestamp NOT NULL,
  `CREATE_BY` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `UPDATE_AT` timestamp NULL DEFAULT NULL,
  `UPDATE_BY` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`ID`) USING BTREE,
  UNIQUE INDEX `IDX_PARAM_CODE`(`PARAM_CODE`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 33 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '入参信息表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for T_SCRIPT_INFO
-- ----------------------------
DROP TABLE IF EXISTS `T_SCRIPT_INFO`;
CREATE TABLE `T_SCRIPT_INFO`  (
  `ID` bigint(20) NOT NULL AUTO_INCREMENT,
  `SCRIPT_TYPE` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '脚本类型',
  `MODULAR_FLAG` varchar(5) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '是否模块化',
  `MODULAR_CODE` varchar(128) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '所属模块代码',
  `DEV_STATUS` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '开发状态',
  `DEV_VERSION` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '开发版本号',
  `DEV_BY` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '开发人',
  `DEV_AT` timestamp NULL DEFAULT NULL COMMENT '开发时间',
  `DEV_SCRIPT` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '开发脚本内容',
  `DEV_DATA_SOURCE` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '开发数据源',
  `TEST_BY` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '测试人',
  `TEST_AT` timestamp NULL DEFAULT NULL COMMENT '测试时间',
  `PRO_STATUS` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '发布状态',
  `PRO_VERSION` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '发布版本号',
  `PRO_BY` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '发布人',
  `PRO_AT` timestamp NULL DEFAULT NULL COMMENT '发布时间',
  `PRO_SCRIPT` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '发布脚本内容',
  `PRO_DATA_SOURCE` varchar(32) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '发布数据源',
  `REMARKS` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `CREATE_AT` timestamp NOT NULL,
  `CREATE_BY` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `UPDATE_AT` timestamp NULL DEFAULT NULL,
  `UPDATE_BY` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`ID`) USING BTREE,
  INDEX `IDX_MODULAR`(`MODULAR_FLAG`, `MODULAR_CODE`) USING BTREE,
  INDEX `IDX_PRO`(`PRO_BY`, `PRO_AT`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 53 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '脚本信息表' ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for T_SCRIPT_LOG
-- ----------------------------
DROP TABLE IF EXISTS `T_SCRIPT_LOG`;
CREATE TABLE `T_SCRIPT_LOG`  (
  `ID` bigint(20) NOT NULL AUTO_INCREMENT,
  `SCRIPT_ID` bigint(20) NOT NULL COMMENT '脚本ID',
  `VERSION` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '版本号',
  `OP_TYPE` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '操作类型',
  `OP_CONTENT` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '更新内容',
  `OP_BY` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL COMMENT '更新人',
  `OP_AT` timestamp NOT NULL COMMENT '更新时间',
  `SCRIPT_CONTENT` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL COMMENT '脚本内容',
  `REMARKS` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL COMMENT '备注',
  `CREATE_AT` timestamp NOT NULL,
  PRIMARY KEY (`ID`) USING BTREE,
  INDEX `IDX_SCRIPT_ID`(`SCRIPT_ID`) USING BTREE,
  INDEX `IDX_OP`(`OP_BY`, `OP_AT`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 625 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci COMMENT = '脚本履历表' ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
