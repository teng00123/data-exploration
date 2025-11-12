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

 Date: 02/12/2024 11:17:40
*/


-- ----------------------------
-- Table structure for biz_data_directory_audit
-- ----------------------------
DROP TABLE IF EXISTS "public"."biz_data_directory_audit";
CREATE TABLE "public"."biz_data_directory_audit" (
  "id" "pg_catalog"."int8" NOT NULL (
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
),
  "data_directory_id" "pg_catalog"."int8",
  "operator_id" "pg_catalog"."int8",
  "operator_name" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "operator_time" "pg_catalog"."timestamptz",
  "audit_result" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "remark" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "type" "pg_catalog"."int4"
)
;
COMMENT ON COLUMN "public"."biz_data_directory_audit"."id" IS '主键';
COMMENT ON COLUMN "public"."biz_data_directory_audit"."data_directory_id" IS '数据目录表 ID';
COMMENT ON COLUMN "public"."biz_data_directory_audit"."operator_id" IS '审核人 ID';
COMMENT ON COLUMN "public"."biz_data_directory_audit"."operator_name" IS '审核人姓名';
COMMENT ON COLUMN "public"."biz_data_directory_audit"."operator_time" IS '审核时间';
COMMENT ON COLUMN "public"."biz_data_directory_audit"."audit_result" IS '审核结果';
COMMENT ON COLUMN "public"."biz_data_directory_audit"."remark" IS '原因';
COMMENT ON COLUMN "public"."biz_data_directory_audit"."type" IS '1 审核 2 校验审核 3 终验审核 4 不予普查审核';
COMMENT ON TABLE "public"."biz_data_directory_audit" IS '数据目录审核记录表';

-- ----------------------------
-- Primary Key structure for table biz_data_directory_audit
-- ----------------------------
ALTER TABLE "public"."biz_data_directory_audit" ADD CONSTRAINT "biz_data_directory_audit_pkey" PRIMARY KEY ("id");
