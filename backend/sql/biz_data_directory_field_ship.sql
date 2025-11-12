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

 Date: 02/12/2024 11:17:52
*/


-- ----------------------------
-- Table structure for biz_data_directory_field_ship
-- ----------------------------
DROP TABLE IF EXISTS "public"."biz_data_directory_field_ship";
CREATE TABLE "public"."biz_data_directory_field_ship" (
  "id" "pg_catalog"."int8" NOT NULL DEFAULT nextval('biz_data_directory_field_ship_id_seq'::regclass),
  "data_directory_id" "pg_catalog"."int8",
  "field_id" "pg_catalog"."int8",
  "ship_data_directory_id" "pg_catalog"."int8",
  "field_name" "pg_catalog"."varchar" COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "public"."biz_data_directory_field_ship"."id" IS '主键';
COMMENT ON COLUMN "public"."biz_data_directory_field_ship"."data_directory_id" IS '目录ID';
COMMENT ON COLUMN "public"."biz_data_directory_field_ship"."field_id" IS '字段ID';
COMMENT ON COLUMN "public"."biz_data_directory_field_ship"."ship_data_directory_id" IS '关联的目录ID';
COMMENT ON COLUMN "public"."biz_data_directory_field_ship"."field_name" IS '字段名称';
COMMENT ON TABLE "public"."biz_data_directory_field_ship" IS '数据目录和表字段关联';

-- ----------------------------
-- Primary Key structure for table biz_data_directory_field_ship
-- ----------------------------
ALTER TABLE "public"."biz_data_directory_field_ship" ADD CONSTRAINT "biz_data_directory_field_ship_pkey" PRIMARY KEY ("id");
