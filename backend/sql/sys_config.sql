/*
 Navicat Premium Data Transfer

 Source Server         : 192.168.20.48
 Source Server Type    : PostgreSQL
 Source Server Version : 160004
 Source Host           : 192.168.20.48:5432
 Source Catalog        : bsp-user
 Source Schema         : public

 Target Server Type    : PostgreSQL
 Target Server Version : 160004
 File Encoding         : 65001

 Date: 02/12/2024 11:18:59
*/


-- ----------------------------
-- Table structure for sys_config
-- ----------------------------
DROP TABLE IF EXISTS "public"."sys_config";
CREATE TABLE "public"."sys_config" (
  "config_id" "pg_catalog"."int8" NOT NULL,
  "tenant_id" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" DEFAULT '000000'::character varying,
  "config_name" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" DEFAULT ''::character varying,
  "config_key" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" DEFAULT ''::character varying,
  "config_value" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" DEFAULT ''::character varying,
  "config_type" "pg_catalog"."bpchar" COLLATE "pg_catalog"."default" DEFAULT 'N'::bpchar,
  "create_dept" "pg_catalog"."int8",
  "create_by" "pg_catalog"."int8",
  "create_time" "pg_catalog"."timestamptz",
  "update_by" "pg_catalog"."int8",
  "update_time" "pg_catalog"."timestamptz",
  "remark" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" DEFAULT NULL::character varying
)
;
COMMENT ON COLUMN "public"."sys_config"."config_id" IS '参数主键';
COMMENT ON COLUMN "public"."sys_config"."tenant_id" IS '租户编号';
COMMENT ON COLUMN "public"."sys_config"."config_name" IS '参数名称';
COMMENT ON COLUMN "public"."sys_config"."config_key" IS '参数键名';
COMMENT ON COLUMN "public"."sys_config"."config_value" IS '参数键值';
COMMENT ON COLUMN "public"."sys_config"."config_type" IS '系统内置（Y是 N否）';
COMMENT ON COLUMN "public"."sys_config"."create_dept" IS '创建部门';
COMMENT ON COLUMN "public"."sys_config"."create_by" IS '创建者';
COMMENT ON COLUMN "public"."sys_config"."create_time" IS '创建时间';
COMMENT ON COLUMN "public"."sys_config"."update_by" IS '更新者';
COMMENT ON COLUMN "public"."sys_config"."update_time" IS '更新时间';
COMMENT ON COLUMN "public"."sys_config"."remark" IS '备注';
COMMENT ON TABLE "public"."sys_config" IS '参数配置表';

-- ----------------------------
-- Primary Key structure for table sys_config
-- ----------------------------
ALTER TABLE "public"."sys_config" ADD CONSTRAINT "sys_config_pkey" PRIMARY KEY ("config_id");
