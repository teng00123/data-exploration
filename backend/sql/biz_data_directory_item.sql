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

 Date: 02/12/2024 11:17:59
*/


-- ----------------------------
-- Table structure for biz_data_directory_item
-- ----------------------------
DROP TABLE IF EXISTS "public"."biz_data_directory_item";
CREATE TABLE "public"."biz_data_directory_item" (
  "id" "pg_catalog"."int8" NOT NULL,
  "table_info_id" "pg_catalog"."int8" NOT NULL,
  "field_id" "pg_catalog"."int8",
  "en_name" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "item_name" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "item_type" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "primary_keys" "pg_catalog"."bool",
  "data_directory_id" "pg_catalog"."int8"
)
;
COMMENT ON COLUMN "public"."biz_data_directory_item"."id" IS '主键';
COMMENT ON COLUMN "public"."biz_data_directory_item"."table_info_id" IS '表 ID';
COMMENT ON COLUMN "public"."biz_data_directory_item"."field_id" IS '字段 ID';
COMMENT ON COLUMN "public"."biz_data_directory_item"."en_name" IS '数据项英文名称';
COMMENT ON COLUMN "public"."biz_data_directory_item"."item_name" IS '数据项名称';
COMMENT ON COLUMN "public"."biz_data_directory_item"."item_type" IS '数据项类型';
COMMENT ON COLUMN "public"."biz_data_directory_item"."primary_keys" IS '是否主键';
COMMENT ON COLUMN "public"."biz_data_directory_item"."data_directory_id" IS '目录 ID';
COMMENT ON TABLE "public"."biz_data_directory_item" IS '数据项信息';

-- ----------------------------
-- Primary Key structure for table biz_data_directory_item
-- ----------------------------
ALTER TABLE "public"."biz_data_directory_item" ADD CONSTRAINT "biz_data_directory_item_pkey" PRIMARY KEY ("id");
