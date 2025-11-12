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

 Date: 02/12/2024 11:18:04
*/


-- ----------------------------
-- Table structure for biz_data_directory_ship
-- ----------------------------
DROP TABLE IF EXISTS "public"."biz_data_directory_ship";
CREATE TABLE "public"."biz_data_directory_ship" (
  "id" "pg_catalog"."int8" NOT NULL,
  "data_directory_id" "pg_catalog"."int8" NOT NULL,
  "ship_id" "pg_catalog"."int8" NOT NULL,
  "create_time" "pg_catalog"."timestamptz",
  "update_time" "pg_catalog"."timestamptz",
  "create_id" "pg_catalog"."int8"
)
;
COMMENT ON COLUMN "public"."biz_data_directory_ship"."id" IS '主键';
COMMENT ON COLUMN "public"."biz_data_directory_ship"."data_directory_id" IS '数据目录 ID';
COMMENT ON COLUMN "public"."biz_data_directory_ship"."ship_id" IS '关联的目录ID';
COMMENT ON COLUMN "public"."biz_data_directory_ship"."create_time" IS '创建时间';
COMMENT ON COLUMN "public"."biz_data_directory_ship"."update_time" IS '修改时间';
COMMENT ON COLUMN "public"."biz_data_directory_ship"."create_id" IS '创建人 ID';
COMMENT ON TABLE "public"."biz_data_directory_ship" IS '目录关联数据资源表(目录关联目录)';

-- ----------------------------
-- Primary Key structure for table biz_data_directory_ship
-- ----------------------------
ALTER TABLE "public"."biz_data_directory_ship" ADD CONSTRAINT "biz_data_directory_table_pkey" PRIMARY KEY ("id");
