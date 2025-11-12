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

 Date: 02/12/2024 11:18:31
*/


-- ----------------------------
-- Table structure for biz_service_object
-- ----------------------------
DROP TABLE IF EXISTS "public"."biz_service_object";
CREATE TABLE "public"."biz_service_object" (
  "id" "pg_catalog"."int8" NOT NULL (
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
),
  "name" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "code" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "create_id" "pg_catalog"."int8",
  "create_time" "pg_catalog"."timestamptz",
  "update_time" "pg_catalog"."timestamptz",
  "update_id" "pg_catalog"."int8",
  "sort_index" "pg_catalog"."int4"
)
;
COMMENT ON COLUMN "public"."biz_service_object"."id" IS '主键';
COMMENT ON COLUMN "public"."biz_service_object"."name" IS '主体对象名称';
COMMENT ON COLUMN "public"."biz_service_object"."code" IS '主体对象代码';
COMMENT ON COLUMN "public"."biz_service_object"."create_id" IS '创建人 ID';
COMMENT ON COLUMN "public"."biz_service_object"."create_time" IS '创建时间';
COMMENT ON COLUMN "public"."biz_service_object"."update_time" IS '修改时间';
COMMENT ON COLUMN "public"."biz_service_object"."update_id" IS '修改人';
COMMENT ON COLUMN "public"."biz_service_object"."sort_index" IS '排序值';
COMMENT ON TABLE "public"."biz_service_object" IS '业务对象(服务对象)';

-- ----------------------------
-- Records of biz_service_object
-- ----------------------------
INSERT INTO "public"."biz_service_object" VALUES (5, '房', '03', 1, '2024-10-29 21:07:11.622+08', '2024-10-29 21:07:11.622+08', 1, 3);
INSERT INTO "public"."biz_service_object" VALUES (6, '权', '04', 1, '2024-10-29 21:08:22.957+08', '2024-10-29 21:08:22.957+08', 1, 4);
INSERT INTO "public"."biz_service_object" VALUES (7, '人', '05', 1, '2024-10-29 21:08:28.731+08', '2024-10-29 21:08:28.731+08', 1, 5);
INSERT INTO "public"."biz_service_object" VALUES (8, '企', '06', 1, '2024-10-29 21:08:39.543+08', '2024-10-29 21:08:39.543+08', 1, 6);
INSERT INTO "public"."biz_service_object" VALUES (9, '事', '07', 1, '2024-10-29 21:08:45.639+08', '2024-10-29 21:08:45.639+08', 1, 7);
INSERT INTO "public"."biz_service_object" VALUES (10, '物', '08', 1, '2024-10-29 21:08:52.74+08', '2024-10-29 21:08:52.74+08', 1, 8);
INSERT INTO "public"."biz_service_object" VALUES (11, '产', '09', 1, '2024-10-29 21:08:58.611+08', '2024-10-29 21:08:58.611+08', 1, 9);
INSERT INTO "public"."biz_service_object" VALUES (12, '车', '10', 1, '2024-10-29 21:09:09.1+08', '2024-10-29 21:09:09.1+08', 1, 10);
INSERT INTO "public"."biz_service_object" VALUES (3, '地', '01', 1, '2024-10-29 14:51:25.185+08', '2024-10-29 21:42:25.909+08', 1, 1);
INSERT INTO "public"."biz_service_object" VALUES (4, '楼', '02', 1, '2024-10-29 14:51:52.619+08', '2024-10-29 21:42:30.706+08', 1, 2);

-- ----------------------------
-- Primary Key structure for table biz_service_object
-- ----------------------------
ALTER TABLE "public"."biz_service_object" ADD CONSTRAINT "biz_service_object_pkey" PRIMARY KEY ("id");
