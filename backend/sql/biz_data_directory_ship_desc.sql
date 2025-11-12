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

 Date: 02/12/2024 11:18:10
*/


-- ----------------------------
-- Table structure for biz_data_directory_ship_desc
-- ----------------------------
DROP TABLE IF EXISTS "public"."biz_data_directory_ship_desc";
CREATE TABLE "public"."biz_data_directory_ship_desc" (
  "id" "pg_catalog"."int8" NOT NULL,
  "cn_name" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" NOT NULL,
  "data_directory_id" "pg_catalog"."int8" NOT NULL,
  "en_name" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" NOT NULL,
  "fields" "pg_catalog"."text" COLLATE "pg_catalog"."default" NOT NULL
)
;
COMMENT ON COLUMN "public"."biz_data_directory_ship_desc"."id" IS '主键';
COMMENT ON COLUMN "public"."biz_data_directory_ship_desc"."cn_name" IS '数据资源中文名称';
COMMENT ON COLUMN "public"."biz_data_directory_ship_desc"."data_directory_id" IS '关联的数据资源ID';
COMMENT ON COLUMN "public"."biz_data_directory_ship_desc"."en_name" IS '数据资源英文名称';
COMMENT ON COLUMN "public"."biz_data_directory_ship_desc"."fields" IS '关联数据项,号分割';
COMMENT ON TABLE "public"."biz_data_directory_ship_desc" IS '目录关联数据资源目录表和字段关联文字描述';

-- ----------------------------
-- Primary Key structure for table biz_data_directory_ship_desc
-- ----------------------------
ALTER TABLE "public"."biz_data_directory_ship_desc" ADD CONSTRAINT "PRIMARY_KEY" PRIMARY KEY ("id");
