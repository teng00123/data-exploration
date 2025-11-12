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

 Date: 02/12/2024 11:18:42
*/


-- ----------------------------
-- Table structure for gen_table
-- ----------------------------
DROP TABLE IF EXISTS "public"."gen_table";
CREATE TABLE "public"."gen_table" (
  "table_id" "pg_catalog"."int8" NOT NULL,
  "data_name" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" DEFAULT ''::character varying,
  "table_name" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" DEFAULT ''::character varying,
  "table_comment" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" DEFAULT ''::character varying,
  "sub_table_name" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "sub_table_fk_name" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "class_name" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" DEFAULT ''::character varying,
  "tpl_category" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" DEFAULT 'crud'::character varying,
  "package_name" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "module_name" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "business_name" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "function_name" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "function_author" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "gen_type" "pg_catalog"."bpchar" COLLATE "pg_catalog"."default" DEFAULT '0'::bpchar,
  "gen_path" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" DEFAULT '/'::character varying,
  "options" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "create_dept" "pg_catalog"."int8",
  "create_by" "pg_catalog"."int8",
  "create_time" "pg_catalog"."timestamptz",
  "update_by" "pg_catalog"."int8",
  "update_time" "pg_catalog"."timestamptz",
  "remark" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" DEFAULT NULL::character varying
)
;
COMMENT ON COLUMN "public"."gen_table"."table_id" IS '编号';
COMMENT ON COLUMN "public"."gen_table"."data_name" IS '数据源名称';
COMMENT ON COLUMN "public"."gen_table"."table_name" IS '表名称';
COMMENT ON COLUMN "public"."gen_table"."table_comment" IS '表描述';
COMMENT ON COLUMN "public"."gen_table"."sub_table_name" IS '关联子表的表名';
COMMENT ON COLUMN "public"."gen_table"."sub_table_fk_name" IS '子表关联的外键名';
COMMENT ON COLUMN "public"."gen_table"."class_name" IS '实体类名称';
COMMENT ON COLUMN "public"."gen_table"."tpl_category" IS '使用的模板（crud单表操作 tree树表操作）';
COMMENT ON COLUMN "public"."gen_table"."package_name" IS '生成包路径';
COMMENT ON COLUMN "public"."gen_table"."module_name" IS '生成模块名';
COMMENT ON COLUMN "public"."gen_table"."business_name" IS '生成业务名';
COMMENT ON COLUMN "public"."gen_table"."function_name" IS '生成功能名';
COMMENT ON COLUMN "public"."gen_table"."function_author" IS '生成功能作者';
COMMENT ON COLUMN "public"."gen_table"."gen_type" IS '生成代码方式（0zip压缩包 1自定义路径）';
COMMENT ON COLUMN "public"."gen_table"."gen_path" IS '生成路径（不填默认项目路径）';
COMMENT ON COLUMN "public"."gen_table"."options" IS '其它生成选项';
COMMENT ON COLUMN "public"."gen_table"."create_dept" IS '创建部门';
COMMENT ON COLUMN "public"."gen_table"."create_by" IS '创建者';
COMMENT ON COLUMN "public"."gen_table"."create_time" IS '创建时间';
COMMENT ON COLUMN "public"."gen_table"."update_by" IS '更新者';
COMMENT ON COLUMN "public"."gen_table"."update_time" IS '更新时间';
COMMENT ON COLUMN "public"."gen_table"."remark" IS '备注';
COMMENT ON TABLE "public"."gen_table" IS '代码生成业务表';

-- ----------------------------
-- Primary Key structure for table gen_table
-- ----------------------------
ALTER TABLE "public"."gen_table" ADD CONSTRAINT "gen_table_pkey" PRIMARY KEY ("table_id");
