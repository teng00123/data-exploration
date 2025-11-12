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

 Date: 02/12/2024 11:18:47
*/


-- ----------------------------
-- Table structure for gen_table_column
-- ----------------------------
DROP TABLE IF EXISTS "public"."gen_table_column";
CREATE TABLE "public"."gen_table_column" (
  "column_id" "pg_catalog"."int8" NOT NULL,
  "table_id" "pg_catalog"."int8",
  "column_name" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "column_comment" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "column_type" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "java_type" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "java_field" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "is_pk" "pg_catalog"."bpchar" COLLATE "pg_catalog"."default" DEFAULT NULL::bpchar,
  "is_increment" "pg_catalog"."bpchar" COLLATE "pg_catalog"."default" DEFAULT NULL::bpchar,
  "is_required" "pg_catalog"."bpchar" COLLATE "pg_catalog"."default" DEFAULT NULL::bpchar,
  "is_insert" "pg_catalog"."bpchar" COLLATE "pg_catalog"."default" DEFAULT NULL::bpchar,
  "is_edit" "pg_catalog"."bpchar" COLLATE "pg_catalog"."default" DEFAULT NULL::bpchar,
  "is_list" "pg_catalog"."bpchar" COLLATE "pg_catalog"."default" DEFAULT NULL::bpchar,
  "is_query" "pg_catalog"."bpchar" COLLATE "pg_catalog"."default" DEFAULT NULL::bpchar,
  "query_type" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" DEFAULT 'EQ'::character varying,
  "html_type" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "dict_type" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" DEFAULT ''::character varying,
  "sort" "pg_catalog"."int4",
  "create_dept" "pg_catalog"."int8",
  "create_by" "pg_catalog"."int8",
  "create_time" "pg_catalog"."timestamptz",
  "update_by" "pg_catalog"."int8",
  "update_time" "pg_catalog"."timestamptz"
)
;
COMMENT ON COLUMN "public"."gen_table_column"."column_id" IS '编号';
COMMENT ON COLUMN "public"."gen_table_column"."table_id" IS '归属表编号';
COMMENT ON COLUMN "public"."gen_table_column"."column_name" IS '列名称';
COMMENT ON COLUMN "public"."gen_table_column"."column_comment" IS '列描述';
COMMENT ON COLUMN "public"."gen_table_column"."column_type" IS '列类型';
COMMENT ON COLUMN "public"."gen_table_column"."java_type" IS 'JAVA类型';
COMMENT ON COLUMN "public"."gen_table_column"."java_field" IS 'JAVA字段名';
COMMENT ON COLUMN "public"."gen_table_column"."is_pk" IS '是否主键（1是）';
COMMENT ON COLUMN "public"."gen_table_column"."is_increment" IS '是否自增（1是）';
COMMENT ON COLUMN "public"."gen_table_column"."is_required" IS '是否必填（1是）';
COMMENT ON COLUMN "public"."gen_table_column"."is_insert" IS '是否为插入字段（1是）';
COMMENT ON COLUMN "public"."gen_table_column"."is_edit" IS '是否编辑字段（1是）';
COMMENT ON COLUMN "public"."gen_table_column"."is_list" IS '是否列表字段（1是）';
COMMENT ON COLUMN "public"."gen_table_column"."is_query" IS '是否查询字段（1是）';
COMMENT ON COLUMN "public"."gen_table_column"."query_type" IS '查询方式（等于、不等于、大于、小于、范围）';
COMMENT ON COLUMN "public"."gen_table_column"."html_type" IS '显示类型（文本框、文本域、下拉框、复选框、单选框、日期控件）';
COMMENT ON COLUMN "public"."gen_table_column"."dict_type" IS '字典类型';
COMMENT ON COLUMN "public"."gen_table_column"."sort" IS '排序';
COMMENT ON COLUMN "public"."gen_table_column"."create_dept" IS '创建部门';
COMMENT ON COLUMN "public"."gen_table_column"."create_by" IS '创建者';
COMMENT ON COLUMN "public"."gen_table_column"."create_time" IS '创建时间';
COMMENT ON COLUMN "public"."gen_table_column"."update_by" IS '更新者';
COMMENT ON COLUMN "public"."gen_table_column"."update_time" IS '更新时间';
COMMENT ON TABLE "public"."gen_table_column" IS '代码生成业务表字段';

-- ----------------------------
-- Primary Key structure for table gen_table_column
-- ----------------------------
ALTER TABLE "public"."gen_table_column" ADD CONSTRAINT "gen_table_column_pkey" PRIMARY KEY ("column_id");
