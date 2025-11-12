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

 Date: 02/12/2024 15:10:55
*/


-- ----------------------------
-- Table structure for biz_schedule_execute
-- ----------------------------
DROP TABLE IF EXISTS "public"."biz_schedule_execute";
CREATE TABLE "public"."biz_schedule_execute" (
  "id" "pg_catalog"."int8" NOT NULL DEFAULT nextval('biz_schedule_execute_id_seq'::regclass),
  "datasource_id" "pg_catalog"."int8",
  "schedule_id" "pg_catalog"."int8",
  "schedule_name" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "schedule_time" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "schedule_status" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "failure_reason" "pg_catalog"."text" COLLATE "pg_catalog"."default",
  "create_time" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "update_time" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "end_time" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "time_consuming" "pg_catalog"."varchar" COLLATE "pg_catalog"."default"
)
;

-- ----------------------------
-- Primary Key structure for table biz_schedule_execute
-- ----------------------------
ALTER TABLE "public"."biz_schedule_execute" ADD CONSTRAINT "biz_schedule_execute_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Foreign Keys structure for table biz_schedule_execute
-- ----------------------------
ALTER TABLE "public"."biz_schedule_execute" ADD CONSTRAINT "biz_schedule_execute_datasource_id_fkey" FOREIGN KEY ("datasource_id") REFERENCES "public"."biz_datasource_info" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;
ALTER TABLE "public"."biz_schedule_execute" ADD CONSTRAINT "biz_schedule_execute_schedule_id_fkey" FOREIGN KEY ("schedule_id") REFERENCES "public"."biz_schedule_info" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;
