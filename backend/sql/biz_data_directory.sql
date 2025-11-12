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

 Date: 02/12/2024 11:15:02
*/


-- ----------------------------
-- Table structure for biz_data_directory
-- ----------------------------
DROP TABLE IF EXISTS "public"."biz_data_directory";
CREATE TABLE "public"."biz_data_directory" (
  "id" "pg_catalog"."int8" NOT NULL,
  "datasource_id" "pg_catalog"."int8",
  "table_id" "pg_catalog"."int8",
  "create_id" "pg_catalog"."int8",
  "status" "pg_catalog"."int4",
  "create_time" "pg_catalog"."timestamptz",
  "update_time" "pg_catalog"."timestamptz",
  "system_id" "pg_catalog"."int8",
  "data_level" "pg_catalog"."int4",
  "summary" "pg_catalog"."text" COLLATE "pg_catalog"."default",
  "up_cycle" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "data_zie" "pg_catalog"."int8",
  "cn_name" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "contents_code" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "en_name" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "data_source_type" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "data_processing" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "data_scope" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "data_start_date_scope" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "data_end_date_scope" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "contact" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "phone" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "email" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "data_version" "pg_catalog"."int4",
  "data_provider" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "ywy_id" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "zty_id" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "ydx_id" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "ywy_name" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "zty_name" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "ydx_name" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "commit_time" "pg_catalog"."timestamptz",
  "dept_id" "pg_catalog"."int8",
  "data_version_time" "pg_catalog"."timestamptz",
  "history" "pg_catalog"."bool",
  "build_directory" "pg_catalog"."bool" DEFAULT true,
  "build_directory_result" "pg_catalog"."text" COLLATE "pg_catalog"."default",
  "build_directory_time" "pg_catalog"."timestamptz",
  "parent_dept_id" "pg_catalog"."int8",
  "datasource_name" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "creator_name" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "system_name" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "dept_name" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "main_version_id" "pg_catalog"."int8"
)
;
COMMENT ON COLUMN "public"."biz_data_directory"."id" IS '主键';
COMMENT ON COLUMN "public"."biz_data_directory"."datasource_id" IS '数据源 ID';
COMMENT ON COLUMN "public"."biz_data_directory"."table_id" IS '表 ID';
COMMENT ON COLUMN "public"."biz_data_directory"."create_id" IS '创建人 ID';
COMMENT ON COLUMN "public"."biz_data_directory"."status" IS '状态:1待填报 2待审核提交 3已审核提交';
COMMENT ON COLUMN "public"."biz_data_directory"."create_time" IS '创建时间';
COMMENT ON COLUMN "public"."biz_data_directory"."update_time" IS '修改时间';
COMMENT ON COLUMN "public"."biz_data_directory"."system_id" IS '来源系统 ID';
COMMENT ON COLUMN "public"."biz_data_directory"."data_level" IS '1国家级 2 省级 3 市级 4 县(区)级';
COMMENT ON COLUMN "public"."biz_data_directory"."summary" IS '政务数据摘要';
COMMENT ON COLUMN "public"."biz_data_directory"."up_cycle" IS '更新周期';
COMMENT ON COLUMN "public"."biz_data_directory"."data_zie" IS '数据量';
COMMENT ON COLUMN "public"."biz_data_directory"."cn_name" IS '数据目录中文名称';
COMMENT ON COLUMN "public"."biz_data_directory"."contents_code" IS '数据资源目录代码';
COMMENT ON COLUMN "public"."biz_data_directory"."en_name" IS '数据目录英文名称';
COMMENT ON COLUMN "public"."biz_data_directory"."data_source_type" IS '数据资源类型(库表 文件 接口 暂无数据)';
COMMENT ON COLUMN "public"."biz_data_directory"."data_processing" IS '数据加工程度(原始数据 脱敏数据 标签数据 统计数据 融合数据)';
COMMENT ON COLUMN "public"."biz_data_directory"."data_scope" IS '数据区域范围';
COMMENT ON COLUMN "public"."biz_data_directory"."data_start_date_scope" IS '数据时间范围-开始时间';
COMMENT ON COLUMN "public"."biz_data_directory"."data_end_date_scope" IS '数据时间范围-结束时间';
COMMENT ON COLUMN "public"."biz_data_directory"."contact" IS '联系人';
COMMENT ON COLUMN "public"."biz_data_directory"."phone" IS '联系方式';
COMMENT ON COLUMN "public"."biz_data_directory"."email" IS '邮件';
COMMENT ON COLUMN "public"."biz_data_directory"."data_version" IS '数据版本';
COMMENT ON COLUMN "public"."biz_data_directory"."data_provider" IS '数据提供方';
COMMENT ON COLUMN "public"."biz_data_directory"."ywy_id" IS '业务域ID多个,号分割';
COMMENT ON COLUMN "public"."biz_data_directory"."zty_id" IS '主题域ID多个,号分割';
COMMENT ON COLUMN "public"."biz_data_directory"."ydx_id" IS '业务对象 ID多个,号分割';
COMMENT ON COLUMN "public"."biz_data_directory"."ywy_name" IS '业务域名称';
COMMENT ON COLUMN "public"."biz_data_directory"."zty_name" IS '主题域名称';
COMMENT ON COLUMN "public"."biz_data_directory"."ydx_name" IS '业务对象名称';
COMMENT ON COLUMN "public"."biz_data_directory"."commit_time" IS '提交申请的时间';
COMMENT ON COLUMN "public"."biz_data_directory"."dept_id" IS '创建人的科室 ID';
COMMENT ON COLUMN "public"."biz_data_directory"."data_version_time" IS '新版本生成的时间';
COMMENT ON COLUMN "public"."biz_data_directory"."history" IS '是否是旧版本(每次校验通过后生成新的版本)';
COMMENT ON COLUMN "public"."biz_data_directory"."build_directory" IS '不予编目:true编目 false不予编目';
COMMENT ON COLUMN "public"."biz_data_directory"."build_directory_result" IS '不予编目的理由';
COMMENT ON COLUMN "public"."biz_data_directory"."build_directory_time" IS '不予普查提交时间';
COMMENT ON COLUMN "public"."biz_data_directory"."parent_dept_id" IS '二级单位ID(四川省下的二级单位ID)';
COMMENT ON COLUMN "public"."biz_data_directory"."datasource_name" IS '数据源名称';
COMMENT ON COLUMN "public"."biz_data_directory"."creator_name" IS '创建人名称';
COMMENT ON COLUMN "public"."biz_data_directory"."system_name" IS '系统名称';
COMMENT ON COLUMN "public"."biz_data_directory"."dept_name" IS '科室名称';
COMMENT ON COLUMN "public"."biz_data_directory"."main_version_id" IS '主版本ID(版本为1的即为主版本ID)';
COMMENT ON TABLE "public"."biz_data_directory" IS '数据目录表';

-- ----------------------------
-- Primary Key structure for table biz_data_directory
-- ----------------------------
ALTER TABLE "public"."biz_data_directory" ADD CONSTRAINT "biz_data_ directory_pkey" PRIMARY KEY ("id");
