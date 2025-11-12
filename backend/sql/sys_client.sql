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

 Date: 02/12/2024 11:18:54
*/


-- ----------------------------
-- Table structure for sys_client
-- ----------------------------
DROP TABLE IF EXISTS "public"."sys_client";
CREATE TABLE "public"."sys_client" (
  "id" "pg_catalog"."int8" NOT NULL,
  "client_id" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "client_key" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "client_secret" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "grant_type" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "device_type" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" DEFAULT NULL::character varying,
  "active_timeout" "pg_catalog"."int4" DEFAULT 1800,
  "timeout" "pg_catalog"."int4" DEFAULT 604800,
  "status" "pg_catalog"."bpchar" COLLATE "pg_catalog"."default" DEFAULT '0'::bpchar,
  "del_flag" "pg_catalog"."bpchar" COLLATE "pg_catalog"."default" DEFAULT '0'::bpchar,
  "create_dept" "pg_catalog"."int8",
  "create_by" "pg_catalog"."int8",
  "create_time" "pg_catalog"."timestamptz",
  "update_by" "pg_catalog"."int8",
  "update_time" "pg_catalog"."timestamptz",
  "rollback_url" "pg_catalog"."varchar" COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "public"."sys_client"."id" IS 'id';
COMMENT ON COLUMN "public"."sys_client"."client_id" IS '客户端id';
COMMENT ON COLUMN "public"."sys_client"."client_key" IS '客户端key';
COMMENT ON COLUMN "public"."sys_client"."client_secret" IS '客户端秘钥';
COMMENT ON COLUMN "public"."sys_client"."grant_type" IS '授权类型';
COMMENT ON COLUMN "public"."sys_client"."device_type" IS '设备类型';
COMMENT ON COLUMN "public"."sys_client"."active_timeout" IS 'token活跃超时时间';
COMMENT ON COLUMN "public"."sys_client"."timeout" IS 'token固定超时';
COMMENT ON COLUMN "public"."sys_client"."status" IS '状态（0正常 1停用）';
COMMENT ON COLUMN "public"."sys_client"."del_flag" IS '删除标志（0代表存在 2代表删除）';
COMMENT ON COLUMN "public"."sys_client"."create_dept" IS '创建部门';
COMMENT ON COLUMN "public"."sys_client"."create_by" IS '创建者';
COMMENT ON COLUMN "public"."sys_client"."create_time" IS '创建时间';
COMMENT ON COLUMN "public"."sys_client"."update_by" IS '更新者';
COMMENT ON COLUMN "public"."sys_client"."update_time" IS '更新时间';
COMMENT ON COLUMN "public"."sys_client"."rollback_url" IS '回调地址';
COMMENT ON TABLE "public"."sys_client" IS '系统授权表';

-- ----------------------------
-- Records of sys_client
-- ----------------------------
INSERT INTO "public"."sys_client" VALUES (1, 'e5cd7e4891bf95d1d19206ce24a7b32e', 'pc', 'pc123', 'password,social,pai,province', 'pc', 900, 1800, '0', '0', NULL, NULL, '2024-08-27 18:10:04+08', NULL, '2024-08-27 18:10:04+08', 'http://192.168.20.32/manage/#/oauth/callback');
INSERT INTO "public"."sys_client" VALUES (2, '428a8310cd442757ae699df5d894f051', 'app', 'app123', 'password,sms,social', 'android', 900, 1800, '0', '0', NULL, NULL, '2024-08-27 18:10:04+08', NULL, '2024-08-27 18:10:04+08', 'http://localhost');
INSERT INTO "public"."sys_client" VALUES (3, '45cbc8c8f4b54cb28ec779ea75c5aef0', 'tsl', '379eba7890384f76a8121216b7479514', 'externalApp,password', 'pc', 900, 1800, '0', '0', NULL, NULL, '2024-08-27 18:10:04+08', NULL, '2024-08-27 18:10:04+08', 'http://localhost:5180//manage/#/oauth/callback');

-- ----------------------------
-- Primary Key structure for table sys_client
-- ----------------------------
ALTER TABLE "public"."sys_client" ADD CONSTRAINT "sys_client_pkey" PRIMARY KEY ("id");
