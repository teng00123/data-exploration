/*
 Navicat Premium Data Transfer

 Source Server         : 192.168.20.48
 Source Server Type    : PostgreSQL
 Source Server Version : 160004
 Source Host           : 192.168.20.48:5432
 Source Catalog        : nacos
 Source Schema         : public

 Target Server Type    : PostgreSQL
 Target Server Version : 160004
 File Encoding         : 65001

 Date: 30/10/2024 10:00:31
*/


-- ----------------------------
-- Sequence structure for config_info_aggr_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "config_info_aggr_id_seq" CASCADE;
CREATE SEQUENCE "config_info_aggr_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for config_info_beta_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "config_info_beta_id_seq" CASCADE;
CREATE SEQUENCE "config_info_beta_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for config_info_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "config_info_id_seq" CASCADE;
CREATE SEQUENCE "config_info_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for config_info_tag_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "config_info_tag_id_seq" CASCADE;
CREATE SEQUENCE "config_info_tag_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for config_tags_relation_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "config_tags_relation_id_seq" CASCADE;
CREATE SEQUENCE "config_tags_relation_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for config_tags_relation_nid_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "config_tags_relation_nid_seq" CASCADE;
CREATE SEQUENCE "config_tags_relation_nid_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for group_capacity_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "group_capacity_id_seq" CASCADE;
CREATE SEQUENCE "group_capacity_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for his_config_info_nid_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "his_config_info_nid_seq" CASCADE;
CREATE SEQUENCE "his_config_info_nid_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for tenant_capacity_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "tenant_capacity_id_seq" CASCADE;
CREATE SEQUENCE "tenant_capacity_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for tenant_info_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "tenant_info_id_seq" CASCADE;
CREATE SEQUENCE "tenant_info_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Table structure for config_info
-- ----------------------------
DROP TABLE IF EXISTS "config_info" CASCADE;
CREATE TABLE "config_info" (
  "id" "pg_catalog"."int8" NOT NULL DEFAULT nextval('config_info_id_seq'::regclass),
  "data_id" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" NOT NULL,
  "group_id" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "content" "pg_catalog"."text" COLLATE "pg_catalog"."default" NOT NULL,
  "md5" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "gmt_create" "pg_catalog"."timestamp" NOT NULL,
  "gmt_modified" "pg_catalog"."timestamp" NOT NULL,
  "src_user" "pg_catalog"."text" COLLATE "pg_catalog"."default",
  "src_ip" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "app_name" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "tenant_id" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "c_desc" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "c_use" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "effect" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "type" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "c_schema" "pg_catalog"."text" COLLATE "pg_catalog"."default",
  "encrypted_data_key" "pg_catalog"."text" COLLATE "pg_catalog"."default" NOT NULL
)
;
COMMENT ON COLUMN "config_info"."id" IS 'id';
COMMENT ON COLUMN "config_info"."data_id" IS 'data_id';
COMMENT ON COLUMN "config_info"."content" IS 'content';
COMMENT ON COLUMN "config_info"."md5" IS 'md5';
COMMENT ON COLUMN "config_info"."gmt_create" IS '创建时间';
COMMENT ON COLUMN "config_info"."gmt_modified" IS '修改时间';
COMMENT ON COLUMN "config_info"."src_user" IS 'source user';
COMMENT ON COLUMN "config_info"."src_ip" IS 'source ip';
COMMENT ON COLUMN "config_info"."tenant_id" IS '租户字段';
COMMENT ON COLUMN "config_info"."encrypted_data_key" IS '秘钥';
COMMENT ON TABLE "config_info" IS 'config_info';

-- ----------------------------
-- Records of config_info
-- ----------------------------
BEGIN;
INSERT INTO "config_info" VALUES (1, 'common.yaml', 'DEFAULT_GROUP', 'spring:
  cloud:
    nacos:
      discovery:
        server-addr: 192.168.20.48:8848
        namespace: 876aed9e-d385-4cb1-9b39-63a28eaf0737  #命名空间 代指某个环境
  sentinel:
    transport:
      # 指定sentinel 控制台的地址
      dashboard: 192.168.20.94:8080
    eager: true
  jackson:
    mapper:
      ALLOW_EXPLICIT_PROPERTY_RENAMING: true
    deserialization:
      READ_DATE_TIMESTAMPS_AS_NANOSECONDS: false
    serialization:
      WRITE_DATE_TIMESTAMPS_AS_NANOSECONDS: false
      WRITE_DATES_AS_TIMESTAMPS: true
# api接口加密
api-decrypt:
  # 是否开启全局接口加密
  enabled: false
  # AES 加密头标识
  headerFlag: encrypt-key
  # 响应加密公钥 非对称算法的公私钥 如：SM2，RSA 使用者请自行更换
  # 对应前端解密私钥 MIIBVAIBADANBgkqhkiG9w0BAQEFAASCAT4wggE6AgEAAkEAmc3CuPiGL/LcIIm7zryCEIbl1SPzBkr75E2VMtxegyZ1lYRD+7TZGAPkvIsBcaMs6Nsy0L78n2qh+lIZMpLH8wIDAQABAkEAk82Mhz0tlv6IVCyIcw/s3f0E+WLmtPFyR9/WtV3Y5aaejUkU60JpX4m5xNR2VaqOLTZAYjW8Wy0aXr3zYIhhQQIhAMfqR9oFdYw1J9SsNc+CrhugAvKTi0+BF6VoL6psWhvbAiEAxPPNTmrkmrXwdm/pQQu3UOQmc2vCZ5tiKpW10CgJi8kCIFGkL6utxw93Ncj4exE/gPLvKcT+1Emnoox+O9kRXss5AiAMtYLJDaLEzPrAWcZeeSgSIzbL+ecokmFKSDDcRske6QIgSMkHedwND1olF8vlKsJUGK3BcdtM8w4Xq7BpSBwsloE=
  publicKey: MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAJnNwrj4hi/y3CCJu868ghCG5dUj8wZK++RNlTLcXoMmdZWEQ/u02RgD5LyLAXGjLOjbMtC+/J9qofpSGTKSx/MCAwEAAQ==
  # 请求解密私钥 非对称算法的公私钥 如：SM2，RSA 使用者请自行更换
  # 对应前端加密公钥 MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAKoR8mX0rGKLqzcWmOzbfj64K8ZIgOdHnzkXSOVOZbFu/TJhZ7rFAN+eaGkl3C4buccQd/EjEsj9ir7ijT7h96MCAwEAAQ==
  privateKey: MIIBVAIBADANBgkqhkiG9w0BAQEFAASCAT4wggE6AgEAAkEAqhHyZfSsYourNxaY7Nt+PrgrxkiA50efORdI5U5lsW79MmFnusUA355oaSXcLhu5xxB38SMSyP2KvuKNPuH3owIDAQABAkAfoiLyL+Z4lf4Myxk6xUDgLaWGximj20CUf+5BKKnlrK+Ed8gAkM0HqoTt2UZwA5E2MzS4EI2gjfQhz5X28uqxAiEA3wNFxfrCZlSZHb0gn2zDpWowcSxQAgiCstxGUoOqlW8CIQDDOerGKH5OmCJ4Z21v+F25WaHYPxCFMvwxpcw99EcvDQIgIdhDTIqD2jfYjPTY8Jj3EDGPbH2HHuffvflECt3Ek60CIQCFRlCkHpi7hthhYhovyloRYsM+IS9h/0BzlEAuO0ktMQIgSPT3aFAgJYwKpqRYKlLDVcflZFCKY7u3UP8iWi1Qw0Y=

sa-token:
  #jwt秘钥
  jwt-secret-key: abcdefghijklmnopqrstuvwxyz
  # token 名称（同时也是 cookie 名称）
  token-name: Authorization
  #如果是单体服务，这里设置为false，这个是校验服务访问是否从网关进入
  check-same-token: true
  autoRenew: true
  timeout: 1800', '650afdb60258cebd5316c3cacc25c1e7', '2024-10-18 11:33:20.519', '2024-10-18 14:49:36.279', 'nacos', '192.168.10.2', '', '876aed9e-d385-4cb1-9b39-63a28eaf0737', '', '', '', 'yaml', '', '');
INSERT INTO "config_info" VALUES (2, 'gateway.yaml', 'DEFAULT_GROUP', 'server:
  port: 9200 #端口
   
spring:
  cloud:
    gateway:
      requestLog: true
      discovery:
        locator:
          lowerCaseServiceId: true
          enabled: true
      routes:
       - id: api-user
         uri: lb://user-center
         order: 8001
         predicates:
         - Path=/api-user/**   
         filters:
         - StripPrefix=1 
       - id: api-auth
         uri: lb://auth
         order: 8002
         predicates:
         - Path=/api-auth/**
         filters:
         - PreserveHostHeader
         - StripPrefix=1  
       - id: api-file
         uri: lb://file
         order: 8003
         predicates:
         - Path=/api-file/**    
       - id: api-system
         uri: lb://system
         order: 8008
         predicates:
         - Path=/api-system/**
         filters:
         - StripPrefix=1 
  datasource: 
    dynamic:
      # 设置默认的数据源或者数据源组,默认值即为 master
      primary: master
      datasource:
        # 主库数据源
        master:
          type: com.zaxxer.hikari.HikariDataSource
          driver-class-name: org.postgresql.Driver
          url: jdbc:postgresql://192.168.20.48:5432/bsp-user?useUnicode=true&characterEncoding=utf8&useSSL=true&autoReconnect=true&reWriteBatchedInserts=true
          username: root
          password: 123456              

################### mysq end ##########################
  redis:
################### redis 单机版 start ########################## 
    host: 192.168.20.48
    port: 6379
    password: xshl2023
    timeout: 6000
    database: 8
    lettuce:
      pool:
        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException  
        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
      shutdown-timeout: 100ms
################### redis 单机版 end ##########################   
#    cluster:
#      nodes: 130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #192.168.3.157:7000,192.168.3.158:7000,192.168.3.159:7000,192.168.3.157:7001,192.168.3.158:7001,192.168.3.159:7001
#    timeout: 1000 # 连接超时时间（毫秒）
#    lettuce:
#      pool:
#        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
#        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
#        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException  
#        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
#      shutdown-timeout: 100ms
  
mybatis-plus:
  # 不支持多包, 如有需要可在注解配置 或 提升扫包等级
  # 例如 com.**.**.mapper
  mapperPackage: com.xshl.bsp.**.mapper
  # 对应的 XML 文件位置
  mapperLocations: classpath*:mappers/**/*Mapper.xml
  # 实体扫描，多个package用逗号或者分号分隔
  typeAliasesPackage: com.xshl.bsp.**.domain
  global-config:
    dbConfig:
      # 主键类型
      # AUTO 自增 NONE 空 INPUT 用户输入 ASSIGN_ID 雪花 ASSIGN_UUID 唯一 UUID
      # 如需改为自增 需要将数据库表全部设置为自增
      idType: ASSIGN_ID


sa-token:
  #忽略的路径
  pathIgnores: /code/**, /auth/**, /test/**, /external/auth/getUserInfo, /external/embed/detail/**, /home/page/**, /matter/info/export, /sys/carousel/list, /entrepreneur/theory/list
  jwt-secret-key: abcdefghijklmnopqrstuvwxyz
  # 开启内网服务调用鉴权(不允许越过gateway访问内网服务 保障服务安全)
  #check-same-token: true
  # token 有效期（单位：秒） 默认30天，-1 代表永久有效
  timeout: 86400
  # token 最低活跃频率（单位：秒），如果 token 超过此时间没有访问系统就会被冻结，默认-1 代表不限制，永不冻结
  #active-timeout: -1
  # 是否允许同一账号多地同时登录 （为 true 时允许一起登录, 为 false 时新登录挤掉旧登录）
  #is-concurrent: true
  # 在多人登录同一账号时，是否共用一个 token （为 true 时所有登录共用一个 token, 为 false 时每次登录新建一个 token）
  #is-share: true
  # token 风格（默认可取值：uuid、simple-uuid、random-32、random-64、random-128、tik）
  #token-style: uuid
  # 是否输出操作日志
  #is-log: true

security:
  # 防止XSS攻击
  xss:
    enabled: true
    excludeUrls:
      - /api-user/notice
      - /flow/**
      - /tqt/api-flow/flow/**
      - /api-flow/flow/**
  # 不校验白名单
  ignore:
    whites: 
      - /api-auth/code
      - /api-auth/auth/**
      - /resource/sms/code
      - /*/v3/api-docs
      - /*/v2/api-docs
      - /*/error
      - /csrf
      - /doc.html
      - /webjars/**
      - /swagger-resources/**
      - /api-system/external/embed/detail/**
      - /api-auth/external/auth/**
      - /api-auth/sso/**
      - /api-system/home/page/**
      - /api-policy/home/page/**
      - /api-file/home/page/**
      - /api-policy/matter/info/export
      - /api-system/external/embed/detail/**
      - /api-quartz/test/**
      - /api-flow/login/**
      - /api-system/sys/carousel/list
      - /api-policy/entrepreneur/theory/list

swagger:
  enable: true
  butler:
    api-docs-path:  /v2/api-docs
    auto-generate-from-scg-routes: true
    ignore-routes:  api-eureka,api-generator,api-baidu

ribbon:
  ReadTimeout: 90000
  ConnectTimeout: 90000
  MaxAutoRetries: 0
  MaxAutoRetriesNextServer: 1
  OkToRetryOnAllOperations: false

feign:
  sentinel:
    enabled: true  #为feign整合sentinel

corsUrls: "*"', '548b501948c3a5a27412b85995157790', '2024-10-18 11:50:14.957', '2024-10-18 15:44:50.416', 'nacos', '192.168.10.2', '', '876aed9e-d385-4cb1-9b39-63a28eaf0737', '', '', '', 'yaml', '', '');
INSERT INTO "config_info" VALUES (4, 'user-center.yaml', 'DEFAULT_GROUP', '#端口配置
server:
  port: 8100   #固定端口
  forward-headers-strategy: none  #
  
spring:
  datasource: 
    dynamic:
      # 设置默认的数据源或者数据源组,默认值即为 master
      primary: master
      datasource:
        # 主库数据源
        master:
          type: com.zaxxer.hikari.HikariDataSource
          driver-class-name: org.postgresql.Driver
          url: jdbc:postgresql://192.168.20.48:5432/bsp-user?useUnicode=true&characterEncoding=utf8&useSSL=true&autoReconnect=true&reWriteBatchedInserts=true
          username: root
          password: 123456

  ################### redis 单机版 start ##########################
  redis:
    host: 192.168.20.48
    port: 6379
    password: xshl2023
    timeout: 6000
    database: 8
    lettuce:
      pool:
        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException
        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
      shutdown-timeout: 100ms
################### redis 单机版 end ##########################
#    cluster:
#      nodes: 130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #192.168.3.157:7000,192.168.3.158:7000,192.168.3.159:7000,192.168.3.157:7001,192.168.3.158:7001,192.168.3.159:7001
#    timeout: 1000 # 连接超时时间（毫秒）
#    lettuce:
#      pool:
#        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
#        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
#        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException
#        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
#      shutdown-timeout: 100ms

mybatis-plus:
  # 不支持多包, 如有需要可在注解配置 或 提升扫包等级
  # 例如 com.**.**.mapper
  mapperPackage: com.xshl.bsp.**.mapper
  # 对应的 XML 文件位置
  mapperLocations: classpath*:mappers/**/*Mapper.xml
  # 实体扫描，多个package用逗号或者分号分隔
  typeAliasesPackage: com.xshl.bsp.**.domain
  global-config:
    dbConfig:
      # 主键类型
      # AUTO 自增 NONE 空 INPUT 用户输入 ASSIGN_ID 雪花 ASSIGN_UUID 唯一 UUID
      # 如需改为自增 需要将数据库表全部设置为自增
      idType: ASSIGN_ID

logging:
  level:
    io.swagger.models.parameters.AbstractSerializableParameter: info #忽略swagger中的错误信息
    com.xshl.bsp: info
#配置日志输出
logback:
  log:
    level: INFO
    path: /home/xshl/logs/user-center


#设置最大超时时间
ribbon:  
  ServerListRefreshInterval: 10  #刷新服务列表源的间隔时间
  OkToRetryOnAllOperations: true
  MaxAutoRetries: 1
  MaxAutoRetriesNextServer: 1
  ReadTimeout: 16000  
  ConnectTimeout: 16000 

gdzw:
  tokenUrl: a

environment: dev

sa-token:
  #忽略的路径
  pathIgnores: /user/**, dept/**
  # token 有效期（单位：秒） 默认30天，-1 代表永久有效
  #timeout: 2592000
  # token 最低活跃频率（单位：秒），如果 token 超过此时间没有访问系统就会被冻结，默认-1 代表不限制，永不冻结
  #active-timeout: -1
  # 是否允许同一账号多地同时登录 （为 true 时允许一起登录, 为 false 时新登录挤掉旧登录）
  #is-concurrent: true
  # 在多人登录同一账号时，是否共用一个 token （为 true 时所有登录共用一个 token, 为 false 时每次登录新建一个 token）
  #is-share: true
  # token 风格（默认可取值：uuid、simple-uuid、random-32、random-64、random-128、tik）
  #token-style: uuid
  # 是否输出操作日志
  #is-log: true

flow:
  companyId: b482a6393faefd53783f9d093cd4ddff
  sync: true
 ', '2726e107b651bcbd6a90cc406f976178', '2024-10-18 11:51:32.733', '2024-10-18 15:50:51.292', 'nacos', '192.168.10.2', '', '876aed9e-d385-4cb1-9b39-63a28eaf0737', '', '', '', 'yaml', '', '');
INSERT INTO "config_info" VALUES (15, 'common.yaml', 'DEFAULT_GROUP', 'spring:
  cloud:
    nacos:
      discovery:
        server-addr: 192.168.20.48:8848
        namespace: 876aed9e-d385-4cb1-9b39-63a28eaf0737  #命名空间 代指某个环境
  sentinel:
    transport:
      # 指定sentinel 控制台的地址
      dashboard: 192.168.20.94:8080
    eager: true
  jackson:
    mapper:
      ALLOW_EXPLICIT_PROPERTY_RENAMING: true
    deserialization:
      READ_DATE_TIMESTAMPS_AS_NANOSECONDS: false
    serialization:
      WRITE_DATE_TIMESTAMPS_AS_NANOSECONDS: false
      WRITE_DATES_AS_TIMESTAMPS: true
# api接口加密
api-decrypt:
  # 是否开启全局接口加密
  enabled: false
  # AES 加密头标识
  headerFlag: encrypt-key
  # 响应加密公钥 非对称算法的公私钥 如：SM2，RSA 使用者请自行更换
  # 对应前端解密私钥 MIIBVAIBADANBgkqhkiG9w0BAQEFAASCAT4wggE6AgEAAkEAmc3CuPiGL/LcIIm7zryCEIbl1SPzBkr75E2VMtxegyZ1lYRD+7TZGAPkvIsBcaMs6Nsy0L78n2qh+lIZMpLH8wIDAQABAkEAk82Mhz0tlv6IVCyIcw/s3f0E+WLmtPFyR9/WtV3Y5aaejUkU60JpX4m5xNR2VaqOLTZAYjW8Wy0aXr3zYIhhQQIhAMfqR9oFdYw1J9SsNc+CrhugAvKTi0+BF6VoL6psWhvbAiEAxPPNTmrkmrXwdm/pQQu3UOQmc2vCZ5tiKpW10CgJi8kCIFGkL6utxw93Ncj4exE/gPLvKcT+1Emnoox+O9kRXss5AiAMtYLJDaLEzPrAWcZeeSgSIzbL+ecokmFKSDDcRske6QIgSMkHedwND1olF8vlKsJUGK3BcdtM8w4Xq7BpSBwsloE=
  publicKey: MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAJnNwrj4hi/y3CCJu868ghCG5dUj8wZK++RNlTLcXoMmdZWEQ/u02RgD5LyLAXGjLOjbMtC+/J9qofpSGTKSx/MCAwEAAQ==
  # 请求解密私钥 非对称算法的公私钥 如：SM2，RSA 使用者请自行更换
  # 对应前端加密公钥 MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAKoR8mX0rGKLqzcWmOzbfj64K8ZIgOdHnzkXSOVOZbFu/TJhZ7rFAN+eaGkl3C4buccQd/EjEsj9ir7ijT7h96MCAwEAAQ==
  privateKey: MIIBVAIBADANBgkqhkiG9w0BAQEFAASCAT4wggE6AgEAAkEAqhHyZfSsYourNxaY7Nt+PrgrxkiA50efORdI5U5lsW79MmFnusUA355oaSXcLhu5xxB38SMSyP2KvuKNPuH3owIDAQABAkAfoiLyL+Z4lf4Myxk6xUDgLaWGximj20CUf+5BKKnlrK+Ed8gAkM0HqoTt2UZwA5E2MzS4EI2gjfQhz5X28uqxAiEA3wNFxfrCZlSZHb0gn2zDpWowcSxQAgiCstxGUoOqlW8CIQDDOerGKH5OmCJ4Z21v+F25WaHYPxCFMvwxpcw99EcvDQIgIdhDTIqD2jfYjPTY8Jj3EDGPbH2HHuffvflECt3Ek60CIQCFRlCkHpi7hthhYhovyloRYsM+IS9h/0BzlEAuO0ktMQIgSPT3aFAgJYwKpqRYKlLDVcflZFCKY7u3UP8iWi1Qw0Y=

sa-token:
  #jwt秘钥
  jwt-secret-key: abcdefghijklmnopqrstuvwxyz
  # token 名称（同时也是 cookie 名称）
  token-name: Authorization
  #如果是单体服务，这里设置为false，这个是校验服务访问是否从网关进入
  check-same-token: true
  autoRenew: true
  timeout: 1800', '650afdb60258cebd5316c3cacc25c1e7', '2024-10-18 16:07:22.231', '2024-10-18 16:07:22.231', NULL, '192.168.10.2', '', '704f0050-72fe-4572-8e7d-40eb1e58aecd', '', NULL, NULL, 'yaml', NULL, '');
INSERT INTO "config_info" VALUES (16, 'gateway.yaml', 'DEFAULT_GROUP', 'server:
  port: 9200 #端口
   
spring:
  cloud:
    gateway:
      requestLog: true
      discovery:
        locator:
          lowerCaseServiceId: true
          enabled: true
      routes:
       - id: api-user
         uri: lb://user-center
         order: 8001
         predicates:
         - Path=/api-user/**   
         filters:
         - StripPrefix=1 
       - id: api-auth
         uri: lb://auth
         order: 8002
         predicates:
         - Path=/api-auth/**
         filters:
         - PreserveHostHeader
         - StripPrefix=1  
       - id: api-file
         uri: lb://file
         order: 8003
         predicates:
         - Path=/api-file/**    
       - id: api-system
         uri: lb://system
         order: 8008
         predicates:
         - Path=/api-system/**
         filters:
         - StripPrefix=1 
  datasource: 
    dynamic:
      # 设置默认的数据源或者数据源组,默认值即为 master
      primary: master
      datasource:
        # 主库数据源
        master:
          type: com.zaxxer.hikari.HikariDataSource
          driver-class-name: org.postgresql.Driver
          url: jdbc:postgresql://192.168.20.48:5432/bsp-user?useUnicode=true&characterEncoding=utf8&useSSL=true&autoReconnect=true&reWriteBatchedInserts=true
          username: root
          password: 123456              

################### mysq end ##########################
  redis:
################### redis 单机版 start ########################## 
    host: 192.168.20.48
    port: 6379
    password: xshl2023
    timeout: 6000
    database: 8
    lettuce:
      pool:
        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException  
        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
      shutdown-timeout: 100ms
################### redis 单机版 end ##########################   
#    cluster:
#      nodes: 130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #192.168.3.157:7000,192.168.3.158:7000,192.168.3.159:7000,192.168.3.157:7001,192.168.3.158:7001,192.168.3.159:7001
#    timeout: 1000 # 连接超时时间（毫秒）
#    lettuce:
#      pool:
#        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
#        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
#        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException  
#        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
#      shutdown-timeout: 100ms
  
mybatis-plus:
  # 不支持多包, 如有需要可在注解配置 或 提升扫包等级
  # 例如 com.**.**.mapper
  mapperPackage: com.xshl.bsp.**.mapper
  # 对应的 XML 文件位置
  mapperLocations: classpath*:mappers/**/*Mapper.xml
  # 实体扫描，多个package用逗号或者分号分隔
  typeAliasesPackage: com.xshl.bsp.**.domain
  global-config:
    dbConfig:
      # 主键类型
      # AUTO 自增 NONE 空 INPUT 用户输入 ASSIGN_ID 雪花 ASSIGN_UUID 唯一 UUID
      # 如需改为自增 需要将数据库表全部设置为自增
      idType: ASSIGN_ID


sa-token:
  #忽略的路径
  pathIgnores: /code/**, /auth/**, /test/**, /external/auth/getUserInfo, /external/embed/detail/**, /home/page/**, /matter/info/export, /sys/carousel/list, /entrepreneur/theory/list
  jwt-secret-key: abcdefghijklmnopqrstuvwxyz
  # 开启内网服务调用鉴权(不允许越过gateway访问内网服务 保障服务安全)
  #check-same-token: true
  # token 有效期（单位：秒） 默认30天，-1 代表永久有效
  timeout: 86400
  # token 最低活跃频率（单位：秒），如果 token 超过此时间没有访问系统就会被冻结，默认-1 代表不限制，永不冻结
  #active-timeout: -1
  # 是否允许同一账号多地同时登录 （为 true 时允许一起登录, 为 false 时新登录挤掉旧登录）
  #is-concurrent: true
  # 在多人登录同一账号时，是否共用一个 token （为 true 时所有登录共用一个 token, 为 false 时每次登录新建一个 token）
  #is-share: true
  # token 风格（默认可取值：uuid、simple-uuid、random-32、random-64、random-128、tik）
  #token-style: uuid
  # 是否输出操作日志
  #is-log: true

security:
  # 防止XSS攻击
  xss:
    enabled: true
    excludeUrls:
      - /api-user/notice
      - /flow/**
      - /tqt/api-flow/flow/**
      - /api-flow/flow/**
  # 不校验白名单
  ignore:
    whites: 
      - /api-auth/code
      - /api-auth/auth/**
      - /resource/sms/code
      - /*/v3/api-docs
      - /*/v2/api-docs
      - /*/error
      - /csrf
      - /doc.html
      - /webjars/**
      - /swagger-resources/**
      - /api-system/external/embed/detail/**
      - /api-auth/external/auth/**
      - /api-auth/sso/**
      - /api-system/home/page/**
      - /api-policy/home/page/**
      - /api-file/home/page/**
      - /api-policy/matter/info/export
      - /api-system/external/embed/detail/**
      - /api-quartz/test/**
      - /api-flow/login/**
      - /api-system/sys/carousel/list
      - /api-policy/entrepreneur/theory/list

swagger:
  enable: true
  butler:
    api-docs-path:  /v2/api-docs
    auto-generate-from-scg-routes: true
    ignore-routes:  api-eureka,api-generator,api-baidu

ribbon:
  ReadTimeout: 90000
  ConnectTimeout: 90000
  MaxAutoRetries: 0
  MaxAutoRetriesNextServer: 1
  OkToRetryOnAllOperations: false

feign:
  sentinel:
    enabled: true  #为feign整合sentinel

corsUrls: "*"', '548b501948c3a5a27412b85995157790', '2024-10-18 16:07:22.231', '2024-10-18 16:07:22.231', NULL, '192.168.10.2', '', '704f0050-72fe-4572-8e7d-40eb1e58aecd', '', NULL, NULL, 'yaml', NULL, '');
INSERT INTO "config_info" VALUES (17, 'auth.yaml', 'DEFAULT_GROUP', '#端口配置
server:
  port: 8000   #固定端口
  forward-headers-strategy: none  #客户端请求头获取策略

spring:
  datasource: 
    dynamic:
      # 设置默认的数据源或者数据源组,默认值即为 master
      primary: master
      datasource:
        # 主库数据源
        master:
          type: com.zaxxer.hikari.HikariDataSource
          driver-class-name: org.postgresql.Driver
          url: jdbc:postgresql://192.168.20.48:5432/bsp-user?useUnicode=true&characterEncoding=utf8&useSSL=true&autoReconnect=true&reWriteBatchedInserts=true
          username: root
          password: 123456
#       oracle:
#          type: ${spring.datasource.type}
#          driverClassName: oracle.jdbc.OracleDriver
#          url: ${datasource.system-oracle.url}
#          username: ${datasource.system-oracle.username}
#          password: ${datasource.system-oracle.password}
#        postgres:
#          type: ${spring.datasource.type}
#          driverClassName: org.postgresql.Driver
#          url: ${datasource.system-postgres.url}
#          username: ${datasource.system-postgres.username}
#          password: ${datasource.system-postgres.password}

  ################### redis 单机版 start ##########################
  redis:
    host: 192.168.20.48
    port: 6379
    password: xshl2023
    timeout: 6000
    database: 8
    lettuce:
      pool:
        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException
        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
      shutdown-timeout: 100ms
################### redis 单机版 end ##########################
#    cluster:
#      nodes: 130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #192.168.3.157:7000,192.168.3.158:7000,192.168.3.159:7000,192.168.3.157:7001,192.168.3.158:7001,192.168.3.159:7001
#    timeout: 1000 # 连接超时时间（毫秒）
#    lettuce:
#      pool:
#        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
#        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
#        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException
#        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
#      shutdown-timeout: 100ms

mybatis-plus:
  # 不支持多包, 如有需要可在注解配置 或 提升扫包等级
  # 例如 com.**.**.mapper
  mapperPackage: com.xshl.bsp.**.mapper
  # 对应的 XML 文件位置
  mapperLocations: classpath*:mappers/**/*Mapper.xml
  # 实体扫描，多个package用逗号或者分号分隔
  typeAliasesPackage: com.xshl.bsp.**.domain
  global-config:
    dbConfig:
      # 主键类型
      # AUTO 自增 NONE 空 INPUT 用户输入 ASSIGN_ID 雪花 ASSIGN_UUID 唯一 UUID
      # 如需改为自增 需要将数据库表全部设置为自增
      idType: ASSIGN_ID

logging:
  level:
    io.swagger.models.parameters.AbstractSerializableParameter: info #忽略swagger中的错误信息
    com.xshl.bsp.user.dao: info

#spring-security配置
# security:
#   oauth2:
#     ignored: /users-anon/**, /doc.html, /document.html, /users/save
#     token:
#       store:
#         type: redis

#设置最大超时时间
ribbon:  
  ServerListRefreshInterval: 10  #刷新服务列表源的间隔时间
  OkToRetryOnAllOperations: true
  MaxAutoRetries: 1
  MaxAutoRetriesNextServer: 1
  ReadTimeout: 16000  
  ConnectTimeout: 16000 


gdzw:
  tokenUrl: a

environment: dev

sa-token:
  #忽略的路径
  pathIgnores: /code/**, /auth/**, /external/auth/**, /sso/*
  # 开启内网服务调用鉴权(不允许越过gateway访问内网服务 保障服务安全)
  #check-same-token: true
  # token 有效期（单位：秒） 默认30天，-1 代表永久有效
  timeout: 1800
  # token 最低活跃频率（单位：秒），如果 token 超过此时间没有访问系统就会被冻结，默认-1 代表不限制，永不冻结
  #active-timeout: -1
  # 是否允许同一账号多地同时登录 （为 true 时允许一起登录, 为 false 时新登录挤掉旧登录）
  #is-concurrent: true
  # 在多人登录同一账号时，是否共用一个 token （为 true 时所有登录共用一个 token, 为 false 时每次登录新建一个 token）
  #is-share: true
  # token 风格（默认可取值：uuid、simple-uuid、random-32、random-64、random-128、tik）
  #token-style: uuid
  # 是否输出操作日志
  #is-log: true
  check-same-token: true


  # 安全配置
security:
  # 验证码
  captcha:
    # 是否开启验证码
    enabled: true
    # 验证码类型 math 数组计算 char 字符验证
    type: MATH
    # line 线段干扰 circle 圆圈干扰 shear 扭曲干扰
    category: CIRCLE
    # 数字验证码位数
    numberLength: 1
    # 字符验证码长度
    charLength: 4

# 用户配置
user:
  password:
    # 密码最大错误次数
    maxRetryCount: 15
    # 密码锁定时间（默认10分钟）
    lockTime: 10

justauth:
  enabled: true
  # 前端外网访问地址
  address: http://localhost:80
  type:
    #pai平台对接
    pai:
      server-url: http://114.255.170.237:8086/pai
      client-id: policy_manage_test
      client-secret: fk9lr3710u7iklxzqy6bsakbyi7x36e6
      redirect-uri: http://localhost
      sso-context-path: /pai-sso
      api-context-path: /pai-api
      token-url: /login/token
      user-info: /v1/sdk/user
      user-info-list: /v1/sdk/user/list/all
      org-tree-url: /v1/sdk/org/tree
      log-out-url: /login/logout
    tz-province:
      server-url: https://tzsyslpt.zwfw.taizhou.gov.cn/tzs-tyrz
      client-id: tzsjj-yqlb
      client-secret: 4P7ByloTY474
      redirect-uri: http://localhost
      token-url: /ticket/token
      user-info: /token/user
      log-out-url: 

logback:
  log:
    level: info
    path: /home/xshl/logs/auth

license:
  subject: license
  publicAlias: publicCert
  storePass: public_Xshl2024
  licensePath: /home/license.lic
  publicKeysStorePath: /home/publicCerts.keystore ', '6e3de8ad739a0a7825ef2ac20596f470', '2024-10-18 16:07:22.231', '2024-10-18 16:07:22.231', NULL, '192.168.10.2', '', '704f0050-72fe-4572-8e7d-40eb1e58aecd', '', NULL, NULL, 'yaml', NULL, '');
INSERT INTO "config_info" VALUES (18, 'user-center.yaml', 'DEFAULT_GROUP', '#端口配置
server:
  port: 8100   #固定端口
  forward-headers-strategy: none  #
  
spring:
  datasource: 
    dynamic:
      # 设置默认的数据源或者数据源组,默认值即为 master
      primary: master
      datasource:
        # 主库数据源
        master:
          type: com.zaxxer.hikari.HikariDataSource
          driver-class-name: org.postgresql.Driver
          url: jdbc:postgresql://192.168.20.48:5432/bsp-user?useUnicode=true&characterEncoding=utf8&useSSL=true&autoReconnect=true&reWriteBatchedInserts=true
          username: root
          password: 123456

  ################### redis 单机版 start ##########################
  redis:
    host: 192.168.20.48
    port: 6379
    password: xshl2023
    timeout: 6000
    database: 8
    lettuce:
      pool:
        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException
        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
      shutdown-timeout: 100ms
################### redis 单机版 end ##########################
#    cluster:
#      nodes: 130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #192.168.3.157:7000,192.168.3.158:7000,192.168.3.159:7000,192.168.3.157:7001,192.168.3.158:7001,192.168.3.159:7001
#    timeout: 1000 # 连接超时时间（毫秒）
#    lettuce:
#      pool:
#        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
#        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
#        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException
#        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
#      shutdown-timeout: 100ms

mybatis-plus:
  # 不支持多包, 如有需要可在注解配置 或 提升扫包等级
  # 例如 com.**.**.mapper
  mapperPackage: com.xshl.bsp.**.mapper
  # 对应的 XML 文件位置
  mapperLocations: classpath*:mappers/**/*Mapper.xml
  # 实体扫描，多个package用逗号或者分号分隔
  typeAliasesPackage: com.xshl.bsp.**.domain
  global-config:
    dbConfig:
      # 主键类型
      # AUTO 自增 NONE 空 INPUT 用户输入 ASSIGN_ID 雪花 ASSIGN_UUID 唯一 UUID
      # 如需改为自增 需要将数据库表全部设置为自增
      idType: ASSIGN_ID

logging:
  level:
    io.swagger.models.parameters.AbstractSerializableParameter: info #忽略swagger中的错误信息
    com.xshl.bsp: info
#配置日志输出
logback:
  log:
    level: INFO
    path: /home/xshl/logs/user-center


#设置最大超时时间
ribbon:  
  ServerListRefreshInterval: 10  #刷新服务列表源的间隔时间
  OkToRetryOnAllOperations: true
  MaxAutoRetries: 1
  MaxAutoRetriesNextServer: 1
  ReadTimeout: 16000  
  ConnectTimeout: 16000 

gdzw:
  tokenUrl: a

environment: dev

sa-token:
  #忽略的路径
  pathIgnores: /user/**, dept/**
  # token 有效期（单位：秒） 默认30天，-1 代表永久有效
  #timeout: 2592000
  # token 最低活跃频率（单位：秒），如果 token 超过此时间没有访问系统就会被冻结，默认-1 代表不限制，永不冻结
  #active-timeout: -1
  # 是否允许同一账号多地同时登录 （为 true 时允许一起登录, 为 false 时新登录挤掉旧登录）
  #is-concurrent: true
  # 在多人登录同一账号时，是否共用一个 token （为 true 时所有登录共用一个 token, 为 false 时每次登录新建一个 token）
  #is-share: true
  # token 风格（默认可取值：uuid、simple-uuid、random-32、random-64、random-128、tik）
  #token-style: uuid
  # 是否输出操作日志
  #is-log: true

flow:
  companyId: b482a6393faefd53783f9d093cd4ddff
  sync: true
 ', '2726e107b651bcbd6a90cc406f976178', '2024-10-18 16:07:22.231', '2024-10-18 16:07:22.231', NULL, '192.168.10.2', '', '704f0050-72fe-4572-8e7d-40eb1e58aecd', '', NULL, NULL, 'yaml', NULL, '');
INSERT INTO "config_info" VALUES (3, 'auth.yaml', 'DEFAULT_GROUP', '#端口配置
server:
  port: 8000   #固定端口
  forward-headers-strategy: none  #客户端请求头获取策略

spring:
  datasource: 
    dynamic:
      # 设置默认的数据源或者数据源组,默认值即为 master
      primary: master
      datasource:
        # 主库数据源
        master:
          type: com.zaxxer.hikari.HikariDataSource
          driver-class-name: org.postgresql.Driver
          url: jdbc:postgresql://192.168.20.48:5432/bsp-user?useUnicode=true&characterEncoding=utf8&useSSL=true&autoReconnect=true&reWriteBatchedInserts=true
          username: root
          password: 123456
#       oracle:
#          type: ${spring.datasource.type}
#          driverClassName: oracle.jdbc.OracleDriver
#          url: ${datasource.system-oracle.url}
#          username: ${datasource.system-oracle.username}
#          password: ${datasource.system-oracle.password}
#        postgres:
#          type: ${spring.datasource.type}
#          driverClassName: org.postgresql.Driver
#          url: ${datasource.system-postgres.url}
#          username: ${datasource.system-postgres.username}
#          password: ${datasource.system-postgres.password}

  ################### redis 单机版 start ##########################
  redis:
    host: 192.168.20.48
    port: 6379
    password: xshl2023
    timeout: 6000
    database: 8
    lettuce:
      pool:
        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException
        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
      shutdown-timeout: 100ms
################### redis 单机版 end ##########################
#    cluster:
#      nodes: 130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #192.168.3.157:7000,192.168.3.158:7000,192.168.3.159:7000,192.168.3.157:7001,192.168.3.158:7001,192.168.3.159:7001
#    timeout: 1000 # 连接超时时间（毫秒）
#    lettuce:
#      pool:
#        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
#        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
#        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException
#        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
#      shutdown-timeout: 100ms
', '3198c595ea4f8c4ddb3ec6423ef4ca72', '2024-10-18 11:50:56.986', '2024-10-21 09:39:49.117', 'nacos', '192.168.10.2', '', '876aed9e-d385-4cb1-9b39-63a28eaf0737', '', '', '', 'yaml', '', '');
INSERT INTO "config_info" VALUES (21, 'gateway.yaml', 'DEFAULT_GROUP', 'server:
  port: 9200 #端口
   
spring:
  cloud:
    gateway:
      requestLog: true
      discovery:
        locator:
          lowerCaseServiceId: true
          enabled: true
      routes:
       - id: api-user
         uri: lb://user-center
         order: 8001
         predicates:
         - Path=/api-user/**   
         filters:
         - StripPrefix=1 
       - id: api-auth
         uri: lb://auth
         order: 8002
         predicates:
         - Path=/api-auth/**
         filters:
         - PreserveHostHeader
         - StripPrefix=1  
       - id: api-file
         uri: lb://file
         order: 8003
         predicates:
         - Path=/api-file/**    
       - id: api-system
         uri: lb://system
         order: 8008
         predicates:
         - Path=/api-system/**
         filters:
         - StripPrefix=1 
  datasource: 
    dynamic:
      # 设置默认的数据源或者数据源组,默认值即为 master
      primary: master
      datasource:
        # 主库数据源
        master:
          type: com.zaxxer.hikari.HikariDataSource
          driver-class-name: org.postgresql.Driver
          url: jdbc:postgresql://172.21.143.186:5432/bsp-user?useUnicode=true&characterEncoding=utf8&useSSL=true&autoReconnect=true&reWriteBatchedInserts=true
          username: root
          password: 123456              

################### mysq end ##########################
  redis:
################### redis 单机版 start ########################## 
    host: 172.21.136.27
    port: 6379
    password: xshl2023
    timeout: 6000
    database: 8
    lettuce:
      pool:
        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException  
        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
      shutdown-timeout: 100ms
################### redis 单机版 end ##########################   
#    cluster:
#      nodes: 130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #192.168.3.157:7000,192.168.3.158:7000,192.168.3.159:7000,192.168.3.157:7001,192.168.3.158:7001,192.168.3.159:7001
#    timeout: 1000 # 连接超时时间（毫秒）
#    lettuce:
#      pool:
#        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
#        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
#        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException  
#        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
#      shutdown-timeout: 100ms
  
mybatis-plus:
  # 不支持多包, 如有需要可在注解配置 或 提升扫包等级
  # 例如 com.**.**.mapper
  mapperPackage: com.xshl.bsp.**.mapper
  # 对应的 XML 文件位置
  mapperLocations: classpath*:mappers/**/*Mapper.xml
  # 实体扫描，多个package用逗号或者分号分隔
  typeAliasesPackage: com.xshl.bsp.**.domain
  global-config:
    dbConfig:
      # 主键类型
      # AUTO 自增 NONE 空 INPUT 用户输入 ASSIGN_ID 雪花 ASSIGN_UUID 唯一 UUID
      # 如需改为自增 需要将数据库表全部设置为自增
      idType: ASSIGN_ID


sa-token:
  #忽略的路径
  pathIgnores: /code/**, /auth/**, /test/**, /external/auth/getUserInfo, /external/embed/detail/**, /home/page/**, /matter/info/export, /sys/carousel/list, /entrepreneur/theory/list
  jwt-secret-key: abcdefghijklmnopqrstuvwxyz
  # 开启内网服务调用鉴权(不允许越过gateway访问内网服务 保障服务安全)
  #check-same-token: true
  # token 有效期（单位：秒） 默认30天，-1 代表永久有效
  timeout: 86400
  # token 最低活跃频率（单位：秒），如果 token 超过此时间没有访问系统就会被冻结，默认-1 代表不限制，永不冻结
  #active-timeout: -1
  # 是否允许同一账号多地同时登录 （为 true 时允许一起登录, 为 false 时新登录挤掉旧登录）
  #is-concurrent: true
  # 在多人登录同一账号时，是否共用一个 token （为 true 时所有登录共用一个 token, 为 false 时每次登录新建一个 token）
  #is-share: true
  # token 风格（默认可取值：uuid、simple-uuid、random-32、random-64、random-128、tik）
  #token-style: uuid
  # 是否输出操作日志
  #is-log: true

security:
  # 防止XSS攻击
  xss:
    enabled: true
    excludeUrls:
      - /api-user/notice
      - /flow/**
      - /tqt/api-flow/flow/**
      - /api-flow/flow/**
  # 不校验白名单
  ignore:
    whites: 
      - /api-auth/code
      - /api-auth/auth/**
      - /resource/sms/code
      - /*/v3/api-docs
      - /*/v2/api-docs
      - /*/error
      - /csrf
      - /doc.html
      - /webjars/**
      - /swagger-resources/**
      - /api-system/external/embed/detail/**
      - /api-auth/external/auth/**
      - /api-auth/sso/**
      - /api-system/home/page/**
      - /api-policy/home/page/**
      - /api-file/home/page/**
      - /api-policy/matter/info/export
      - /api-system/external/embed/detail/**
      - /api-quartz/test/**
      - /api-flow/login/**
      - /api-system/sys/carousel/list
      - /api-policy/entrepreneur/theory/list

swagger:
  enable: true
  butler:
    api-docs-path:  /v2/api-docs
    auto-generate-from-scg-routes: true
    ignore-routes:  api-eureka,api-generator,api-baidu

ribbon:
  ReadTimeout: 90000
  ConnectTimeout: 90000
  MaxAutoRetries: 0
  MaxAutoRetriesNextServer: 1
  OkToRetryOnAllOperations: false

feign:
  sentinel:
    enabled: true  #为feign整合sentinel

corsUrls: "*"', '80972ba0adf33085895f39ef922063d9', '2024-10-25 11:18:46.423', '2024-10-25 11:20:32.143', 'nacos', '192.168.10.171', '', 'da36facd-d730-409b-ba05-f6f57a5f1edc', '', '', '', 'yaml', '', '');
INSERT INTO "config_info" VALUES (22, 'user-center.yaml', 'DEFAULT_GROUP', '#端口配置
server:
  port: 8100   #固定端口
  forward-headers-strategy: none  #
  
spring:
  datasource: 
    dynamic:
      # 设置默认的数据源或者数据源组,默认值即为 master
      primary: master
      datasource:
        # 主库数据源
        master:
          type: com.zaxxer.hikari.HikariDataSource
          driver-class-name: org.postgresql.Driver
          url: jdbc:postgresql://172.21.143.186:5432/bsp-user?useUnicode=true&characterEncoding=utf8&useSSL=true&autoReconnect=true&reWriteBatchedInserts=true
          username: root
          password: 123456

  ################### redis 单机版 start ##########################
  redis:
    host: 172.21.136.27
    port: 6379
    password: xshl2023
    timeout: 6000
    database: 8
    lettuce:
      pool:
        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException
        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
      shutdown-timeout: 100ms
################### redis 单机版 end ##########################
#    cluster:
#      nodes: 130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #192.168.3.157:7000,192.168.3.158:7000,192.168.3.159:7000,192.168.3.157:7001,192.168.3.158:7001,192.168.3.159:7001
#    timeout: 1000 # 连接超时时间（毫秒）
#    lettuce:
#      pool:
#        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
#        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
#        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException
#        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
#      shutdown-timeout: 100ms

mybatis-plus:
  # 不支持多包, 如有需要可在注解配置 或 提升扫包等级
  # 例如 com.**.**.mapper
  mapperPackage: com.xshl.bsp.**.mapper
  # 对应的 XML 文件位置
  mapperLocations: classpath*:mappers/**/*Mapper.xml
  # 实体扫描，多个package用逗号或者分号分隔
  typeAliasesPackage: com.xshl.bsp.**.domain
  global-config:
    dbConfig:
      # 主键类型
      # AUTO 自增 NONE 空 INPUT 用户输入 ASSIGN_ID 雪花 ASSIGN_UUID 唯一 UUID
      # 如需改为自增 需要将数据库表全部设置为自增
      idType: ASSIGN_ID

logging:
  level:
    io.swagger.models.parameters.AbstractSerializableParameter: info #忽略swagger中的错误信息
    com.xshl.bsp: info
#配置日志输出
logback:
  log:
    level: INFO
    path: /home/xshl/logs/user-center


#设置最大超时时间
ribbon:  
  ServerListRefreshInterval: 10  #刷新服务列表源的间隔时间
  OkToRetryOnAllOperations: true
  MaxAutoRetries: 1
  MaxAutoRetriesNextServer: 1
  ReadTimeout: 16000  
  ConnectTimeout: 16000 

gdzw:
  tokenUrl: a

environment: dev

sa-token:
  #忽略的路径
  pathIgnores: /user/**, dept/**
  # token 有效期（单位：秒） 默认30天，-1 代表永久有效
  #timeout: 2592000
  # token 最低活跃频率（单位：秒），如果 token 超过此时间没有访问系统就会被冻结，默认-1 代表不限制，永不冻结
  #active-timeout: -1
  # 是否允许同一账号多地同时登录 （为 true 时允许一起登录, 为 false 时新登录挤掉旧登录）
  #is-concurrent: true
  # 在多人登录同一账号时，是否共用一个 token （为 true 时所有登录共用一个 token, 为 false 时每次登录新建一个 token）
  #is-share: true
  # token 风格（默认可取值：uuid、simple-uuid、random-32、random-64、random-128、tik）
  #token-style: uuid
  # 是否输出操作日志
  #is-log: true

flow:
  companyId: b482a6393faefd53783f9d093cd4ddff
  sync: true
 ', '0f2736e786ec4c951f74d9421fae99e1', '2024-10-25 11:18:46.423', '2024-10-25 11:21:40.796', 'nacos', '192.168.10.171', '', 'da36facd-d730-409b-ba05-f6f57a5f1edc', '', '', '', 'yaml', '', '');
INSERT INTO "config_info" VALUES (20, 'common.yaml', 'DEFAULT_GROUP', 'spring:
  cloud:
    nacos:
      discovery:
        server-addr: 172.21.136.27:8848
        namespace: da36facd-d730-409b-ba05-f6f57a5f1edc  #命名空间 代指某个环境
  sentinel:
    transport:
      # 指定sentinel 控制台的地址
      dashboard: 172.21.136.27:8080
    eager: true
  jackson:
    mapper:
      ALLOW_EXPLICIT_PROPERTY_RENAMING: true
    deserialization:
      READ_DATE_TIMESTAMPS_AS_NANOSECONDS: false
    serialization:
      WRITE_DATE_TIMESTAMPS_AS_NANOSECONDS: false
      WRITE_DATES_AS_TIMESTAMPS: true
# api接口加密
api-decrypt:
  # 是否开启全局接口加密
  enabled: false
  # AES 加密头标识
  headerFlag: encrypt-key
  # 响应加密公钥 非对称算法的公私钥 如：SM2，RSA 使用者请自行更换
  # 对应前端解密私钥 MIIBVAIBADANBgkqhkiG9w0BAQEFAASCAT4wggE6AgEAAkEAmc3CuPiGL/LcIIm7zryCEIbl1SPzBkr75E2VMtxegyZ1lYRD+7TZGAPkvIsBcaMs6Nsy0L78n2qh+lIZMpLH8wIDAQABAkEAk82Mhz0tlv6IVCyIcw/s3f0E+WLmtPFyR9/WtV3Y5aaejUkU60JpX4m5xNR2VaqOLTZAYjW8Wy0aXr3zYIhhQQIhAMfqR9oFdYw1J9SsNc+CrhugAvKTi0+BF6VoL6psWhvbAiEAxPPNTmrkmrXwdm/pQQu3UOQmc2vCZ5tiKpW10CgJi8kCIFGkL6utxw93Ncj4exE/gPLvKcT+1Emnoox+O9kRXss5AiAMtYLJDaLEzPrAWcZeeSgSIzbL+ecokmFKSDDcRske6QIgSMkHedwND1olF8vlKsJUGK3BcdtM8w4Xq7BpSBwsloE=
  publicKey: MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAJnNwrj4hi/y3CCJu868ghCG5dUj8wZK++RNlTLcXoMmdZWEQ/u02RgD5LyLAXGjLOjbMtC+/J9qofpSGTKSx/MCAwEAAQ==
  # 请求解密私钥 非对称算法的公私钥 如：SM2，RSA 使用者请自行更换
  # 对应前端加密公钥 MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAKoR8mX0rGKLqzcWmOzbfj64K8ZIgOdHnzkXSOVOZbFu/TJhZ7rFAN+eaGkl3C4buccQd/EjEsj9ir7ijT7h96MCAwEAAQ==
  privateKey: MIIBVAIBADANBgkqhkiG9w0BAQEFAASCAT4wggE6AgEAAkEAqhHyZfSsYourNxaY7Nt+PrgrxkiA50efORdI5U5lsW79MmFnusUA355oaSXcLhu5xxB38SMSyP2KvuKNPuH3owIDAQABAkAfoiLyL+Z4lf4Myxk6xUDgLaWGximj20CUf+5BKKnlrK+Ed8gAkM0HqoTt2UZwA5E2MzS4EI2gjfQhz5X28uqxAiEA3wNFxfrCZlSZHb0gn2zDpWowcSxQAgiCstxGUoOqlW8CIQDDOerGKH5OmCJ4Z21v+F25WaHYPxCFMvwxpcw99EcvDQIgIdhDTIqD2jfYjPTY8Jj3EDGPbH2HHuffvflECt3Ek60CIQCFRlCkHpi7hthhYhovyloRYsM+IS9h/0BzlEAuO0ktMQIgSPT3aFAgJYwKpqRYKlLDVcflZFCKY7u3UP8iWi1Qw0Y=

sa-token:
  #jwt秘钥
  jwt-secret-key: abcdefghijklmnopqrstuvwxyz
  # token 名称（同时也是 cookie 名称）
  token-name: Authorization
  #如果是单体服务，这里设置为false，这个是校验服务访问是否从网关进入
  check-same-token: true
  autoRenew: true
  timeout: 1800', 'c1b7be9e7d7d2e49b29b40352b721b96', '2024-10-25 11:18:46.423', '2024-10-25 13:56:28.756', 'nacos', '192.168.10.171', '', 'da36facd-d730-409b-ba05-f6f57a5f1edc', '', '', '', 'yaml', '', '');
INSERT INTO "config_info" VALUES (23, 'auth.yaml', 'DEFAULT_GROUP', '#端口配置
server:
  port: 8000   #固定端口
  forward-headers-strategy: none  #客户端请求头获取策略

spring:
  datasource: 
    dynamic:
      # 设置默认的数据源或者数据源组,默认值即为 master
      primary: master
      datasource:
        # 主库数据源
        master:
          type: com.zaxxer.hikari.HikariDataSource
          driver-class-name: org.postgresql.Driver
          url: jdbc:postgresql://172.21.143.186:5432/bsp-user?useUnicode=true&characterEncoding=utf8&useSSL=true&autoReconnect=true&reWriteBatchedInserts=true
          username: root
          password: 123456
#       oracle:
#          type: ${spring.datasource.type}
#          driverClassName: oracle.jdbc.OracleDriver
#          url: ${datasource.system-oracle.url}
#          username: ${datasource.system-oracle.username}
#          password: ${datasource.system-oracle.password}
#        postgres:
#          type: ${spring.datasource.type}
#          driverClassName: org.postgresql.Driver
#          url: ${datasource.system-postgres.url}
#          username: ${datasource.system-postgres.username}
#          password: ${datasource.system-postgres.password}

  ################### redis 单机版 start ##########################
  redis:
    host: 172.21.136.27
    port: 6379
    password: xshl2023
    timeout: 6000
    database: 8
    lettuce:
      pool:
        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException
        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
      shutdown-timeout: 100ms
################### redis 单机版 end ##########################
#    cluster:
#      nodes: 130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #192.168.3.157:7000,192.168.3.158:7000,192.168.3.159:7000,192.168.3.157:7001,192.168.3.158:7001,192.168.3.159:7001
#    timeout: 1000 # 连接超时时间（毫秒）
#    lettuce:
#      pool:
#        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
#        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
#        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException
#        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
#      shutdown-timeout: 100ms
', '39555f788772aea76acbbc496f56e37e', '2024-10-25 11:18:46.423', '2024-10-25 11:21:11.536', 'nacos', '192.168.10.171', '', 'da36facd-d730-409b-ba05-f6f57a5f1edc', '', '', '', 'yaml', '', '');
COMMIT;

-- ----------------------------
-- Table structure for config_info_aggr
-- ----------------------------
DROP TABLE IF EXISTS "config_info_aggr" CASCADE;
CREATE TABLE "config_info_aggr" (
  "id" "pg_catalog"."int8" NOT NULL DEFAULT nextval('config_info_aggr_id_seq'::regclass),
  "data_id" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" NOT NULL,
  "group_id" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" NOT NULL,
  "datum_id" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" NOT NULL,
  "content" "pg_catalog"."text" COLLATE "pg_catalog"."default" NOT NULL,
  "gmt_modified" "pg_catalog"."timestamp" NOT NULL,
  "app_name" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "tenant_id" "pg_catalog"."varchar" COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "config_info_aggr"."id" IS 'id';
COMMENT ON COLUMN "config_info_aggr"."data_id" IS 'data_id';
COMMENT ON COLUMN "config_info_aggr"."group_id" IS 'group_id';
COMMENT ON COLUMN "config_info_aggr"."datum_id" IS 'datum_id';
COMMENT ON COLUMN "config_info_aggr"."content" IS '内容';
COMMENT ON COLUMN "config_info_aggr"."gmt_modified" IS '修改时间';
COMMENT ON COLUMN "config_info_aggr"."tenant_id" IS '租户字段';
COMMENT ON TABLE "config_info_aggr" IS '增加租户字段';

-- ----------------------------
-- Records of config_info_aggr
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for config_info_beta
-- ----------------------------
DROP TABLE IF EXISTS "config_info_beta" CASCADE;
CREATE TABLE "config_info_beta" (
  "id" "pg_catalog"."int8" NOT NULL DEFAULT nextval('config_info_beta_id_seq'::regclass),
  "data_id" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" NOT NULL,
  "group_id" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" NOT NULL,
  "app_name" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "content" "pg_catalog"."text" COLLATE "pg_catalog"."default" NOT NULL,
  "beta_ips" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "md5" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "gmt_create" "pg_catalog"."timestamp" NOT NULL,
  "gmt_modified" "pg_catalog"."timestamp" NOT NULL,
  "src_user" "pg_catalog"."text" COLLATE "pg_catalog"."default",
  "src_ip" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "tenant_id" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "encrypted_data_key" "pg_catalog"."text" COLLATE "pg_catalog"."default" NOT NULL
)
;
COMMENT ON COLUMN "config_info_beta"."id" IS 'id';
COMMENT ON COLUMN "config_info_beta"."data_id" IS 'data_id';
COMMENT ON COLUMN "config_info_beta"."group_id" IS 'group_id';
COMMENT ON COLUMN "config_info_beta"."app_name" IS 'app_name';
COMMENT ON COLUMN "config_info_beta"."content" IS 'content';
COMMENT ON COLUMN "config_info_beta"."beta_ips" IS 'betaIps';
COMMENT ON COLUMN "config_info_beta"."md5" IS 'md5';
COMMENT ON COLUMN "config_info_beta"."gmt_create" IS '创建时间';
COMMENT ON COLUMN "config_info_beta"."gmt_modified" IS '修改时间';
COMMENT ON COLUMN "config_info_beta"."src_user" IS 'source user';
COMMENT ON COLUMN "config_info_beta"."src_ip" IS 'source ip';
COMMENT ON COLUMN "config_info_beta"."tenant_id" IS '租户字段';
COMMENT ON COLUMN "config_info_beta"."encrypted_data_key" IS '秘钥';
COMMENT ON TABLE "config_info_beta" IS 'config_info_beta';

-- ----------------------------
-- Records of config_info_beta
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for config_info_tag
-- ----------------------------
DROP TABLE IF EXISTS "config_info_tag" CASCADE;
CREATE TABLE "config_info_tag" (
  "id" "pg_catalog"."int8" NOT NULL DEFAULT nextval('config_info_tag_id_seq'::regclass),
  "data_id" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" NOT NULL,
  "group_id" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" NOT NULL,
  "tenant_id" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "tag_id" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" NOT NULL,
  "app_name" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "content" "pg_catalog"."text" COLLATE "pg_catalog"."default" NOT NULL,
  "md5" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "gmt_create" "pg_catalog"."timestamp" NOT NULL,
  "gmt_modified" "pg_catalog"."timestamp" NOT NULL,
  "src_user" "pg_catalog"."text" COLLATE "pg_catalog"."default",
  "src_ip" "pg_catalog"."varchar" COLLATE "pg_catalog"."default"
)
;
COMMENT ON COLUMN "config_info_tag"."id" IS 'id';
COMMENT ON COLUMN "config_info_tag"."data_id" IS 'data_id';
COMMENT ON COLUMN "config_info_tag"."group_id" IS 'group_id';
COMMENT ON COLUMN "config_info_tag"."tenant_id" IS 'tenant_id';
COMMENT ON COLUMN "config_info_tag"."tag_id" IS 'tag_id';
COMMENT ON COLUMN "config_info_tag"."app_name" IS 'app_name';
COMMENT ON COLUMN "config_info_tag"."content" IS 'content';
COMMENT ON COLUMN "config_info_tag"."md5" IS 'md5';
COMMENT ON COLUMN "config_info_tag"."gmt_create" IS '创建时间';
COMMENT ON COLUMN "config_info_tag"."gmt_modified" IS '修改时间';
COMMENT ON COLUMN "config_info_tag"."src_user" IS 'source user';
COMMENT ON COLUMN "config_info_tag"."src_ip" IS 'source ip';
COMMENT ON TABLE "config_info_tag" IS 'config_info_tag';

-- ----------------------------
-- Records of config_info_tag
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for config_tags_relation
-- ----------------------------
DROP TABLE IF EXISTS "config_tags_relation" CASCADE;
CREATE TABLE "config_tags_relation" (
  "id" "pg_catalog"."int8" NOT NULL DEFAULT nextval('config_tags_relation_id_seq'::regclass),
  "tag_name" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" NOT NULL,
  "tag_type" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "data_id" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" NOT NULL,
  "group_id" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" NOT NULL,
  "tenant_id" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "nid" "pg_catalog"."int8" NOT NULL DEFAULT nextval('config_tags_relation_nid_seq'::regclass)
)
;
COMMENT ON COLUMN "config_tags_relation"."id" IS 'id';
COMMENT ON COLUMN "config_tags_relation"."tag_name" IS 'tag_name';
COMMENT ON COLUMN "config_tags_relation"."tag_type" IS 'tag_type';
COMMENT ON COLUMN "config_tags_relation"."data_id" IS 'data_id';
COMMENT ON COLUMN "config_tags_relation"."group_id" IS 'group_id';
COMMENT ON COLUMN "config_tags_relation"."tenant_id" IS 'tenant_id';
COMMENT ON TABLE "config_tags_relation" IS 'config_tag_relation';

-- ----------------------------
-- Records of config_tags_relation
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for group_capacity
-- ----------------------------
DROP TABLE IF EXISTS "group_capacity" CASCADE;
CREATE TABLE "group_capacity" (
  "id" "pg_catalog"."int8" NOT NULL DEFAULT nextval('group_capacity_id_seq'::regclass),
  "group_id" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" NOT NULL,
  "quota" "pg_catalog"."int4" NOT NULL,
  "usage" "pg_catalog"."int4" NOT NULL,
  "max_size" "pg_catalog"."int4" NOT NULL,
  "max_aggr_count" "pg_catalog"."int4" NOT NULL,
  "max_aggr_size" "pg_catalog"."int4" NOT NULL,
  "max_history_count" "pg_catalog"."int4" NOT NULL,
  "gmt_create" "pg_catalog"."timestamp" NOT NULL,
  "gmt_modified" "pg_catalog"."timestamp" NOT NULL
)
;
COMMENT ON COLUMN "group_capacity"."id" IS '主键ID';
COMMENT ON COLUMN "group_capacity"."group_id" IS 'Group ID，空字符表示整个集群';
COMMENT ON COLUMN "group_capacity"."quota" IS '配额，0表示使用默认值';
COMMENT ON COLUMN "group_capacity"."usage" IS '使用量';
COMMENT ON COLUMN "group_capacity"."max_size" IS '单个配置大小上限，单位为字节，0表示使用默认值';
COMMENT ON COLUMN "group_capacity"."max_aggr_count" IS '聚合子配置最大个数，，0表示使用默认值';
COMMENT ON COLUMN "group_capacity"."max_aggr_size" IS '单个聚合数据的子配置大小上限，单位为字节，0表示使用默认值';
COMMENT ON COLUMN "group_capacity"."max_history_count" IS '最大变更历史数量';
COMMENT ON COLUMN "group_capacity"."gmt_create" IS '创建时间';
COMMENT ON COLUMN "group_capacity"."gmt_modified" IS '修改时间';
COMMENT ON TABLE "group_capacity" IS '集群、各Group容量信息表';

-- ----------------------------
-- Records of group_capacity
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for his_config_info
-- ----------------------------
DROP TABLE IF EXISTS "his_config_info" CASCADE;
CREATE TABLE "his_config_info" (
  "id" "pg_catalog"."int8" NOT NULL,
  "nid" "pg_catalog"."int8" NOT NULL DEFAULT nextval('his_config_info_nid_seq'::regclass),
  "data_id" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" NOT NULL,
  "group_id" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" NOT NULL,
  "app_name" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "content" "pg_catalog"."text" COLLATE "pg_catalog"."default" NOT NULL,
  "md5" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "gmt_create" "pg_catalog"."timestamp" NOT NULL DEFAULT '2010-05-05 00:00:00'::timestamp without time zone,
  "gmt_modified" "pg_catalog"."timestamp" NOT NULL,
  "src_user" "pg_catalog"."text" COLLATE "pg_catalog"."default",
  "src_ip" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "op_type" "pg_catalog"."bpchar" COLLATE "pg_catalog"."default",
  "tenant_id" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "encrypted_data_key" "pg_catalog"."text" COLLATE "pg_catalog"."default" NOT NULL
)
;
COMMENT ON COLUMN "his_config_info"."app_name" IS 'app_name';
COMMENT ON COLUMN "his_config_info"."tenant_id" IS '租户字段';
COMMENT ON COLUMN "his_config_info"."encrypted_data_key" IS '秘钥';
COMMENT ON TABLE "his_config_info" IS '多租户改造';

-- ----------------------------
-- Records of his_config_info
-- ----------------------------
BEGIN;
INSERT INTO "his_config_info" VALUES (0, 1, 'common.yaml', 'DEFAULT_GROUP', '', 'pring:
  cloud:
    nacos:
      discovery:
        server-addr: 192.168.20.48:8848
        namespace: 876aed9e-d385-4cb1-9b39-63a28eaf0737  #命名空间 代指某个环境
  sentinel:
    transport:
      # 指定sentinel 控制台的地址
      dashboard: 192.168.20.94:8080
    eager: true
  jackson:
    mapper:
      ALLOW_EXPLICIT_PROPERTY_RENAMING: true
    deserialization:
      READ_DATE_TIMESTAMPS_AS_NANOSECONDS: false
    serialization:
      WRITE_DATE_TIMESTAMPS_AS_NANOSECONDS: false
      WRITE_DATES_AS_TIMESTAMPS: true
# api接口加密
api-decrypt:
  # 是否开启全局接口加密
  enabled: false
  # AES 加密头标识
  headerFlag: encrypt-key
  # 响应加密公钥 非对称算法的公私钥 如：SM2，RSA 使用者请自行更换
  # 对应前端解密私钥 MIIBVAIBADANBgkqhkiG9w0BAQEFAASCAT4wggE6AgEAAkEAmc3CuPiGL/LcIIm7zryCEIbl1SPzBkr75E2VMtxegyZ1lYRD+7TZGAPkvIsBcaMs6Nsy0L78n2qh+lIZMpLH8wIDAQABAkEAk82Mhz0tlv6IVCyIcw/s3f0E+WLmtPFyR9/WtV3Y5aaejUkU60JpX4m5xNR2VaqOLTZAYjW8Wy0aXr3zYIhhQQIhAMfqR9oFdYw1J9SsNc+CrhugAvKTi0+BF6VoL6psWhvbAiEAxPPNTmrkmrXwdm/pQQu3UOQmc2vCZ5tiKpW10CgJi8kCIFGkL6utxw93Ncj4exE/gPLvKcT+1Emnoox+O9kRXss5AiAMtYLJDaLEzPrAWcZeeSgSIzbL+ecokmFKSDDcRske6QIgSMkHedwND1olF8vlKsJUGK3BcdtM8w4Xq7BpSBwsloE=
  publicKey: MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAJnNwrj4hi/y3CCJu868ghCG5dUj8wZK++RNlTLcXoMmdZWEQ/u02RgD5LyLAXGjLOjbMtC+/J9qofpSGTKSx/MCAwEAAQ==
  # 请求解密私钥 非对称算法的公私钥 如：SM2，RSA 使用者请自行更换
  # 对应前端加密公钥 MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAKoR8mX0rGKLqzcWmOzbfj64K8ZIgOdHnzkXSOVOZbFu/TJhZ7rFAN+eaGkl3C4buccQd/EjEsj9ir7ijT7h96MCAwEAAQ==
  privateKey: MIIBVAIBADANBgkqhkiG9w0BAQEFAASCAT4wggE6AgEAAkEAqhHyZfSsYourNxaY7Nt+PrgrxkiA50efORdI5U5lsW79MmFnusUA355oaSXcLhu5xxB38SMSyP2KvuKNPuH3owIDAQABAkAfoiLyL+Z4lf4Myxk6xUDgLaWGximj20CUf+5BKKnlrK+Ed8gAkM0HqoTt2UZwA5E2MzS4EI2gjfQhz5X28uqxAiEA3wNFxfrCZlSZHb0gn2zDpWowcSxQAgiCstxGUoOqlW8CIQDDOerGKH5OmCJ4Z21v+F25WaHYPxCFMvwxpcw99EcvDQIgIdhDTIqD2jfYjPTY8Jj3EDGPbH2HHuffvflECt3Ek60CIQCFRlCkHpi7hthhYhovyloRYsM+IS9h/0BzlEAuO0ktMQIgSPT3aFAgJYwKpqRYKlLDVcflZFCKY7u3UP8iWi1Qw0Y=

sa-token:
  #jwt秘钥
  jwt-secret-key: abcdefghijklmnopqrstuvwxyz
  # token 名称（同时也是 cookie 名称）
  token-name: Authorization
  #如果是单体服务，这里设置为false，这个是校验服务访问是否从网关进入
  check-same-token: true
  autoRenew: true
  timeout: 1800', '3942a58ce2c9ade4012432221f330f4d', '2010-05-05 00:00:00', '2024-10-18 11:33:20.519', NULL, '192.168.10.2', 'I         ', '876aed9e-d385-4cb1-9b39-63a28eaf0737', '');
INSERT INTO "his_config_info" VALUES (0, 2, 'gateway.yaml', 'DEFAULT_GROUP', '', 'server:
  port: 9200 #端口
   
spring:
  cloud:
    gateway:
      requestLog: true
      discovery:
        locator:
          lowerCaseServiceId: true
          enabled: true
      routes:
       - id: api-user
         uri: lb://user-center
         order: 8001
         predicates:
         - Path=/api-user/**   
         filters:
         - StripPrefix=1 
       - id: api-auth
         uri: lb://auth
         order: 8002
         predicates:
         - Path=/api-auth/**
         filters:
         - PreserveHostHeader
         - StripPrefix=1  
       - id: api-file
         uri: lb://file
         order: 8003
         predicates:
         - Path=/api-file/**    
       - id: api-policy
         uri: lb://policy
         order: 8007
         predicates:
         - Path=/api-policy/**
         filters:
         - StripPrefix=1 
       - id: api-system
         uri: lb://system
         order: 8008
         predicates:
         - Path=/api-system/**
         filters:
         - StripPrefix=1 
       - id: api-mtc
         uri: lb://mtc
         order: 8009
         predicates:
         - Path=/api-mtc/**
         filters:
         - StripPrefix=1 
       - id: api-survey
         uri: lb://survey
         order: 8009
         predicates:
         - Path=/api-survey/**
         filters:
         - StripPrefix=1
       - id: api-flow
         uri: lb://flow
         order: 8009
         predicates:
         - Path=/api-flow/**
         filters:
         - StripPrefix=1 
       - id: api-apply
         uri: lb://apply
         order: 8009
         predicates:
         - Path=/api-apply/**
         filters:
         - StripPrefix=1
  datasource: 
    dynamic:
      # 设置默认的数据源或者数据源组,默认值即为 master
      primary: master
      datasource:
        # 主库数据源
        master:
          type: com.zaxxer.hikari.HikariDataSource
          driver-class-name: org.postgresql.Driver
          url: jdbc:postgresql://192.168.20.30:5432/bsp-user?useUnicode=true&characterEncoding=utf8&useSSL=true&autoReconnect=true&reWriteBatchedInserts=true
          username: postgres
          password: ''!@#xshl2024''              

################### mysq end ##########################
  redis:
################### redis 单机版 start ########################## 
    host: 192.168.20.30
    port: 6379
    password: xshl2023
    timeout: 6000
    database: 8
    lettuce:
      pool:
        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException  
        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
      shutdown-timeout: 100ms
################### redis 单机版 end ##########################   
#    cluster:
#      nodes: 130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #192.168.3.157:7000,192.168.3.158:7000,192.168.3.159:7000,192.168.3.157:7001,192.168.3.158:7001,192.168.3.159:7001
#    timeout: 1000 # 连接超时时间（毫秒）
#    lettuce:
#      pool:
#        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
#        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
#        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException  
#        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
#      shutdown-timeout: 100ms
  
mybatis-plus:
  # 不支持多包, 如有需要可在注解配置 或 提升扫包等级
  # 例如 com.**.**.mapper
  mapperPackage: com.xshl.bsp.**.mapper
  # 对应的 XML 文件位置
  mapperLocations: classpath*:mappers/**/*Mapper.xml
  # 实体扫描，多个package用逗号或者分号分隔
  typeAliasesPackage: com.xshl.bsp.**.domain
  global-config:
    dbConfig:
      # 主键类型
      # AUTO 自增 NONE 空 INPUT 用户输入 ASSIGN_ID 雪花 ASSIGN_UUID 唯一 UUID
      # 如需改为自增 需要将数据库表全部设置为自增
      idType: ASSIGN_ID


sa-token:
  #忽略的路径
  pathIgnores: /code/**, /auth/**, /test/**, /external/auth/getUserInfo, /external/embed/detail/**, /home/page/**, /matter/info/export, /sys/carousel/list, /entrepreneur/theory/list
  jwt-secret-key: abcdefghijklmnopqrstuvwxyz
  # 开启内网服务调用鉴权(不允许越过gateway访问内网服务 保障服务安全)
  #check-same-token: true
  # token 有效期（单位：秒） 默认30天，-1 代表永久有效
  timeout: 86400
  # token 最低活跃频率（单位：秒），如果 token 超过此时间没有访问系统就会被冻结，默认-1 代表不限制，永不冻结
  #active-timeout: -1
  # 是否允许同一账号多地同时登录 （为 true 时允许一起登录, 为 false 时新登录挤掉旧登录）
  #is-concurrent: true
  # 在多人登录同一账号时，是否共用一个 token （为 true 时所有登录共用一个 token, 为 false 时每次登录新建一个 token）
  #is-share: true
  # token 风格（默认可取值：uuid、simple-uuid、random-32、random-64、random-128、tik）
  #token-style: uuid
  # 是否输出操作日志
  #is-log: true

security:
  # 防止XSS攻击
  xss:
    enabled: true
    excludeUrls:
      - /api-user/notice
      - /flow/**
      - /tqt/api-flow/flow/**
      - /api-flow/flow/**
  # 不校验白名单
  ignore:
    whites: 
      - /api-auth/code
      - /api-auth/auth/**
      - /resource/sms/code
      - /*/v3/api-docs
      - /*/v2/api-docs
      - /*/error
      - /csrf
      - /doc.html
      - /webjars/**
      - /swagger-resources/**
      - /api-system/external/embed/detail/**
      - /api-auth/external/auth/**
      - /api-auth/sso/**
      - /api-system/home/page/**
      - /api-policy/home/page/**
      - /api-file/home/page/**
      - /api-policy/matter/info/export
      - /api-system/external/embed/detail/**
      - /api-quartz/test/**
      - /api-flow/login/**
      - /api-system/sys/carousel/list
      - /api-policy/entrepreneur/theory/list

swagger:
  enable: true
  butler:
    api-docs-path:  /v2/api-docs
    auto-generate-from-scg-routes: true
    ignore-routes:  api-eureka,api-generator,api-baidu

ribbon:
  ReadTimeout: 90000
  ConnectTimeout: 90000
  MaxAutoRetries: 0
  MaxAutoRetriesNextServer: 1
  OkToRetryOnAllOperations: false

feign:
  sentinel:
    enabled: true  #为feign整合sentinel

corsUrls: "*"', '15d9936225440d8e6aed8e20f3932635', '2010-05-05 00:00:00', '2024-10-18 11:50:14.957', NULL, '192.168.10.2', 'I         ', '876aed9e-d385-4cb1-9b39-63a28eaf0737', '');
INSERT INTO "his_config_info" VALUES (0, 3, 'auth.yaml', 'DEFAULT_GROUP', '', '#端口配置
server:
  port: 8000   #固定端口
  forward-headers-strategy: none  #客户端请求头获取策略

spring:
  datasource: 
    dynamic:
      # 设置默认的数据源或者数据源组,默认值即为 master
      primary: master
      datasource:
        # 主库数据源
        master:
          type: com.zaxxer.hikari.HikariDataSource
          driver-class-name: org.postgresql.Driver
          url: jdbc:postgresql://192.168.20.30:5432/bsp-user?useUnicode=true&characterEncoding=utf8&useSSL=true&autoReconnect=true&reWriteBatchedInserts=true
          username: postgres
          password: ''!@#xshl2024''
#       oracle:
#          type: ${spring.datasource.type}
#          driverClassName: oracle.jdbc.OracleDriver
#          url: ${datasource.system-oracle.url}
#          username: ${datasource.system-oracle.username}
#          password: ${datasource.system-oracle.password}
#        postgres:
#          type: ${spring.datasource.type}
#          driverClassName: org.postgresql.Driver
#          url: ${datasource.system-postgres.url}
#          username: ${datasource.system-postgres.username}
#          password: ${datasource.system-postgres.password}

  ################### redis 单机版 start ##########################
  redis:
    host: 192.168.20.30
    port: 6379
    password: xshl2023
    timeout: 6000
    database: 8
    lettuce:
      pool:
        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException
        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
      shutdown-timeout: 100ms
################### redis 单机版 end ##########################
#    cluster:
#      nodes: 130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #192.168.3.157:7000,192.168.3.158:7000,192.168.3.159:7000,192.168.3.157:7001,192.168.3.158:7001,192.168.3.159:7001
#    timeout: 1000 # 连接超时时间（毫秒）
#    lettuce:
#      pool:
#        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
#        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
#        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException
#        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
#      shutdown-timeout: 100ms

mybatis-plus:
  # 不支持多包, 如有需要可在注解配置 或 提升扫包等级
  # 例如 com.**.**.mapper
  mapperPackage: com.xshl.bsp.**.mapper
  # 对应的 XML 文件位置
  mapperLocations: classpath*:mappers/**/*Mapper.xml
  # 实体扫描，多个package用逗号或者分号分隔
  typeAliasesPackage: com.xshl.bsp.**.domain
  global-config:
    dbConfig:
      # 主键类型
      # AUTO 自增 NONE 空 INPUT 用户输入 ASSIGN_ID 雪花 ASSIGN_UUID 唯一 UUID
      # 如需改为自增 需要将数据库表全部设置为自增
      idType: ASSIGN_ID

logging:
  level:
    io.swagger.models.parameters.AbstractSerializableParameter: info #忽略swagger中的错误信息
    com.xshl.bsp.user.dao: info

#spring-security配置
# security:
#   oauth2:
#     ignored: /users-anon/**, /doc.html, /document.html, /users/save
#     token:
#       store:
#         type: redis

#设置最大超时时间
ribbon:  
  ServerListRefreshInterval: 10  #刷新服务列表源的间隔时间
  OkToRetryOnAllOperations: true
  MaxAutoRetries: 1
  MaxAutoRetriesNextServer: 1
  ReadTimeout: 16000  
  ConnectTimeout: 16000 


gdzw:
  tokenUrl: a

environment: dev

sa-token:
  #忽略的路径
  pathIgnores: /code/**, /auth/**, /external/auth/**, /sso/*
  # 开启内网服务调用鉴权(不允许越过gateway访问内网服务 保障服务安全)
  #check-same-token: true
  # token 有效期（单位：秒） 默认30天，-1 代表永久有效
  timeout: 1800
  # token 最低活跃频率（单位：秒），如果 token 超过此时间没有访问系统就会被冻结，默认-1 代表不限制，永不冻结
  #active-timeout: -1
  # 是否允许同一账号多地同时登录 （为 true 时允许一起登录, 为 false 时新登录挤掉旧登录）
  #is-concurrent: true
  # 在多人登录同一账号时，是否共用一个 token （为 true 时所有登录共用一个 token, 为 false 时每次登录新建一个 token）
  #is-share: true
  # token 风格（默认可取值：uuid、simple-uuid、random-32、random-64、random-128、tik）
  #token-style: uuid
  # 是否输出操作日志
  #is-log: true
  check-same-token: true


  # 安全配置
security:
  # 验证码
  captcha:
    # 是否开启验证码
    enabled: true
    # 验证码类型 math 数组计算 char 字符验证
    type: MATH
    # line 线段干扰 circle 圆圈干扰 shear 扭曲干扰
    category: CIRCLE
    # 数字验证码位数
    numberLength: 1
    # 字符验证码长度
    charLength: 4

# 用户配置
user:
  password:
    # 密码最大错误次数
    maxRetryCount: 15
    # 密码锁定时间（默认10分钟）
    lockTime: 10

justauth:
  enabled: true
  # 前端外网访问地址
  address: http://localhost:80
  type:
    #pai平台对接
    pai:
      server-url: http://114.255.170.237:8086/pai
      client-id: policy_manage_test
      client-secret: fk9lr3710u7iklxzqy6bsakbyi7x36e6
      redirect-uri: http://localhost
      sso-context-path: /pai-sso
      api-context-path: /pai-api
      token-url: /login/token
      user-info: /v1/sdk/user
      user-info-list: /v1/sdk/user/list/all
      org-tree-url: /v1/sdk/org/tree
      log-out-url: /login/logout
    tz-province:
      server-url: https://tzsyslpt.zwfw.taizhou.gov.cn/tzs-tyrz
      client-id: tzsjj-yqlb
      client-secret: 4P7ByloTY474
      redirect-uri: http://localhost
      token-url: /ticket/token
      user-info: /token/user
      log-out-url: 

logback:
  log:
    level: info
    path: /home/xshl/logs/auth

license:
  subject: license
  publicAlias: publicCert
  storePass: public_Xshl2024
  licensePath: /home/license.lic
  publicKeysStorePath: /home/publicCerts.keystore ', '38e6d6173d863afe8bff6d222fff3485', '2010-05-05 00:00:00', '2024-10-18 11:50:56.986', NULL, '192.168.10.2', 'I         ', '876aed9e-d385-4cb1-9b39-63a28eaf0737', '');
INSERT INTO "his_config_info" VALUES (0, 4, 'user-center.yaml', 'DEFAULT_GROUP', '', '#端口配置
server:
  port: 8100   #固定端口
  forward-headers-strategy: none  #
  
spring:
  datasource: 
    dynamic:
      # 设置默认的数据源或者数据源组,默认值即为 master
      primary: master
      datasource:
        # 主库数据源
        master:
          type: com.zaxxer.hikari.HikariDataSource
          driver-class-name: org.postgresql.Driver
          url: jdbc:postgresql://192.168.20.30:5432/bsp-user?useUnicode=true&characterEncoding=utf8&useSSL=true&autoReconnect=true&reWriteBatchedInserts=true
          username: postgres
          password: ''!@#xshl2024''

  ################### redis 单机版 start ##########################
  redis:
    host: 192.168.20.30
    port: 6379
    password: xshl2023
    timeout: 6000
    database: 8
    lettuce:
      pool:
        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException
        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
      shutdown-timeout: 100ms
################### redis 单机版 end ##########################
#    cluster:
#      nodes: 130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #192.168.3.157:7000,192.168.3.158:7000,192.168.3.159:7000,192.168.3.157:7001,192.168.3.158:7001,192.168.3.159:7001
#    timeout: 1000 # 连接超时时间（毫秒）
#    lettuce:
#      pool:
#        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
#        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
#        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException
#        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
#      shutdown-timeout: 100ms

mybatis-plus:
  # 不支持多包, 如有需要可在注解配置 或 提升扫包等级
  # 例如 com.**.**.mapper
  mapperPackage: com.xshl.bsp.**.mapper
  # 对应的 XML 文件位置
  mapperLocations: classpath*:mappers/**/*Mapper.xml
  # 实体扫描，多个package用逗号或者分号分隔
  typeAliasesPackage: com.xshl.bsp.**.domain
  global-config:
    dbConfig:
      # 主键类型
      # AUTO 自增 NONE 空 INPUT 用户输入 ASSIGN_ID 雪花 ASSIGN_UUID 唯一 UUID
      # 如需改为自增 需要将数据库表全部设置为自增
      idType: ASSIGN_ID

logging:
  level:
    io.swagger.models.parameters.AbstractSerializableParameter: info #忽略swagger中的错误信息
    com.xshl.bsp: info
#配置日志输出
logback:
  log:
    level: INFO
    path: /home/xshl/logs/user-center


#设置最大超时时间
ribbon:  
  ServerListRefreshInterval: 10  #刷新服务列表源的间隔时间
  OkToRetryOnAllOperations: true
  MaxAutoRetries: 1
  MaxAutoRetriesNextServer: 1
  ReadTimeout: 16000  
  ConnectTimeout: 16000 

gdzw:
  tokenUrl: a

environment: dev

sa-token:
  #忽略的路径
  pathIgnores: /user/**, dept/**
  # token 有效期（单位：秒） 默认30天，-1 代表永久有效
  #timeout: 2592000
  # token 最低活跃频率（单位：秒），如果 token 超过此时间没有访问系统就会被冻结，默认-1 代表不限制，永不冻结
  #active-timeout: -1
  # 是否允许同一账号多地同时登录 （为 true 时允许一起登录, 为 false 时新登录挤掉旧登录）
  #is-concurrent: true
  # 在多人登录同一账号时，是否共用一个 token （为 true 时所有登录共用一个 token, 为 false 时每次登录新建一个 token）
  #is-share: true
  # token 风格（默认可取值：uuid、simple-uuid、random-32、random-64、random-128、tik）
  #token-style: uuid
  # 是否输出操作日志
  #is-log: true

flow:
  companyId: b482a6393faefd53783f9d093cd4ddff
  sync: true
 ', 'fce5a3a89744755456fb079637a5d582', '2010-05-05 00:00:00', '2024-10-18 11:51:32.733', NULL, '192.168.10.2', 'I         ', '876aed9e-d385-4cb1-9b39-63a28eaf0737', '');
INSERT INTO "his_config_info" VALUES (1, 5, 'common.yaml', 'DEFAULT_GROUP', '', 'pring:
  cloud:
    nacos:
      discovery:
        server-addr: 192.168.20.48:8848
        namespace: 876aed9e-d385-4cb1-9b39-63a28eaf0737  #命名空间 代指某个环境
  sentinel:
    transport:
      # 指定sentinel 控制台的地址
      dashboard: 192.168.20.94:8080
    eager: true
  jackson:
    mapper:
      ALLOW_EXPLICIT_PROPERTY_RENAMING: true
    deserialization:
      READ_DATE_TIMESTAMPS_AS_NANOSECONDS: false
    serialization:
      WRITE_DATE_TIMESTAMPS_AS_NANOSECONDS: false
      WRITE_DATES_AS_TIMESTAMPS: true
# api接口加密
api-decrypt:
  # 是否开启全局接口加密
  enabled: false
  # AES 加密头标识
  headerFlag: encrypt-key
  # 响应加密公钥 非对称算法的公私钥 如：SM2，RSA 使用者请自行更换
  # 对应前端解密私钥 MIIBVAIBADANBgkqhkiG9w0BAQEFAASCAT4wggE6AgEAAkEAmc3CuPiGL/LcIIm7zryCEIbl1SPzBkr75E2VMtxegyZ1lYRD+7TZGAPkvIsBcaMs6Nsy0L78n2qh+lIZMpLH8wIDAQABAkEAk82Mhz0tlv6IVCyIcw/s3f0E+WLmtPFyR9/WtV3Y5aaejUkU60JpX4m5xNR2VaqOLTZAYjW8Wy0aXr3zYIhhQQIhAMfqR9oFdYw1J9SsNc+CrhugAvKTi0+BF6VoL6psWhvbAiEAxPPNTmrkmrXwdm/pQQu3UOQmc2vCZ5tiKpW10CgJi8kCIFGkL6utxw93Ncj4exE/gPLvKcT+1Emnoox+O9kRXss5AiAMtYLJDaLEzPrAWcZeeSgSIzbL+ecokmFKSDDcRske6QIgSMkHedwND1olF8vlKsJUGK3BcdtM8w4Xq7BpSBwsloE=
  publicKey: MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAJnNwrj4hi/y3CCJu868ghCG5dUj8wZK++RNlTLcXoMmdZWEQ/u02RgD5LyLAXGjLOjbMtC+/J9qofpSGTKSx/MCAwEAAQ==
  # 请求解密私钥 非对称算法的公私钥 如：SM2，RSA 使用者请自行更换
  # 对应前端加密公钥 MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAKoR8mX0rGKLqzcWmOzbfj64K8ZIgOdHnzkXSOVOZbFu/TJhZ7rFAN+eaGkl3C4buccQd/EjEsj9ir7ijT7h96MCAwEAAQ==
  privateKey: MIIBVAIBADANBgkqhkiG9w0BAQEFAASCAT4wggE6AgEAAkEAqhHyZfSsYourNxaY7Nt+PrgrxkiA50efORdI5U5lsW79MmFnusUA355oaSXcLhu5xxB38SMSyP2KvuKNPuH3owIDAQABAkAfoiLyL+Z4lf4Myxk6xUDgLaWGximj20CUf+5BKKnlrK+Ed8gAkM0HqoTt2UZwA5E2MzS4EI2gjfQhz5X28uqxAiEA3wNFxfrCZlSZHb0gn2zDpWowcSxQAgiCstxGUoOqlW8CIQDDOerGKH5OmCJ4Z21v+F25WaHYPxCFMvwxpcw99EcvDQIgIdhDTIqD2jfYjPTY8Jj3EDGPbH2HHuffvflECt3Ek60CIQCFRlCkHpi7hthhYhovyloRYsM+IS9h/0BzlEAuO0ktMQIgSPT3aFAgJYwKpqRYKlLDVcflZFCKY7u3UP8iWi1Qw0Y=

sa-token:
  #jwt秘钥
  jwt-secret-key: abcdefghijklmnopqrstuvwxyz
  # token 名称（同时也是 cookie 名称）
  token-name: Authorization
  #如果是单体服务，这里设置为false，这个是校验服务访问是否从网关进入
  check-same-token: true
  autoRenew: true
  timeout: 1800', '3942a58ce2c9ade4012432221f330f4d', '2010-05-05 00:00:00', '2024-10-18 14:49:36.279', 'nacos', '192.168.10.2', 'U         ', '876aed9e-d385-4cb1-9b39-63a28eaf0737', '');
INSERT INTO "his_config_info" VALUES (2, 6, 'gateway.yaml', 'DEFAULT_GROUP', '', 'server:
  port: 9200 #端口
   
spring:
  cloud:
    gateway:
      requestLog: true
      discovery:
        locator:
          lowerCaseServiceId: true
          enabled: true
      routes:
       - id: api-user
         uri: lb://user-center
         order: 8001
         predicates:
         - Path=/api-user/**   
         filters:
         - StripPrefix=1 
       - id: api-auth
         uri: lb://auth
         order: 8002
         predicates:
         - Path=/api-auth/**
         filters:
         - PreserveHostHeader
         - StripPrefix=1  
       - id: api-file
         uri: lb://file
         order: 8003
         predicates:
         - Path=/api-file/**    
       - id: api-policy
         uri: lb://policy
         order: 8007
         predicates:
         - Path=/api-policy/**
         filters:
         - StripPrefix=1 
       - id: api-system
         uri: lb://system
         order: 8008
         predicates:
         - Path=/api-system/**
         filters:
         - StripPrefix=1 
       - id: api-mtc
         uri: lb://mtc
         order: 8009
         predicates:
         - Path=/api-mtc/**
         filters:
         - StripPrefix=1 
       - id: api-survey
         uri: lb://survey
         order: 8009
         predicates:
         - Path=/api-survey/**
         filters:
         - StripPrefix=1
       - id: api-flow
         uri: lb://flow
         order: 8009
         predicates:
         - Path=/api-flow/**
         filters:
         - StripPrefix=1 
       - id: api-apply
         uri: lb://apply
         order: 8009
         predicates:
         - Path=/api-apply/**
         filters:
         - StripPrefix=1
  datasource: 
    dynamic:
      # 设置默认的数据源或者数据源组,默认值即为 master
      primary: master
      datasource:
        # 主库数据源
        master:
          type: com.zaxxer.hikari.HikariDataSource
          driver-class-name: org.postgresql.Driver
          url: jdbc:postgresql://192.168.20.30:5432/bsp-user?useUnicode=true&characterEncoding=utf8&useSSL=true&autoReconnect=true&reWriteBatchedInserts=true
          username: postgres
          password: ''!@#xshl2024''              

################### mysq end ##########################
  redis:
################### redis 单机版 start ########################## 
    host: 192.168.20.30
    port: 6379
    password: xshl2023
    timeout: 6000
    database: 8
    lettuce:
      pool:
        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException  
        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
      shutdown-timeout: 100ms
################### redis 单机版 end ##########################   
#    cluster:
#      nodes: 130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #192.168.3.157:7000,192.168.3.158:7000,192.168.3.159:7000,192.168.3.157:7001,192.168.3.158:7001,192.168.3.159:7001
#    timeout: 1000 # 连接超时时间（毫秒）
#    lettuce:
#      pool:
#        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
#        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
#        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException  
#        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
#      shutdown-timeout: 100ms
  
mybatis-plus:
  # 不支持多包, 如有需要可在注解配置 或 提升扫包等级
  # 例如 com.**.**.mapper
  mapperPackage: com.xshl.bsp.**.mapper
  # 对应的 XML 文件位置
  mapperLocations: classpath*:mappers/**/*Mapper.xml
  # 实体扫描，多个package用逗号或者分号分隔
  typeAliasesPackage: com.xshl.bsp.**.domain
  global-config:
    dbConfig:
      # 主键类型
      # AUTO 自增 NONE 空 INPUT 用户输入 ASSIGN_ID 雪花 ASSIGN_UUID 唯一 UUID
      # 如需改为自增 需要将数据库表全部设置为自增
      idType: ASSIGN_ID


sa-token:
  #忽略的路径
  pathIgnores: /code/**, /auth/**, /test/**, /external/auth/getUserInfo, /external/embed/detail/**, /home/page/**, /matter/info/export, /sys/carousel/list, /entrepreneur/theory/list
  jwt-secret-key: abcdefghijklmnopqrstuvwxyz
  # 开启内网服务调用鉴权(不允许越过gateway访问内网服务 保障服务安全)
  #check-same-token: true
  # token 有效期（单位：秒） 默认30天，-1 代表永久有效
  timeout: 86400
  # token 最低活跃频率（单位：秒），如果 token 超过此时间没有访问系统就会被冻结，默认-1 代表不限制，永不冻结
  #active-timeout: -1
  # 是否允许同一账号多地同时登录 （为 true 时允许一起登录, 为 false 时新登录挤掉旧登录）
  #is-concurrent: true
  # 在多人登录同一账号时，是否共用一个 token （为 true 时所有登录共用一个 token, 为 false 时每次登录新建一个 token）
  #is-share: true
  # token 风格（默认可取值：uuid、simple-uuid、random-32、random-64、random-128、tik）
  #token-style: uuid
  # 是否输出操作日志
  #is-log: true

security:
  # 防止XSS攻击
  xss:
    enabled: true
    excludeUrls:
      - /api-user/notice
      - /flow/**
      - /tqt/api-flow/flow/**
      - /api-flow/flow/**
  # 不校验白名单
  ignore:
    whites: 
      - /api-auth/code
      - /api-auth/auth/**
      - /resource/sms/code
      - /*/v3/api-docs
      - /*/v2/api-docs
      - /*/error
      - /csrf
      - /doc.html
      - /webjars/**
      - /swagger-resources/**
      - /api-system/external/embed/detail/**
      - /api-auth/external/auth/**
      - /api-auth/sso/**
      - /api-system/home/page/**
      - /api-policy/home/page/**
      - /api-file/home/page/**
      - /api-policy/matter/info/export
      - /api-system/external/embed/detail/**
      - /api-quartz/test/**
      - /api-flow/login/**
      - /api-system/sys/carousel/list
      - /api-policy/entrepreneur/theory/list

swagger:
  enable: true
  butler:
    api-docs-path:  /v2/api-docs
    auto-generate-from-scg-routes: true
    ignore-routes:  api-eureka,api-generator,api-baidu

ribbon:
  ReadTimeout: 90000
  ConnectTimeout: 90000
  MaxAutoRetries: 0
  MaxAutoRetriesNextServer: 1
  OkToRetryOnAllOperations: false

feign:
  sentinel:
    enabled: true  #为feign整合sentinel

corsUrls: "*"', '15d9936225440d8e6aed8e20f3932635', '2010-05-05 00:00:00', '2024-10-18 14:49:50.414', 'nacos', '192.168.10.2', 'U         ', '876aed9e-d385-4cb1-9b39-63a28eaf0737', '');
INSERT INTO "his_config_info" VALUES (2, 7, 'gateway.yaml', 'DEFAULT_GROUP', '', 'server:
  port: 9200 #端口
   
spring:
  cloud:
    gateway:
      requestLog: true
      discovery:
        locator:
          lowerCaseServiceId: true
          enabled: true
      routes:
       - id: api-user
         uri: lb://user-center
         order: 8001
         predicates:
         - Path=/api-user/**   
         filters:
         - StripPrefix=1 
       - id: api-auth
         uri: lb://auth
         order: 8002
         predicates:
         - Path=/api-auth/**
         filters:
         - PreserveHostHeader
         - StripPrefix=1  
       - id: api-file
         uri: lb://file
         order: 8003
         predicates:
         - Path=/api-file/**    
       - id: api-policy
         uri: lb://policy
         order: 8007
         predicates:
         - Path=/api-policy/**
         filters:
         - StripPrefix=1 
       - id: api-system
         uri: lb://system
         order: 8008
         predicates:
         - Path=/api-system/**
         filters:
         - StripPrefix=1 
       - id: api-mtc
         uri: lb://mtc
         order: 8009
         predicates:
         - Path=/api-mtc/**
         filters:
         - StripPrefix=1 
       - id: api-survey
         uri: lb://survey
         order: 8009
         predicates:
         - Path=/api-survey/**
         filters:
         - StripPrefix=1
       - id: api-flow
         uri: lb://flow
         order: 8009
         predicates:
         - Path=/api-flow/**
         filters:
         - StripPrefix=1 
       - id: api-apply
         uri: lb://apply
         order: 8009
         predicates:
         - Path=/api-apply/**
         filters:
         - StripPrefix=1
  datasource: 
    dynamic:
      # 设置默认的数据源或者数据源组,默认值即为 master
      primary: master
      datasource:
        # 主库数据源
        master:
          type: com.zaxxer.hikari.HikariDataSource
          driver-class-name: org.postgresql.Driver
          url: jdbc:postgresql://192.168.20.30:5432/bsp-user?useUnicode=true&characterEncoding=utf8&useSSL=true&autoReconnect=true&reWriteBatchedInserts=true
          username: postgres
          password: ''!@#xshl2024''              

################### mysq end ##########################
  redis:
################### redis 单机版 start ########################## 
    host: 192.168.20.30
    port: 6379
    password: xshl2023
    timeout: 6000
    database: 8
    lettuce:
      pool:
        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException  
        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
      shutdown-timeout: 100ms
################### redis 单机版 end ##########################   
#    cluster:
#      nodes: 130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #192.168.3.157:7000,192.168.3.158:7000,192.168.3.159:7000,192.168.3.157:7001,192.168.3.158:7001,192.168.3.159:7001
#    timeout: 1000 # 连接超时时间（毫秒）
#    lettuce:
#      pool:
#        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
#        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
#        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException  
#        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
#      shutdown-timeout: 100ms
  
mybatis-plus:
  # 不支持多包, 如有需要可在注解配置 或 提升扫包等级
  # 例如 com.**.**.mapper
  mapperPackage: com.xshl.bsp.**.mapper
  # 对应的 XML 文件位置
  mapperLocations: classpath*:mappers/**/*Mapper.xml
  # 实体扫描，多个package用逗号或者分号分隔
  typeAliasesPackage: com.xshl.bsp.**.domain
  global-config:
    dbConfig:
      # 主键类型
      # AUTO 自增 NONE 空 INPUT 用户输入 ASSIGN_ID 雪花 ASSIGN_UUID 唯一 UUID
      # 如需改为自增 需要将数据库表全部设置为自增
      idType: ASSIGN_ID


sa-token:
  #忽略的路径
  pathIgnores: /code/**, /auth/**, /test/**, /external/auth/getUserInfo, /external/embed/detail/**, /home/page/**, /matter/info/export, /sys/carousel/list, /entrepreneur/theory/list
  jwt-secret-key: abcdefghijklmnopqrstuvwxyz
  # 开启内网服务调用鉴权(不允许越过gateway访问内网服务 保障服务安全)
  #check-same-token: true
  # token 有效期（单位：秒） 默认30天，-1 代表永久有效
  timeout: 86400
  # token 最低活跃频率（单位：秒），如果 token 超过此时间没有访问系统就会被冻结，默认-1 代表不限制，永不冻结
  #active-timeout: -1
  # 是否允许同一账号多地同时登录 （为 true 时允许一起登录, 为 false 时新登录挤掉旧登录）
  #is-concurrent: true
  # 在多人登录同一账号时，是否共用一个 token （为 true 时所有登录共用一个 token, 为 false 时每次登录新建一个 token）
  #is-share: true
  # token 风格（默认可取值：uuid、simple-uuid、random-32、random-64、random-128、tik）
  #token-style: uuid
  # 是否输出操作日志
  #is-log: true

security:
  # 防止XSS攻击
  xss:
    enabled: true
    excludeUrls:
      - /api-user/notice
      - /flow/**
      - /tqt/api-flow/flow/**
      - /api-flow/flow/**
  # 不校验白名单
  ignore:
    whites: 
      - /api-auth/code
      - /api-auth/auth/**
      - /resource/sms/code
      - /*/v3/api-docs
      - /*/v2/api-docs
      - /*/error
      - /csrf
      - /doc.html
      - /webjars/**
      - /swagger-resources/**
      - /api-system/external/embed/detail/**
      - /api-auth/external/auth/**
      - /api-auth/sso/**
      - /api-system/home/page/**
      - /api-policy/home/page/**
      - /api-file/home/page/**
      - /api-policy/matter/info/export
      - /api-system/external/embed/detail/**
      - /api-quartz/test/**
      - /api-flow/login/**
      - /api-system/sys/carousel/list
      - /api-policy/entrepreneur/theory/list

swagger:
  enable: true
  butler:
    api-docs-path:  /v2/api-docs
    auto-generate-from-scg-routes: true
    ignore-routes:  api-eureka,api-generator,api-baidu

ribbon:
  ReadTimeout: 90000
  ConnectTimeout: 90000
  MaxAutoRetries: 0
  MaxAutoRetriesNextServer: 1
  OkToRetryOnAllOperations: false

feign:
  sentinel:
    enabled: true  #为feign整合sentinel

corsUrls: "*"', '15d9936225440d8e6aed8e20f3932635', '2010-05-05 00:00:00', '2024-10-18 14:52:20.2', 'nacos', '192.168.10.2', 'U         ', '876aed9e-d385-4cb1-9b39-63a28eaf0737', '');
INSERT INTO "his_config_info" VALUES (0, 8, 'auth.yaml', 'DEFAULT_GROUP', '', '#端口配置
server:
  port: 8000   #固定端口
  forward-headers-strategy: none  #客户端请求头获取策略

spring:
  datasource: 
    dynamic:
      # 设置默认的数据源或者数据源组,默认值即为 master
      primary: master
      datasource:
        # 主库数据源
        master:
          type: com.zaxxer.hikari.HikariDataSource
          driver-class-name: org.postgresql.Driver
          url: jdbc:postgresql://192.168.20.30:5432/bsp-user?useUnicode=true&characterEncoding=utf8&useSSL=true&autoReconnect=true&reWriteBatchedInserts=true
          username: postgres
          password: ''!@#xshl2024''
#       oracle:
#          type: ${spring.datasource.type}
#          driverClassName: oracle.jdbc.OracleDriver
#          url: ${datasource.system-oracle.url}
#          username: ${datasource.system-oracle.username}
#          password: ${datasource.system-oracle.password}
#        postgres:
#          type: ${spring.datasource.type}
#          driverClassName: org.postgresql.Driver
#          url: ${datasource.system-postgres.url}
#          username: ${datasource.system-postgres.username}
#          password: ${datasource.system-postgres.password}

  ################### redis 单机版 start ##########################
  redis:
    host: 192.168.20.30
    port: 6379
    password: xshl2023
    timeout: 6000
    database: 8
    lettuce:
      pool:
        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException
        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
      shutdown-timeout: 100ms
################### redis 单机版 end ##########################
#    cluster:
#      nodes: 130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #192.168.3.157:7000,192.168.3.158:7000,192.168.3.159:7000,192.168.3.157:7001,192.168.3.158:7001,192.168.3.159:7001
#    timeout: 1000 # 连接超时时间（毫秒）
#    lettuce:
#      pool:
#        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
#        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
#        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException
#        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
#      shutdown-timeout: 100ms

mybatis-plus:
  # 不支持多包, 如有需要可在注解配置 或 提升扫包等级
  # 例如 com.**.**.mapper
  mapperPackage: com.xshl.bsp.**.mapper
  # 对应的 XML 文件位置
  mapperLocations: classpath*:mappers/**/*Mapper.xml
  # 实体扫描，多个package用逗号或者分号分隔
  typeAliasesPackage: com.xshl.bsp.**.domain
  global-config:
    dbConfig:
      # 主键类型
      # AUTO 自增 NONE 空 INPUT 用户输入 ASSIGN_ID 雪花 ASSIGN_UUID 唯一 UUID
      # 如需改为自增 需要将数据库表全部设置为自增
      idType: ASSIGN_ID

logging:
  level:
    io.swagger.models.parameters.AbstractSerializableParameter: info #忽略swagger中的错误信息
    com.xshl.bsp.user.dao: info

#spring-security配置
# security:
#   oauth2:
#     ignored: /users-anon/**, /doc.html, /document.html, /users/save
#     token:
#       store:
#         type: redis

#设置最大超时时间
ribbon:  
  ServerListRefreshInterval: 10  #刷新服务列表源的间隔时间
  OkToRetryOnAllOperations: true
  MaxAutoRetries: 1
  MaxAutoRetriesNextServer: 1
  ReadTimeout: 16000  
  ConnectTimeout: 16000 


gdzw:
  tokenUrl: a

environment: dev

sa-token:
  #忽略的路径
  pathIgnores: /code/**, /auth/**, /external/auth/**, /sso/*
  # 开启内网服务调用鉴权(不允许越过gateway访问内网服务 保障服务安全)
  #check-same-token: true
  # token 有效期（单位：秒） 默认30天，-1 代表永久有效
  timeout: 1800
  # token 最低活跃频率（单位：秒），如果 token 超过此时间没有访问系统就会被冻结，默认-1 代表不限制，永不冻结
  #active-timeout: -1
  # 是否允许同一账号多地同时登录 （为 true 时允许一起登录, 为 false 时新登录挤掉旧登录）
  #is-concurrent: true
  # 在多人登录同一账号时，是否共用一个 token （为 true 时所有登录共用一个 token, 为 false 时每次登录新建一个 token）
  #is-share: true
  # token 风格（默认可取值：uuid、simple-uuid、random-32、random-64、random-128、tik）
  #token-style: uuid
  # 是否输出操作日志
  #is-log: true
  check-same-token: true


  # 安全配置
security:
  # 验证码
  captcha:
    # 是否开启验证码
    enabled: true
    # 验证码类型 math 数组计算 char 字符验证
    type: MATH
    # line 线段干扰 circle 圆圈干扰 shear 扭曲干扰
    category: CIRCLE
    # 数字验证码位数
    numberLength: 1
    # 字符验证码长度
    charLength: 4

# 用户配置
user:
  password:
    # 密码最大错误次数
    maxRetryCount: 15
    # 密码锁定时间（默认10分钟）
    lockTime: 10

justauth:
  enabled: true
  # 前端外网访问地址
  address: http://localhost:80
  type:
    #pai平台对接
    pai:
      server-url: http://114.255.170.237:8086/pai
      client-id: policy_manage_test
      client-secret: fk9lr3710u7iklxzqy6bsakbyi7x36e6
      redirect-uri: http://localhost
      sso-context-path: /pai-sso
      api-context-path: /pai-api
      token-url: /login/token
      user-info: /v1/sdk/user
      user-info-list: /v1/sdk/user/list/all
      org-tree-url: /v1/sdk/org/tree
      log-out-url: /login/logout
    tz-province:
      server-url: https://tzsyslpt.zwfw.taizhou.gov.cn/tzs-tyrz
      client-id: tzsjj-yqlb
      client-secret: 4P7ByloTY474
      redirect-uri: http://localhost
      token-url: /ticket/token
      user-info: /token/user
      log-out-url: 

logback:
  log:
    level: info
    path: /home/xshl/logs/auth

license:
  subject: license
  publicAlias: publicCert
  storePass: public_Xshl2024
  licensePath: /home/license.lic
  publicKeysStorePath: /home/publicCerts.keystore ', '38e6d6173d863afe8bff6d222fff3485', '2010-05-05 00:00:00', '2024-10-18 15:06:57.172', NULL, '192.168.10.2', 'I         ', '704f0050-72fe-4572-8e7d-40eb1e58aecd', '');
INSERT INTO "his_config_info" VALUES (0, 9, 'user-center.yaml', 'DEFAULT_GROUP', '', '#端口配置
server:
  port: 8100   #固定端口
  forward-headers-strategy: none  #
  
spring:
  datasource: 
    dynamic:
      # 设置默认的数据源或者数据源组,默认值即为 master
      primary: master
      datasource:
        # 主库数据源
        master:
          type: com.zaxxer.hikari.HikariDataSource
          driver-class-name: org.postgresql.Driver
          url: jdbc:postgresql://192.168.20.30:5432/bsp-user?useUnicode=true&characterEncoding=utf8&useSSL=true&autoReconnect=true&reWriteBatchedInserts=true
          username: postgres
          password: ''!@#xshl2024''

  ################### redis 单机版 start ##########################
  redis:
    host: 192.168.20.30
    port: 6379
    password: xshl2023
    timeout: 6000
    database: 8
    lettuce:
      pool:
        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException
        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
      shutdown-timeout: 100ms
################### redis 单机版 end ##########################
#    cluster:
#      nodes: 130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #192.168.3.157:7000,192.168.3.158:7000,192.168.3.159:7000,192.168.3.157:7001,192.168.3.158:7001,192.168.3.159:7001
#    timeout: 1000 # 连接超时时间（毫秒）
#    lettuce:
#      pool:
#        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
#        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
#        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException
#        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
#      shutdown-timeout: 100ms

mybatis-plus:
  # 不支持多包, 如有需要可在注解配置 或 提升扫包等级
  # 例如 com.**.**.mapper
  mapperPackage: com.xshl.bsp.**.mapper
  # 对应的 XML 文件位置
  mapperLocations: classpath*:mappers/**/*Mapper.xml
  # 实体扫描，多个package用逗号或者分号分隔
  typeAliasesPackage: com.xshl.bsp.**.domain
  global-config:
    dbConfig:
      # 主键类型
      # AUTO 自增 NONE 空 INPUT 用户输入 ASSIGN_ID 雪花 ASSIGN_UUID 唯一 UUID
      # 如需改为自增 需要将数据库表全部设置为自增
      idType: ASSIGN_ID

logging:
  level:
    io.swagger.models.parameters.AbstractSerializableParameter: info #忽略swagger中的错误信息
    com.xshl.bsp: info
#配置日志输出
logback:
  log:
    level: INFO
    path: /home/xshl/logs/user-center


#设置最大超时时间
ribbon:  
  ServerListRefreshInterval: 10  #刷新服务列表源的间隔时间
  OkToRetryOnAllOperations: true
  MaxAutoRetries: 1
  MaxAutoRetriesNextServer: 1
  ReadTimeout: 16000  
  ConnectTimeout: 16000 

gdzw:
  tokenUrl: a

environment: dev

sa-token:
  #忽略的路径
  pathIgnores: /user/**, dept/**
  # token 有效期（单位：秒） 默认30天，-1 代表永久有效
  #timeout: 2592000
  # token 最低活跃频率（单位：秒），如果 token 超过此时间没有访问系统就会被冻结，默认-1 代表不限制，永不冻结
  #active-timeout: -1
  # 是否允许同一账号多地同时登录 （为 true 时允许一起登录, 为 false 时新登录挤掉旧登录）
  #is-concurrent: true
  # 在多人登录同一账号时，是否共用一个 token （为 true 时所有登录共用一个 token, 为 false 时每次登录新建一个 token）
  #is-share: true
  # token 风格（默认可取值：uuid、simple-uuid、random-32、random-64、random-128、tik）
  #token-style: uuid
  # 是否输出操作日志
  #is-log: true

flow:
  companyId: b482a6393faefd53783f9d093cd4ddff
  sync: true
 ', 'fce5a3a89744755456fb079637a5d582', '2010-05-05 00:00:00', '2024-10-18 15:06:57.172', NULL, '192.168.10.2', 'I         ', '704f0050-72fe-4572-8e7d-40eb1e58aecd', '');
INSERT INTO "his_config_info" VALUES (0, 10, 'common.yaml', 'DEFAULT_GROUP', '', 'spring:
  cloud:
    nacos:
      discovery:
        server-addr: 192.168.20.48:8848
        namespace: 876aed9e-d385-4cb1-9b39-63a28eaf0737  #命名空间 代指某个环境
  sentinel:
    transport:
      # 指定sentinel 控制台的地址
      dashboard: 192.168.20.94:8080
    eager: true
  jackson:
    mapper:
      ALLOW_EXPLICIT_PROPERTY_RENAMING: true
    deserialization:
      READ_DATE_TIMESTAMPS_AS_NANOSECONDS: false
    serialization:
      WRITE_DATE_TIMESTAMPS_AS_NANOSECONDS: false
      WRITE_DATES_AS_TIMESTAMPS: true
# api接口加密
api-decrypt:
  # 是否开启全局接口加密
  enabled: false
  # AES 加密头标识
  headerFlag: encrypt-key
  # 响应加密公钥 非对称算法的公私钥 如：SM2，RSA 使用者请自行更换
  # 对应前端解密私钥 MIIBVAIBADANBgkqhkiG9w0BAQEFAASCAT4wggE6AgEAAkEAmc3CuPiGL/LcIIm7zryCEIbl1SPzBkr75E2VMtxegyZ1lYRD+7TZGAPkvIsBcaMs6Nsy0L78n2qh+lIZMpLH8wIDAQABAkEAk82Mhz0tlv6IVCyIcw/s3f0E+WLmtPFyR9/WtV3Y5aaejUkU60JpX4m5xNR2VaqOLTZAYjW8Wy0aXr3zYIhhQQIhAMfqR9oFdYw1J9SsNc+CrhugAvKTi0+BF6VoL6psWhvbAiEAxPPNTmrkmrXwdm/pQQu3UOQmc2vCZ5tiKpW10CgJi8kCIFGkL6utxw93Ncj4exE/gPLvKcT+1Emnoox+O9kRXss5AiAMtYLJDaLEzPrAWcZeeSgSIzbL+ecokmFKSDDcRske6QIgSMkHedwND1olF8vlKsJUGK3BcdtM8w4Xq7BpSBwsloE=
  publicKey: MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAJnNwrj4hi/y3CCJu868ghCG5dUj8wZK++RNlTLcXoMmdZWEQ/u02RgD5LyLAXGjLOjbMtC+/J9qofpSGTKSx/MCAwEAAQ==
  # 请求解密私钥 非对称算法的公私钥 如：SM2，RSA 使用者请自行更换
  # 对应前端加密公钥 MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAKoR8mX0rGKLqzcWmOzbfj64K8ZIgOdHnzkXSOVOZbFu/TJhZ7rFAN+eaGkl3C4buccQd/EjEsj9ir7ijT7h96MCAwEAAQ==
  privateKey: MIIBVAIBADANBgkqhkiG9w0BAQEFAASCAT4wggE6AgEAAkEAqhHyZfSsYourNxaY7Nt+PrgrxkiA50efORdI5U5lsW79MmFnusUA355oaSXcLhu5xxB38SMSyP2KvuKNPuH3owIDAQABAkAfoiLyL+Z4lf4Myxk6xUDgLaWGximj20CUf+5BKKnlrK+Ed8gAkM0HqoTt2UZwA5E2MzS4EI2gjfQhz5X28uqxAiEA3wNFxfrCZlSZHb0gn2zDpWowcSxQAgiCstxGUoOqlW8CIQDDOerGKH5OmCJ4Z21v+F25WaHYPxCFMvwxpcw99EcvDQIgIdhDTIqD2jfYjPTY8Jj3EDGPbH2HHuffvflECt3Ek60CIQCFRlCkHpi7hthhYhovyloRYsM+IS9h/0BzlEAuO0ktMQIgSPT3aFAgJYwKpqRYKlLDVcflZFCKY7u3UP8iWi1Qw0Y=

sa-token:
  #jwt秘钥
  jwt-secret-key: abcdefghijklmnopqrstuvwxyz
  # token 名称（同时也是 cookie 名称）
  token-name: Authorization
  #如果是单体服务，这里设置为false，这个是校验服务访问是否从网关进入
  check-same-token: true
  autoRenew: true
  timeout: 1800', '650afdb60258cebd5316c3cacc25c1e7', '2010-05-05 00:00:00', '2024-10-18 15:06:57.172', NULL, '192.168.10.2', 'I         ', '704f0050-72fe-4572-8e7d-40eb1e58aecd', '');
INSERT INTO "his_config_info" VALUES (0, 11, 'gateway.yaml', 'DEFAULT_GROUP', '', 'server:
  port: 9200 #端口
   
spring:
  cloud:
    gateway:
      requestLog: true
      discovery:
        locator:
          lowerCaseServiceId: true
          enabled: true
      routes:
       - id: api-user
         uri: lb://user-center
         order: 8001
         predicates:
         - Path=/api-user/**   
         filters:
         - StripPrefix=1 
       - id: api-auth
         uri: lb://auth
         order: 8002
         predicates:
         - Path=/api-auth/**
         filters:
         - PreserveHostHeader
         - StripPrefix=1  
       - id: api-file
         uri: lb://file
         order: 8003
         predicates:
         - Path=/api-file/**    
       - id: api-policy
         uri: lb://policy
         order: 8007
         predicates:
         - Path=/api-policy/**
         filters:
         - StripPrefix=1 
       - id: api-system
         uri: lb://system
         order: 8008
         predicates:
         - Path=/api-system/**
         filters:
         - StripPrefix=1 
       - id: api-mtc
         uri: lb://mtc
         order: 8009
         predicates:
         - Path=/api-mtc/**
         filters:
         - StripPrefix=1 
       - id: api-survey
         uri: lb://survey
         order: 8009
         predicates:
         - Path=/api-survey/**
         filters:
         - StripPrefix=1
       - id: api-flow
         uri: lb://flow
         order: 8009
         predicates:
         - Path=/api-flow/**
         filters:
         - StripPrefix=1 
       - id: api-apply
         uri: lb://apply
         order: 8009
         predicates:
         - Path=/api-apply/**
         filters:
         - StripPrefix=1
  datasource: 
    dynamic:
      # 设置默认的数据源或者数据源组,默认值即为 master
      primary: master
      datasource:
        # 主库数据源
        master:
          type: com.zaxxer.hikari.HikariDataSource
          driver-class-name: org.postgresql.Driver
          url: jdbc:postgresql://192.168.20.48:5432/bsp-user?useUnicode=true&characterEncoding=utf8&useSSL=true&autoReconnect=true&reWriteBatchedInserts=true
          username: root
          password: 123456              

################### mysq end ##########################
  redis:
################### redis 单机版 start ########################## 
    host: 192.168.20.48
    port: 6379
    password: xshl2023
    timeout: 6000
    database: 8
    lettuce:
      pool:
        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException  
        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
      shutdown-timeout: 100ms
################### redis 单机版 end ##########################   
#    cluster:
#      nodes: 130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #192.168.3.157:7000,192.168.3.158:7000,192.168.3.159:7000,192.168.3.157:7001,192.168.3.158:7001,192.168.3.159:7001
#    timeout: 1000 # 连接超时时间（毫秒）
#    lettuce:
#      pool:
#        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
#        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
#        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException  
#        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
#      shutdown-timeout: 100ms
  
mybatis-plus:
  # 不支持多包, 如有需要可在注解配置 或 提升扫包等级
  # 例如 com.**.**.mapper
  mapperPackage: com.xshl.bsp.**.mapper
  # 对应的 XML 文件位置
  mapperLocations: classpath*:mappers/**/*Mapper.xml
  # 实体扫描，多个package用逗号或者分号分隔
  typeAliasesPackage: com.xshl.bsp.**.domain
  global-config:
    dbConfig:
      # 主键类型
      # AUTO 自增 NONE 空 INPUT 用户输入 ASSIGN_ID 雪花 ASSIGN_UUID 唯一 UUID
      # 如需改为自增 需要将数据库表全部设置为自增
      idType: ASSIGN_ID


sa-token:
  #忽略的路径
  pathIgnores: /code/**, /auth/**, /test/**, /external/auth/getUserInfo, /external/embed/detail/**, /home/page/**, /matter/info/export, /sys/carousel/list, /entrepreneur/theory/list
  jwt-secret-key: abcdefghijklmnopqrstuvwxyz
  # 开启内网服务调用鉴权(不允许越过gateway访问内网服务 保障服务安全)
  #check-same-token: true
  # token 有效期（单位：秒） 默认30天，-1 代表永久有效
  timeout: 86400
  # token 最低活跃频率（单位：秒），如果 token 超过此时间没有访问系统就会被冻结，默认-1 代表不限制，永不冻结
  #active-timeout: -1
  # 是否允许同一账号多地同时登录 （为 true 时允许一起登录, 为 false 时新登录挤掉旧登录）
  #is-concurrent: true
  # 在多人登录同一账号时，是否共用一个 token （为 true 时所有登录共用一个 token, 为 false 时每次登录新建一个 token）
  #is-share: true
  # token 风格（默认可取值：uuid、simple-uuid、random-32、random-64、random-128、tik）
  #token-style: uuid
  # 是否输出操作日志
  #is-log: true

security:
  # 防止XSS攻击
  xss:
    enabled: true
    excludeUrls:
      - /api-user/notice
      - /flow/**
      - /tqt/api-flow/flow/**
      - /api-flow/flow/**
  # 不校验白名单
  ignore:
    whites: 
      - /api-auth/code
      - /api-auth/auth/**
      - /resource/sms/code
      - /*/v3/api-docs
      - /*/v2/api-docs
      - /*/error
      - /csrf
      - /doc.html
      - /webjars/**
      - /swagger-resources/**
      - /api-system/external/embed/detail/**
      - /api-auth/external/auth/**
      - /api-auth/sso/**
      - /api-system/home/page/**
      - /api-policy/home/page/**
      - /api-file/home/page/**
      - /api-policy/matter/info/export
      - /api-system/external/embed/detail/**
      - /api-quartz/test/**
      - /api-flow/login/**
      - /api-system/sys/carousel/list
      - /api-policy/entrepreneur/theory/list

swagger:
  enable: true
  butler:
    api-docs-path:  /v2/api-docs
    auto-generate-from-scg-routes: true
    ignore-routes:  api-eureka,api-generator,api-baidu

ribbon:
  ReadTimeout: 90000
  ConnectTimeout: 90000
  MaxAutoRetries: 0
  MaxAutoRetriesNextServer: 1
  OkToRetryOnAllOperations: false

feign:
  sentinel:
    enabled: true  #为feign整合sentinel

corsUrls: "*"', 'f3c22fd58eb7d1e153b3dacd33e97a5a', '2010-05-05 00:00:00', '2024-10-18 15:06:57.172', NULL, '192.168.10.2', 'I         ', '704f0050-72fe-4572-8e7d-40eb1e58aecd', '');
INSERT INTO "his_config_info" VALUES (2, 12, 'gateway.yaml', 'DEFAULT_GROUP', '', 'server:
  port: 9200 #端口
   
spring:
  cloud:
    gateway:
      requestLog: true
      discovery:
        locator:
          lowerCaseServiceId: true
          enabled: true
      routes:
       - id: api-user
         uri: lb://user-center
         order: 8001
         predicates:
         - Path=/api-user/**   
         filters:
         - StripPrefix=1 
       - id: api-auth
         uri: lb://auth
         order: 8002
         predicates:
         - Path=/api-auth/**
         filters:
         - PreserveHostHeader
         - StripPrefix=1  
       - id: api-file
         uri: lb://file
         order: 8003
         predicates:
         - Path=/api-file/**    
       - id: api-policy
         uri: lb://policy
         order: 8007
         predicates:
         - Path=/api-policy/**
         filters:
         - StripPrefix=1 
       - id: api-system
         uri: lb://system
         order: 8008
         predicates:
         - Path=/api-system/**
         filters:
         - StripPrefix=1 
       - id: api-mtc
         uri: lb://mtc
         order: 8009
         predicates:
         - Path=/api-mtc/**
         filters:
         - StripPrefix=1 
       - id: api-survey
         uri: lb://survey
         order: 8009
         predicates:
         - Path=/api-survey/**
         filters:
         - StripPrefix=1
       - id: api-flow
         uri: lb://flow
         order: 8009
         predicates:
         - Path=/api-flow/**
         filters:
         - StripPrefix=1 
       - id: api-apply
         uri: lb://apply
         order: 8009
         predicates:
         - Path=/api-apply/**
         filters:
         - StripPrefix=1
  datasource: 
    dynamic:
      # 设置默认的数据源或者数据源组,默认值即为 master
      primary: master
      datasource:
        # 主库数据源
        master:
          type: com.zaxxer.hikari.HikariDataSource
          driver-class-name: org.postgresql.Driver
          url: jdbc:postgresql://192.168.20.48:5432/bsp-user?useUnicode=true&characterEncoding=utf8&useSSL=true&autoReconnect=true&reWriteBatchedInserts=true
          username: root
          password: 123456              

################### mysq end ##########################
  redis:
################### redis 单机版 start ########################## 
    host: 192.168.20.48
    port: 6379
    password: xshl2023
    timeout: 6000
    database: 8
    lettuce:
      pool:
        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException  
        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
      shutdown-timeout: 100ms
################### redis 单机版 end ##########################   
#    cluster:
#      nodes: 130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #192.168.3.157:7000,192.168.3.158:7000,192.168.3.159:7000,192.168.3.157:7001,192.168.3.158:7001,192.168.3.159:7001
#    timeout: 1000 # 连接超时时间（毫秒）
#    lettuce:
#      pool:
#        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
#        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
#        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException  
#        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
#      shutdown-timeout: 100ms
  
mybatis-plus:
  # 不支持多包, 如有需要可在注解配置 或 提升扫包等级
  # 例如 com.**.**.mapper
  mapperPackage: com.xshl.bsp.**.mapper
  # 对应的 XML 文件位置
  mapperLocations: classpath*:mappers/**/*Mapper.xml
  # 实体扫描，多个package用逗号或者分号分隔
  typeAliasesPackage: com.xshl.bsp.**.domain
  global-config:
    dbConfig:
      # 主键类型
      # AUTO 自增 NONE 空 INPUT 用户输入 ASSIGN_ID 雪花 ASSIGN_UUID 唯一 UUID
      # 如需改为自增 需要将数据库表全部设置为自增
      idType: ASSIGN_ID


sa-token:
  #忽略的路径
  pathIgnores: /code/**, /auth/**, /test/**, /external/auth/getUserInfo, /external/embed/detail/**, /home/page/**, /matter/info/export, /sys/carousel/list, /entrepreneur/theory/list
  jwt-secret-key: abcdefghijklmnopqrstuvwxyz
  # 开启内网服务调用鉴权(不允许越过gateway访问内网服务 保障服务安全)
  #check-same-token: true
  # token 有效期（单位：秒） 默认30天，-1 代表永久有效
  timeout: 86400
  # token 最低活跃频率（单位：秒），如果 token 超过此时间没有访问系统就会被冻结，默认-1 代表不限制，永不冻结
  #active-timeout: -1
  # 是否允许同一账号多地同时登录 （为 true 时允许一起登录, 为 false 时新登录挤掉旧登录）
  #is-concurrent: true
  # 在多人登录同一账号时，是否共用一个 token （为 true 时所有登录共用一个 token, 为 false 时每次登录新建一个 token）
  #is-share: true
  # token 风格（默认可取值：uuid、simple-uuid、random-32、random-64、random-128、tik）
  #token-style: uuid
  # 是否输出操作日志
  #is-log: true

security:
  # 防止XSS攻击
  xss:
    enabled: true
    excludeUrls:
      - /api-user/notice
      - /flow/**
      - /tqt/api-flow/flow/**
      - /api-flow/flow/**
  # 不校验白名单
  ignore:
    whites: 
      - /api-auth/code
      - /api-auth/auth/**
      - /resource/sms/code
      - /*/v3/api-docs
      - /*/v2/api-docs
      - /*/error
      - /csrf
      - /doc.html
      - /webjars/**
      - /swagger-resources/**
      - /api-system/external/embed/detail/**
      - /api-auth/external/auth/**
      - /api-auth/sso/**
      - /api-system/home/page/**
      - /api-policy/home/page/**
      - /api-file/home/page/**
      - /api-policy/matter/info/export
      - /api-system/external/embed/detail/**
      - /api-quartz/test/**
      - /api-flow/login/**
      - /api-system/sys/carousel/list
      - /api-policy/entrepreneur/theory/list

swagger:
  enable: true
  butler:
    api-docs-path:  /v2/api-docs
    auto-generate-from-scg-routes: true
    ignore-routes:  api-eureka,api-generator,api-baidu

ribbon:
  ReadTimeout: 90000
  ConnectTimeout: 90000
  MaxAutoRetries: 0
  MaxAutoRetriesNextServer: 1
  OkToRetryOnAllOperations: false

feign:
  sentinel:
    enabled: true  #为feign整合sentinel

corsUrls: "*"', 'f3c22fd58eb7d1e153b3dacd33e97a5a', '2010-05-05 00:00:00', '2024-10-18 15:44:50.416', 'nacos', '192.168.10.2', 'U         ', '876aed9e-d385-4cb1-9b39-63a28eaf0737', '');
INSERT INTO "his_config_info" VALUES (3, 13, 'auth.yaml', 'DEFAULT_GROUP', '', '#端口配置
server:
  port: 8000   #固定端口
  forward-headers-strategy: none  #客户端请求头获取策略

spring:
  datasource: 
    dynamic:
      # 设置默认的数据源或者数据源组,默认值即为 master
      primary: master
      datasource:
        # 主库数据源
        master:
          type: com.zaxxer.hikari.HikariDataSource
          driver-class-name: org.postgresql.Driver
          url: jdbc:postgresql://192.168.20.30:5432/bsp-user?useUnicode=true&characterEncoding=utf8&useSSL=true&autoReconnect=true&reWriteBatchedInserts=true
          username: postgres
          password: ''!@#xshl2024''
#       oracle:
#          type: ${spring.datasource.type}
#          driverClassName: oracle.jdbc.OracleDriver
#          url: ${datasource.system-oracle.url}
#          username: ${datasource.system-oracle.username}
#          password: ${datasource.system-oracle.password}
#        postgres:
#          type: ${spring.datasource.type}
#          driverClassName: org.postgresql.Driver
#          url: ${datasource.system-postgres.url}
#          username: ${datasource.system-postgres.username}
#          password: ${datasource.system-postgres.password}

  ################### redis 单机版 start ##########################
  redis:
    host: 192.168.20.30
    port: 6379
    password: xshl2023
    timeout: 6000
    database: 8
    lettuce:
      pool:
        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException
        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
      shutdown-timeout: 100ms
################### redis 单机版 end ##########################
#    cluster:
#      nodes: 130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #192.168.3.157:7000,192.168.3.158:7000,192.168.3.159:7000,192.168.3.157:7001,192.168.3.158:7001,192.168.3.159:7001
#    timeout: 1000 # 连接超时时间（毫秒）
#    lettuce:
#      pool:
#        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
#        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
#        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException
#        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
#      shutdown-timeout: 100ms

mybatis-plus:
  # 不支持多包, 如有需要可在注解配置 或 提升扫包等级
  # 例如 com.**.**.mapper
  mapperPackage: com.xshl.bsp.**.mapper
  # 对应的 XML 文件位置
  mapperLocations: classpath*:mappers/**/*Mapper.xml
  # 实体扫描，多个package用逗号或者分号分隔
  typeAliasesPackage: com.xshl.bsp.**.domain
  global-config:
    dbConfig:
      # 主键类型
      # AUTO 自增 NONE 空 INPUT 用户输入 ASSIGN_ID 雪花 ASSIGN_UUID 唯一 UUID
      # 如需改为自增 需要将数据库表全部设置为自增
      idType: ASSIGN_ID

logging:
  level:
    io.swagger.models.parameters.AbstractSerializableParameter: info #忽略swagger中的错误信息
    com.xshl.bsp.user.dao: info

#spring-security配置
# security:
#   oauth2:
#     ignored: /users-anon/**, /doc.html, /document.html, /users/save
#     token:
#       store:
#         type: redis

#设置最大超时时间
ribbon:  
  ServerListRefreshInterval: 10  #刷新服务列表源的间隔时间
  OkToRetryOnAllOperations: true
  MaxAutoRetries: 1
  MaxAutoRetriesNextServer: 1
  ReadTimeout: 16000  
  ConnectTimeout: 16000 


gdzw:
  tokenUrl: a

environment: dev

sa-token:
  #忽略的路径
  pathIgnores: /code/**, /auth/**, /external/auth/**, /sso/*
  # 开启内网服务调用鉴权(不允许越过gateway访问内网服务 保障服务安全)
  #check-same-token: true
  # token 有效期（单位：秒） 默认30天，-1 代表永久有效
  timeout: 1800
  # token 最低活跃频率（单位：秒），如果 token 超过此时间没有访问系统就会被冻结，默认-1 代表不限制，永不冻结
  #active-timeout: -1
  # 是否允许同一账号多地同时登录 （为 true 时允许一起登录, 为 false 时新登录挤掉旧登录）
  #is-concurrent: true
  # 在多人登录同一账号时，是否共用一个 token （为 true 时所有登录共用一个 token, 为 false 时每次登录新建一个 token）
  #is-share: true
  # token 风格（默认可取值：uuid、simple-uuid、random-32、random-64、random-128、tik）
  #token-style: uuid
  # 是否输出操作日志
  #is-log: true
  check-same-token: true


  # 安全配置
security:
  # 验证码
  captcha:
    # 是否开启验证码
    enabled: true
    # 验证码类型 math 数组计算 char 字符验证
    type: MATH
    # line 线段干扰 circle 圆圈干扰 shear 扭曲干扰
    category: CIRCLE
    # 数字验证码位数
    numberLength: 1
    # 字符验证码长度
    charLength: 4

# 用户配置
user:
  password:
    # 密码最大错误次数
    maxRetryCount: 15
    # 密码锁定时间（默认10分钟）
    lockTime: 10

justauth:
  enabled: true
  # 前端外网访问地址
  address: http://localhost:80
  type:
    #pai平台对接
    pai:
      server-url: http://114.255.170.237:8086/pai
      client-id: policy_manage_test
      client-secret: fk9lr3710u7iklxzqy6bsakbyi7x36e6
      redirect-uri: http://localhost
      sso-context-path: /pai-sso
      api-context-path: /pai-api
      token-url: /login/token
      user-info: /v1/sdk/user
      user-info-list: /v1/sdk/user/list/all
      org-tree-url: /v1/sdk/org/tree
      log-out-url: /login/logout
    tz-province:
      server-url: https://tzsyslpt.zwfw.taizhou.gov.cn/tzs-tyrz
      client-id: tzsjj-yqlb
      client-secret: 4P7ByloTY474
      redirect-uri: http://localhost
      token-url: /ticket/token
      user-info: /token/user
      log-out-url: 

logback:
  log:
    level: info
    path: /home/xshl/logs/auth

license:
  subject: license
  publicAlias: publicCert
  storePass: public_Xshl2024
  licensePath: /home/license.lic
  publicKeysStorePath: /home/publicCerts.keystore ', '38e6d6173d863afe8bff6d222fff3485', '2010-05-05 00:00:00', '2024-10-18 15:50:24.93', 'nacos', '192.168.10.2', 'U         ', '876aed9e-d385-4cb1-9b39-63a28eaf0737', '');
INSERT INTO "his_config_info" VALUES (4, 14, 'user-center.yaml', 'DEFAULT_GROUP', '', '#端口配置
server:
  port: 8100   #固定端口
  forward-headers-strategy: none  #
  
spring:
  datasource: 
    dynamic:
      # 设置默认的数据源或者数据源组,默认值即为 master
      primary: master
      datasource:
        # 主库数据源
        master:
          type: com.zaxxer.hikari.HikariDataSource
          driver-class-name: org.postgresql.Driver
          url: jdbc:postgresql://192.168.20.30:5432/bsp-user?useUnicode=true&characterEncoding=utf8&useSSL=true&autoReconnect=true&reWriteBatchedInserts=true
          username: postgres
          password: ''!@#xshl2024''

  ################### redis 单机版 start ##########################
  redis:
    host: 192.168.20.30
    port: 6379
    password: xshl2023
    timeout: 6000
    database: 8
    lettuce:
      pool:
        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException
        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
      shutdown-timeout: 100ms
################### redis 单机版 end ##########################
#    cluster:
#      nodes: 130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #192.168.3.157:7000,192.168.3.158:7000,192.168.3.159:7000,192.168.3.157:7001,192.168.3.158:7001,192.168.3.159:7001
#    timeout: 1000 # 连接超时时间（毫秒）
#    lettuce:
#      pool:
#        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
#        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
#        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException
#        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
#      shutdown-timeout: 100ms

mybatis-plus:
  # 不支持多包, 如有需要可在注解配置 或 提升扫包等级
  # 例如 com.**.**.mapper
  mapperPackage: com.xshl.bsp.**.mapper
  # 对应的 XML 文件位置
  mapperLocations: classpath*:mappers/**/*Mapper.xml
  # 实体扫描，多个package用逗号或者分号分隔
  typeAliasesPackage: com.xshl.bsp.**.domain
  global-config:
    dbConfig:
      # 主键类型
      # AUTO 自增 NONE 空 INPUT 用户输入 ASSIGN_ID 雪花 ASSIGN_UUID 唯一 UUID
      # 如需改为自增 需要将数据库表全部设置为自增
      idType: ASSIGN_ID

logging:
  level:
    io.swagger.models.parameters.AbstractSerializableParameter: info #忽略swagger中的错误信息
    com.xshl.bsp: info
#配置日志输出
logback:
  log:
    level: INFO
    path: /home/xshl/logs/user-center


#设置最大超时时间
ribbon:  
  ServerListRefreshInterval: 10  #刷新服务列表源的间隔时间
  OkToRetryOnAllOperations: true
  MaxAutoRetries: 1
  MaxAutoRetriesNextServer: 1
  ReadTimeout: 16000  
  ConnectTimeout: 16000 

gdzw:
  tokenUrl: a

environment: dev

sa-token:
  #忽略的路径
  pathIgnores: /user/**, dept/**
  # token 有效期（单位：秒） 默认30天，-1 代表永久有效
  #timeout: 2592000
  # token 最低活跃频率（单位：秒），如果 token 超过此时间没有访问系统就会被冻结，默认-1 代表不限制，永不冻结
  #active-timeout: -1
  # 是否允许同一账号多地同时登录 （为 true 时允许一起登录, 为 false 时新登录挤掉旧登录）
  #is-concurrent: true
  # 在多人登录同一账号时，是否共用一个 token （为 true 时所有登录共用一个 token, 为 false 时每次登录新建一个 token）
  #is-share: true
  # token 风格（默认可取值：uuid、simple-uuid、random-32、random-64、random-128、tik）
  #token-style: uuid
  # 是否输出操作日志
  #is-log: true

flow:
  companyId: b482a6393faefd53783f9d093cd4ddff
  sync: true
 ', 'fce5a3a89744755456fb079637a5d582', '2010-05-05 00:00:00', '2024-10-18 15:50:51.292', 'nacos', '192.168.10.2', 'U         ', '876aed9e-d385-4cb1-9b39-63a28eaf0737', '');
INSERT INTO "his_config_info" VALUES (8, 15, 'auth.yaml', 'DEFAULT_GROUP', '', '#端口配置
server:
  port: 8000   #固定端口
  forward-headers-strategy: none  #客户端请求头获取策略

spring:
  datasource: 
    dynamic:
      # 设置默认的数据源或者数据源组,默认值即为 master
      primary: master
      datasource:
        # 主库数据源
        master:
          type: com.zaxxer.hikari.HikariDataSource
          driver-class-name: org.postgresql.Driver
          url: jdbc:postgresql://192.168.20.30:5432/bsp-user?useUnicode=true&characterEncoding=utf8&useSSL=true&autoReconnect=true&reWriteBatchedInserts=true
          username: postgres
          password: ''!@#xshl2024''
#       oracle:
#          type: ${spring.datasource.type}
#          driverClassName: oracle.jdbc.OracleDriver
#          url: ${datasource.system-oracle.url}
#          username: ${datasource.system-oracle.username}
#          password: ${datasource.system-oracle.password}
#        postgres:
#          type: ${spring.datasource.type}
#          driverClassName: org.postgresql.Driver
#          url: ${datasource.system-postgres.url}
#          username: ${datasource.system-postgres.username}
#          password: ${datasource.system-postgres.password}

  ################### redis 单机版 start ##########################
  redis:
    host: 192.168.20.30
    port: 6379
    password: xshl2023
    timeout: 6000
    database: 8
    lettuce:
      pool:
        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException
        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
      shutdown-timeout: 100ms
################### redis 单机版 end ##########################
#    cluster:
#      nodes: 130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #192.168.3.157:7000,192.168.3.158:7000,192.168.3.159:7000,192.168.3.157:7001,192.168.3.158:7001,192.168.3.159:7001
#    timeout: 1000 # 连接超时时间（毫秒）
#    lettuce:
#      pool:
#        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
#        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
#        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException
#        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
#      shutdown-timeout: 100ms

mybatis-plus:
  # 不支持多包, 如有需要可在注解配置 或 提升扫包等级
  # 例如 com.**.**.mapper
  mapperPackage: com.xshl.bsp.**.mapper
  # 对应的 XML 文件位置
  mapperLocations: classpath*:mappers/**/*Mapper.xml
  # 实体扫描，多个package用逗号或者分号分隔
  typeAliasesPackage: com.xshl.bsp.**.domain
  global-config:
    dbConfig:
      # 主键类型
      # AUTO 自增 NONE 空 INPUT 用户输入 ASSIGN_ID 雪花 ASSIGN_UUID 唯一 UUID
      # 如需改为自增 需要将数据库表全部设置为自增
      idType: ASSIGN_ID

logging:
  level:
    io.swagger.models.parameters.AbstractSerializableParameter: info #忽略swagger中的错误信息
    com.xshl.bsp.user.dao: info

#spring-security配置
# security:
#   oauth2:
#     ignored: /users-anon/**, /doc.html, /document.html, /users/save
#     token:
#       store:
#         type: redis

#设置最大超时时间
ribbon:  
  ServerListRefreshInterval: 10  #刷新服务列表源的间隔时间
  OkToRetryOnAllOperations: true
  MaxAutoRetries: 1
  MaxAutoRetriesNextServer: 1
  ReadTimeout: 16000  
  ConnectTimeout: 16000 


gdzw:
  tokenUrl: a

environment: dev

sa-token:
  #忽略的路径
  pathIgnores: /code/**, /auth/**, /external/auth/**, /sso/*
  # 开启内网服务调用鉴权(不允许越过gateway访问内网服务 保障服务安全)
  #check-same-token: true
  # token 有效期（单位：秒） 默认30天，-1 代表永久有效
  timeout: 1800
  # token 最低活跃频率（单位：秒），如果 token 超过此时间没有访问系统就会被冻结，默认-1 代表不限制，永不冻结
  #active-timeout: -1
  # 是否允许同一账号多地同时登录 （为 true 时允许一起登录, 为 false 时新登录挤掉旧登录）
  #is-concurrent: true
  # 在多人登录同一账号时，是否共用一个 token （为 true 时所有登录共用一个 token, 为 false 时每次登录新建一个 token）
  #is-share: true
  # token 风格（默认可取值：uuid、simple-uuid、random-32、random-64、random-128、tik）
  #token-style: uuid
  # 是否输出操作日志
  #is-log: true
  check-same-token: true


  # 安全配置
security:
  # 验证码
  captcha:
    # 是否开启验证码
    enabled: true
    # 验证码类型 math 数组计算 char 字符验证
    type: MATH
    # line 线段干扰 circle 圆圈干扰 shear 扭曲干扰
    category: CIRCLE
    # 数字验证码位数
    numberLength: 1
    # 字符验证码长度
    charLength: 4

# 用户配置
user:
  password:
    # 密码最大错误次数
    maxRetryCount: 15
    # 密码锁定时间（默认10分钟）
    lockTime: 10

justauth:
  enabled: true
  # 前端外网访问地址
  address: http://localhost:80
  type:
    #pai平台对接
    pai:
      server-url: http://114.255.170.237:8086/pai
      client-id: policy_manage_test
      client-secret: fk9lr3710u7iklxzqy6bsakbyi7x36e6
      redirect-uri: http://localhost
      sso-context-path: /pai-sso
      api-context-path: /pai-api
      token-url: /login/token
      user-info: /v1/sdk/user
      user-info-list: /v1/sdk/user/list/all
      org-tree-url: /v1/sdk/org/tree
      log-out-url: /login/logout
    tz-province:
      server-url: https://tzsyslpt.zwfw.taizhou.gov.cn/tzs-tyrz
      client-id: tzsjj-yqlb
      client-secret: 4P7ByloTY474
      redirect-uri: http://localhost
      token-url: /ticket/token
      user-info: /token/user
      log-out-url: 

logback:
  log:
    level: info
    path: /home/xshl/logs/auth

license:
  subject: license
  publicAlias: publicCert
  storePass: public_Xshl2024
  licensePath: /home/license.lic
  publicKeysStorePath: /home/publicCerts.keystore ', '38e6d6173d863afe8bff6d222fff3485', '2010-05-05 00:00:00', '2024-10-18 16:07:16.229', NULL, '192.168.10.2', 'D         ', '704f0050-72fe-4572-8e7d-40eb1e58aecd', '');
INSERT INTO "his_config_info" VALUES (9, 16, 'user-center.yaml', 'DEFAULT_GROUP', '', '#端口配置
server:
  port: 8100   #固定端口
  forward-headers-strategy: none  #
  
spring:
  datasource: 
    dynamic:
      # 设置默认的数据源或者数据源组,默认值即为 master
      primary: master
      datasource:
        # 主库数据源
        master:
          type: com.zaxxer.hikari.HikariDataSource
          driver-class-name: org.postgresql.Driver
          url: jdbc:postgresql://192.168.20.30:5432/bsp-user?useUnicode=true&characterEncoding=utf8&useSSL=true&autoReconnect=true&reWriteBatchedInserts=true
          username: postgres
          password: ''!@#xshl2024''

  ################### redis 单机版 start ##########################
  redis:
    host: 192.168.20.30
    port: 6379
    password: xshl2023
    timeout: 6000
    database: 8
    lettuce:
      pool:
        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException
        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
      shutdown-timeout: 100ms
################### redis 单机版 end ##########################
#    cluster:
#      nodes: 130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #192.168.3.157:7000,192.168.3.158:7000,192.168.3.159:7000,192.168.3.157:7001,192.168.3.158:7001,192.168.3.159:7001
#    timeout: 1000 # 连接超时时间（毫秒）
#    lettuce:
#      pool:
#        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
#        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
#        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException
#        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
#      shutdown-timeout: 100ms

mybatis-plus:
  # 不支持多包, 如有需要可在注解配置 或 提升扫包等级
  # 例如 com.**.**.mapper
  mapperPackage: com.xshl.bsp.**.mapper
  # 对应的 XML 文件位置
  mapperLocations: classpath*:mappers/**/*Mapper.xml
  # 实体扫描，多个package用逗号或者分号分隔
  typeAliasesPackage: com.xshl.bsp.**.domain
  global-config:
    dbConfig:
      # 主键类型
      # AUTO 自增 NONE 空 INPUT 用户输入 ASSIGN_ID 雪花 ASSIGN_UUID 唯一 UUID
      # 如需改为自增 需要将数据库表全部设置为自增
      idType: ASSIGN_ID

logging:
  level:
    io.swagger.models.parameters.AbstractSerializableParameter: info #忽略swagger中的错误信息
    com.xshl.bsp: info
#配置日志输出
logback:
  log:
    level: INFO
    path: /home/xshl/logs/user-center


#设置最大超时时间
ribbon:  
  ServerListRefreshInterval: 10  #刷新服务列表源的间隔时间
  OkToRetryOnAllOperations: true
  MaxAutoRetries: 1
  MaxAutoRetriesNextServer: 1
  ReadTimeout: 16000  
  ConnectTimeout: 16000 

gdzw:
  tokenUrl: a

environment: dev

sa-token:
  #忽略的路径
  pathIgnores: /user/**, dept/**
  # token 有效期（单位：秒） 默认30天，-1 代表永久有效
  #timeout: 2592000
  # token 最低活跃频率（单位：秒），如果 token 超过此时间没有访问系统就会被冻结，默认-1 代表不限制，永不冻结
  #active-timeout: -1
  # 是否允许同一账号多地同时登录 （为 true 时允许一起登录, 为 false 时新登录挤掉旧登录）
  #is-concurrent: true
  # 在多人登录同一账号时，是否共用一个 token （为 true 时所有登录共用一个 token, 为 false 时每次登录新建一个 token）
  #is-share: true
  # token 风格（默认可取值：uuid、simple-uuid、random-32、random-64、random-128、tik）
  #token-style: uuid
  # 是否输出操作日志
  #is-log: true

flow:
  companyId: b482a6393faefd53783f9d093cd4ddff
  sync: true
 ', 'fce5a3a89744755456fb079637a5d582', '2010-05-05 00:00:00', '2024-10-18 16:07:16.229', NULL, '192.168.10.2', 'D         ', '704f0050-72fe-4572-8e7d-40eb1e58aecd', '');
INSERT INTO "his_config_info" VALUES (10, 17, 'common.yaml', 'DEFAULT_GROUP', '', 'spring:
  cloud:
    nacos:
      discovery:
        server-addr: 192.168.20.48:8848
        namespace: 876aed9e-d385-4cb1-9b39-63a28eaf0737  #命名空间 代指某个环境
  sentinel:
    transport:
      # 指定sentinel 控制台的地址
      dashboard: 192.168.20.94:8080
    eager: true
  jackson:
    mapper:
      ALLOW_EXPLICIT_PROPERTY_RENAMING: true
    deserialization:
      READ_DATE_TIMESTAMPS_AS_NANOSECONDS: false
    serialization:
      WRITE_DATE_TIMESTAMPS_AS_NANOSECONDS: false
      WRITE_DATES_AS_TIMESTAMPS: true
# api接口加密
api-decrypt:
  # 是否开启全局接口加密
  enabled: false
  # AES 加密头标识
  headerFlag: encrypt-key
  # 响应加密公钥 非对称算法的公私钥 如：SM2，RSA 使用者请自行更换
  # 对应前端解密私钥 MIIBVAIBADANBgkqhkiG9w0BAQEFAASCAT4wggE6AgEAAkEAmc3CuPiGL/LcIIm7zryCEIbl1SPzBkr75E2VMtxegyZ1lYRD+7TZGAPkvIsBcaMs6Nsy0L78n2qh+lIZMpLH8wIDAQABAkEAk82Mhz0tlv6IVCyIcw/s3f0E+WLmtPFyR9/WtV3Y5aaejUkU60JpX4m5xNR2VaqOLTZAYjW8Wy0aXr3zYIhhQQIhAMfqR9oFdYw1J9SsNc+CrhugAvKTi0+BF6VoL6psWhvbAiEAxPPNTmrkmrXwdm/pQQu3UOQmc2vCZ5tiKpW10CgJi8kCIFGkL6utxw93Ncj4exE/gPLvKcT+1Emnoox+O9kRXss5AiAMtYLJDaLEzPrAWcZeeSgSIzbL+ecokmFKSDDcRske6QIgSMkHedwND1olF8vlKsJUGK3BcdtM8w4Xq7BpSBwsloE=
  publicKey: MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAJnNwrj4hi/y3CCJu868ghCG5dUj8wZK++RNlTLcXoMmdZWEQ/u02RgD5LyLAXGjLOjbMtC+/J9qofpSGTKSx/MCAwEAAQ==
  # 请求解密私钥 非对称算法的公私钥 如：SM2，RSA 使用者请自行更换
  # 对应前端加密公钥 MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAKoR8mX0rGKLqzcWmOzbfj64K8ZIgOdHnzkXSOVOZbFu/TJhZ7rFAN+eaGkl3C4buccQd/EjEsj9ir7ijT7h96MCAwEAAQ==
  privateKey: MIIBVAIBADANBgkqhkiG9w0BAQEFAASCAT4wggE6AgEAAkEAqhHyZfSsYourNxaY7Nt+PrgrxkiA50efORdI5U5lsW79MmFnusUA355oaSXcLhu5xxB38SMSyP2KvuKNPuH3owIDAQABAkAfoiLyL+Z4lf4Myxk6xUDgLaWGximj20CUf+5BKKnlrK+Ed8gAkM0HqoTt2UZwA5E2MzS4EI2gjfQhz5X28uqxAiEA3wNFxfrCZlSZHb0gn2zDpWowcSxQAgiCstxGUoOqlW8CIQDDOerGKH5OmCJ4Z21v+F25WaHYPxCFMvwxpcw99EcvDQIgIdhDTIqD2jfYjPTY8Jj3EDGPbH2HHuffvflECt3Ek60CIQCFRlCkHpi7hthhYhovyloRYsM+IS9h/0BzlEAuO0ktMQIgSPT3aFAgJYwKpqRYKlLDVcflZFCKY7u3UP8iWi1Qw0Y=

sa-token:
  #jwt秘钥
  jwt-secret-key: abcdefghijklmnopqrstuvwxyz
  # token 名称（同时也是 cookie 名称）
  token-name: Authorization
  #如果是单体服务，这里设置为false，这个是校验服务访问是否从网关进入
  check-same-token: true
  autoRenew: true
  timeout: 1800', '650afdb60258cebd5316c3cacc25c1e7', '2010-05-05 00:00:00', '2024-10-18 16:07:16.229', NULL, '192.168.10.2', 'D         ', '704f0050-72fe-4572-8e7d-40eb1e58aecd', '');
INSERT INTO "his_config_info" VALUES (11, 18, 'gateway.yaml', 'DEFAULT_GROUP', '', 'server:
  port: 9200 #端口
   
spring:
  cloud:
    gateway:
      requestLog: true
      discovery:
        locator:
          lowerCaseServiceId: true
          enabled: true
      routes:
       - id: api-user
         uri: lb://user-center
         order: 8001
         predicates:
         - Path=/api-user/**   
         filters:
         - StripPrefix=1 
       - id: api-auth
         uri: lb://auth
         order: 8002
         predicates:
         - Path=/api-auth/**
         filters:
         - PreserveHostHeader
         - StripPrefix=1  
       - id: api-file
         uri: lb://file
         order: 8003
         predicates:
         - Path=/api-file/**    
       - id: api-policy
         uri: lb://policy
         order: 8007
         predicates:
         - Path=/api-policy/**
         filters:
         - StripPrefix=1 
       - id: api-system
         uri: lb://system
         order: 8008
         predicates:
         - Path=/api-system/**
         filters:
         - StripPrefix=1 
       - id: api-mtc
         uri: lb://mtc
         order: 8009
         predicates:
         - Path=/api-mtc/**
         filters:
         - StripPrefix=1 
       - id: api-survey
         uri: lb://survey
         order: 8009
         predicates:
         - Path=/api-survey/**
         filters:
         - StripPrefix=1
       - id: api-flow
         uri: lb://flow
         order: 8009
         predicates:
         - Path=/api-flow/**
         filters:
         - StripPrefix=1 
       - id: api-apply
         uri: lb://apply
         order: 8009
         predicates:
         - Path=/api-apply/**
         filters:
         - StripPrefix=1
  datasource: 
    dynamic:
      # 设置默认的数据源或者数据源组,默认值即为 master
      primary: master
      datasource:
        # 主库数据源
        master:
          type: com.zaxxer.hikari.HikariDataSource
          driver-class-name: org.postgresql.Driver
          url: jdbc:postgresql://192.168.20.48:5432/bsp-user?useUnicode=true&characterEncoding=utf8&useSSL=true&autoReconnect=true&reWriteBatchedInserts=true
          username: root
          password: 123456              

################### mysq end ##########################
  redis:
################### redis 单机版 start ########################## 
    host: 192.168.20.48
    port: 6379
    password: xshl2023
    timeout: 6000
    database: 8
    lettuce:
      pool:
        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException  
        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
      shutdown-timeout: 100ms
################### redis 单机版 end ##########################   
#    cluster:
#      nodes: 130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #192.168.3.157:7000,192.168.3.158:7000,192.168.3.159:7000,192.168.3.157:7001,192.168.3.158:7001,192.168.3.159:7001
#    timeout: 1000 # 连接超时时间（毫秒）
#    lettuce:
#      pool:
#        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
#        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
#        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException  
#        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
#      shutdown-timeout: 100ms
  
mybatis-plus:
  # 不支持多包, 如有需要可在注解配置 或 提升扫包等级
  # 例如 com.**.**.mapper
  mapperPackage: com.xshl.bsp.**.mapper
  # 对应的 XML 文件位置
  mapperLocations: classpath*:mappers/**/*Mapper.xml
  # 实体扫描，多个package用逗号或者分号分隔
  typeAliasesPackage: com.xshl.bsp.**.domain
  global-config:
    dbConfig:
      # 主键类型
      # AUTO 自增 NONE 空 INPUT 用户输入 ASSIGN_ID 雪花 ASSIGN_UUID 唯一 UUID
      # 如需改为自增 需要将数据库表全部设置为自增
      idType: ASSIGN_ID


sa-token:
  #忽略的路径
  pathIgnores: /code/**, /auth/**, /test/**, /external/auth/getUserInfo, /external/embed/detail/**, /home/page/**, /matter/info/export, /sys/carousel/list, /entrepreneur/theory/list
  jwt-secret-key: abcdefghijklmnopqrstuvwxyz
  # 开启内网服务调用鉴权(不允许越过gateway访问内网服务 保障服务安全)
  #check-same-token: true
  # token 有效期（单位：秒） 默认30天，-1 代表永久有效
  timeout: 86400
  # token 最低活跃频率（单位：秒），如果 token 超过此时间没有访问系统就会被冻结，默认-1 代表不限制，永不冻结
  #active-timeout: -1
  # 是否允许同一账号多地同时登录 （为 true 时允许一起登录, 为 false 时新登录挤掉旧登录）
  #is-concurrent: true
  # 在多人登录同一账号时，是否共用一个 token （为 true 时所有登录共用一个 token, 为 false 时每次登录新建一个 token）
  #is-share: true
  # token 风格（默认可取值：uuid、simple-uuid、random-32、random-64、random-128、tik）
  #token-style: uuid
  # 是否输出操作日志
  #is-log: true

security:
  # 防止XSS攻击
  xss:
    enabled: true
    excludeUrls:
      - /api-user/notice
      - /flow/**
      - /tqt/api-flow/flow/**
      - /api-flow/flow/**
  # 不校验白名单
  ignore:
    whites: 
      - /api-auth/code
      - /api-auth/auth/**
      - /resource/sms/code
      - /*/v3/api-docs
      - /*/v2/api-docs
      - /*/error
      - /csrf
      - /doc.html
      - /webjars/**
      - /swagger-resources/**
      - /api-system/external/embed/detail/**
      - /api-auth/external/auth/**
      - /api-auth/sso/**
      - /api-system/home/page/**
      - /api-policy/home/page/**
      - /api-file/home/page/**
      - /api-policy/matter/info/export
      - /api-system/external/embed/detail/**
      - /api-quartz/test/**
      - /api-flow/login/**
      - /api-system/sys/carousel/list
      - /api-policy/entrepreneur/theory/list

swagger:
  enable: true
  butler:
    api-docs-path:  /v2/api-docs
    auto-generate-from-scg-routes: true
    ignore-routes:  api-eureka,api-generator,api-baidu

ribbon:
  ReadTimeout: 90000
  ConnectTimeout: 90000
  MaxAutoRetries: 0
  MaxAutoRetriesNextServer: 1
  OkToRetryOnAllOperations: false

feign:
  sentinel:
    enabled: true  #为feign整合sentinel

corsUrls: "*"', 'f3c22fd58eb7d1e153b3dacd33e97a5a', '2010-05-05 00:00:00', '2024-10-18 16:07:16.229', NULL, '192.168.10.2', 'D         ', '704f0050-72fe-4572-8e7d-40eb1e58aecd', '');
INSERT INTO "his_config_info" VALUES (0, 19, 'common.yaml', 'DEFAULT_GROUP', '', 'spring:
  cloud:
    nacos:
      discovery:
        server-addr: 192.168.20.48:8848
        namespace: 876aed9e-d385-4cb1-9b39-63a28eaf0737  #命名空间 代指某个环境
  sentinel:
    transport:
      # 指定sentinel 控制台的地址
      dashboard: 192.168.20.94:8080
    eager: true
  jackson:
    mapper:
      ALLOW_EXPLICIT_PROPERTY_RENAMING: true
    deserialization:
      READ_DATE_TIMESTAMPS_AS_NANOSECONDS: false
    serialization:
      WRITE_DATE_TIMESTAMPS_AS_NANOSECONDS: false
      WRITE_DATES_AS_TIMESTAMPS: true
# api接口加密
api-decrypt:
  # 是否开启全局接口加密
  enabled: false
  # AES 加密头标识
  headerFlag: encrypt-key
  # 响应加密公钥 非对称算法的公私钥 如：SM2，RSA 使用者请自行更换
  # 对应前端解密私钥 MIIBVAIBADANBgkqhkiG9w0BAQEFAASCAT4wggE6AgEAAkEAmc3CuPiGL/LcIIm7zryCEIbl1SPzBkr75E2VMtxegyZ1lYRD+7TZGAPkvIsBcaMs6Nsy0L78n2qh+lIZMpLH8wIDAQABAkEAk82Mhz0tlv6IVCyIcw/s3f0E+WLmtPFyR9/WtV3Y5aaejUkU60JpX4m5xNR2VaqOLTZAYjW8Wy0aXr3zYIhhQQIhAMfqR9oFdYw1J9SsNc+CrhugAvKTi0+BF6VoL6psWhvbAiEAxPPNTmrkmrXwdm/pQQu3UOQmc2vCZ5tiKpW10CgJi8kCIFGkL6utxw93Ncj4exE/gPLvKcT+1Emnoox+O9kRXss5AiAMtYLJDaLEzPrAWcZeeSgSIzbL+ecokmFKSDDcRske6QIgSMkHedwND1olF8vlKsJUGK3BcdtM8w4Xq7BpSBwsloE=
  publicKey: MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAJnNwrj4hi/y3CCJu868ghCG5dUj8wZK++RNlTLcXoMmdZWEQ/u02RgD5LyLAXGjLOjbMtC+/J9qofpSGTKSx/MCAwEAAQ==
  # 请求解密私钥 非对称算法的公私钥 如：SM2，RSA 使用者请自行更换
  # 对应前端加密公钥 MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAKoR8mX0rGKLqzcWmOzbfj64K8ZIgOdHnzkXSOVOZbFu/TJhZ7rFAN+eaGkl3C4buccQd/EjEsj9ir7ijT7h96MCAwEAAQ==
  privateKey: MIIBVAIBADANBgkqhkiG9w0BAQEFAASCAT4wggE6AgEAAkEAqhHyZfSsYourNxaY7Nt+PrgrxkiA50efORdI5U5lsW79MmFnusUA355oaSXcLhu5xxB38SMSyP2KvuKNPuH3owIDAQABAkAfoiLyL+Z4lf4Myxk6xUDgLaWGximj20CUf+5BKKnlrK+Ed8gAkM0HqoTt2UZwA5E2MzS4EI2gjfQhz5X28uqxAiEA3wNFxfrCZlSZHb0gn2zDpWowcSxQAgiCstxGUoOqlW8CIQDDOerGKH5OmCJ4Z21v+F25WaHYPxCFMvwxpcw99EcvDQIgIdhDTIqD2jfYjPTY8Jj3EDGPbH2HHuffvflECt3Ek60CIQCFRlCkHpi7hthhYhovyloRYsM+IS9h/0BzlEAuO0ktMQIgSPT3aFAgJYwKpqRYKlLDVcflZFCKY7u3UP8iWi1Qw0Y=

sa-token:
  #jwt秘钥
  jwt-secret-key: abcdefghijklmnopqrstuvwxyz
  # token 名称（同时也是 cookie 名称）
  token-name: Authorization
  #如果是单体服务，这里设置为false，这个是校验服务访问是否从网关进入
  check-same-token: true
  autoRenew: true
  timeout: 1800', '650afdb60258cebd5316c3cacc25c1e7', '2010-05-05 00:00:00', '2024-10-18 16:07:22.231', NULL, '192.168.10.2', 'I         ', '704f0050-72fe-4572-8e7d-40eb1e58aecd', '');
INSERT INTO "his_config_info" VALUES (0, 20, 'gateway.yaml', 'DEFAULT_GROUP', '', 'server:
  port: 9200 #端口
   
spring:
  cloud:
    gateway:
      requestLog: true
      discovery:
        locator:
          lowerCaseServiceId: true
          enabled: true
      routes:
       - id: api-user
         uri: lb://user-center
         order: 8001
         predicates:
         - Path=/api-user/**   
         filters:
         - StripPrefix=1 
       - id: api-auth
         uri: lb://auth
         order: 8002
         predicates:
         - Path=/api-auth/**
         filters:
         - PreserveHostHeader
         - StripPrefix=1  
       - id: api-file
         uri: lb://file
         order: 8003
         predicates:
         - Path=/api-file/**    
       - id: api-system
         uri: lb://system
         order: 8008
         predicates:
         - Path=/api-system/**
         filters:
         - StripPrefix=1 
  datasource: 
    dynamic:
      # 设置默认的数据源或者数据源组,默认值即为 master
      primary: master
      datasource:
        # 主库数据源
        master:
          type: com.zaxxer.hikari.HikariDataSource
          driver-class-name: org.postgresql.Driver
          url: jdbc:postgresql://192.168.20.48:5432/bsp-user?useUnicode=true&characterEncoding=utf8&useSSL=true&autoReconnect=true&reWriteBatchedInserts=true
          username: root
          password: 123456              

################### mysq end ##########################
  redis:
################### redis 单机版 start ########################## 
    host: 192.168.20.48
    port: 6379
    password: xshl2023
    timeout: 6000
    database: 8
    lettuce:
      pool:
        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException  
        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
      shutdown-timeout: 100ms
################### redis 单机版 end ##########################   
#    cluster:
#      nodes: 130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #192.168.3.157:7000,192.168.3.158:7000,192.168.3.159:7000,192.168.3.157:7001,192.168.3.158:7001,192.168.3.159:7001
#    timeout: 1000 # 连接超时时间（毫秒）
#    lettuce:
#      pool:
#        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
#        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
#        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException  
#        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
#      shutdown-timeout: 100ms
  
mybatis-plus:
  # 不支持多包, 如有需要可在注解配置 或 提升扫包等级
  # 例如 com.**.**.mapper
  mapperPackage: com.xshl.bsp.**.mapper
  # 对应的 XML 文件位置
  mapperLocations: classpath*:mappers/**/*Mapper.xml
  # 实体扫描，多个package用逗号或者分号分隔
  typeAliasesPackage: com.xshl.bsp.**.domain
  global-config:
    dbConfig:
      # 主键类型
      # AUTO 自增 NONE 空 INPUT 用户输入 ASSIGN_ID 雪花 ASSIGN_UUID 唯一 UUID
      # 如需改为自增 需要将数据库表全部设置为自增
      idType: ASSIGN_ID


sa-token:
  #忽略的路径
  pathIgnores: /code/**, /auth/**, /test/**, /external/auth/getUserInfo, /external/embed/detail/**, /home/page/**, /matter/info/export, /sys/carousel/list, /entrepreneur/theory/list
  jwt-secret-key: abcdefghijklmnopqrstuvwxyz
  # 开启内网服务调用鉴权(不允许越过gateway访问内网服务 保障服务安全)
  #check-same-token: true
  # token 有效期（单位：秒） 默认30天，-1 代表永久有效
  timeout: 86400
  # token 最低活跃频率（单位：秒），如果 token 超过此时间没有访问系统就会被冻结，默认-1 代表不限制，永不冻结
  #active-timeout: -1
  # 是否允许同一账号多地同时登录 （为 true 时允许一起登录, 为 false 时新登录挤掉旧登录）
  #is-concurrent: true
  # 在多人登录同一账号时，是否共用一个 token （为 true 时所有登录共用一个 token, 为 false 时每次登录新建一个 token）
  #is-share: true
  # token 风格（默认可取值：uuid、simple-uuid、random-32、random-64、random-128、tik）
  #token-style: uuid
  # 是否输出操作日志
  #is-log: true

security:
  # 防止XSS攻击
  xss:
    enabled: true
    excludeUrls:
      - /api-user/notice
      - /flow/**
      - /tqt/api-flow/flow/**
      - /api-flow/flow/**
  # 不校验白名单
  ignore:
    whites: 
      - /api-auth/code
      - /api-auth/auth/**
      - /resource/sms/code
      - /*/v3/api-docs
      - /*/v2/api-docs
      - /*/error
      - /csrf
      - /doc.html
      - /webjars/**
      - /swagger-resources/**
      - /api-system/external/embed/detail/**
      - /api-auth/external/auth/**
      - /api-auth/sso/**
      - /api-system/home/page/**
      - /api-policy/home/page/**
      - /api-file/home/page/**
      - /api-policy/matter/info/export
      - /api-system/external/embed/detail/**
      - /api-quartz/test/**
      - /api-flow/login/**
      - /api-system/sys/carousel/list
      - /api-policy/entrepreneur/theory/list

swagger:
  enable: true
  butler:
    api-docs-path:  /v2/api-docs
    auto-generate-from-scg-routes: true
    ignore-routes:  api-eureka,api-generator,api-baidu

ribbon:
  ReadTimeout: 90000
  ConnectTimeout: 90000
  MaxAutoRetries: 0
  MaxAutoRetriesNextServer: 1
  OkToRetryOnAllOperations: false

feign:
  sentinel:
    enabled: true  #为feign整合sentinel

corsUrls: "*"', '548b501948c3a5a27412b85995157790', '2010-05-05 00:00:00', '2024-10-18 16:07:22.231', NULL, '192.168.10.2', 'I         ', '704f0050-72fe-4572-8e7d-40eb1e58aecd', '');
INSERT INTO "his_config_info" VALUES (0, 21, 'auth.yaml', 'DEFAULT_GROUP', '', '#端口配置
server:
  port: 8000   #固定端口
  forward-headers-strategy: none  #客户端请求头获取策略

spring:
  datasource: 
    dynamic:
      # 设置默认的数据源或者数据源组,默认值即为 master
      primary: master
      datasource:
        # 主库数据源
        master:
          type: com.zaxxer.hikari.HikariDataSource
          driver-class-name: org.postgresql.Driver
          url: jdbc:postgresql://192.168.20.48:5432/bsp-user?useUnicode=true&characterEncoding=utf8&useSSL=true&autoReconnect=true&reWriteBatchedInserts=true
          username: root
          password: 123456
#       oracle:
#          type: ${spring.datasource.type}
#          driverClassName: oracle.jdbc.OracleDriver
#          url: ${datasource.system-oracle.url}
#          username: ${datasource.system-oracle.username}
#          password: ${datasource.system-oracle.password}
#        postgres:
#          type: ${spring.datasource.type}
#          driverClassName: org.postgresql.Driver
#          url: ${datasource.system-postgres.url}
#          username: ${datasource.system-postgres.username}
#          password: ${datasource.system-postgres.password}

  ################### redis 单机版 start ##########################
  redis:
    host: 192.168.20.48
    port: 6379
    password: xshl2023
    timeout: 6000
    database: 8
    lettuce:
      pool:
        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException
        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
      shutdown-timeout: 100ms
################### redis 单机版 end ##########################
#    cluster:
#      nodes: 130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #192.168.3.157:7000,192.168.3.158:7000,192.168.3.159:7000,192.168.3.157:7001,192.168.3.158:7001,192.168.3.159:7001
#    timeout: 1000 # 连接超时时间（毫秒）
#    lettuce:
#      pool:
#        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
#        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
#        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException
#        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
#      shutdown-timeout: 100ms

mybatis-plus:
  # 不支持多包, 如有需要可在注解配置 或 提升扫包等级
  # 例如 com.**.**.mapper
  mapperPackage: com.xshl.bsp.**.mapper
  # 对应的 XML 文件位置
  mapperLocations: classpath*:mappers/**/*Mapper.xml
  # 实体扫描，多个package用逗号或者分号分隔
  typeAliasesPackage: com.xshl.bsp.**.domain
  global-config:
    dbConfig:
      # 主键类型
      # AUTO 自增 NONE 空 INPUT 用户输入 ASSIGN_ID 雪花 ASSIGN_UUID 唯一 UUID
      # 如需改为自增 需要将数据库表全部设置为自增
      idType: ASSIGN_ID

logging:
  level:
    io.swagger.models.parameters.AbstractSerializableParameter: info #忽略swagger中的错误信息
    com.xshl.bsp.user.dao: info

#spring-security配置
# security:
#   oauth2:
#     ignored: /users-anon/**, /doc.html, /document.html, /users/save
#     token:
#       store:
#         type: redis

#设置最大超时时间
ribbon:  
  ServerListRefreshInterval: 10  #刷新服务列表源的间隔时间
  OkToRetryOnAllOperations: true
  MaxAutoRetries: 1
  MaxAutoRetriesNextServer: 1
  ReadTimeout: 16000  
  ConnectTimeout: 16000 


gdzw:
  tokenUrl: a

environment: dev

sa-token:
  #忽略的路径
  pathIgnores: /code/**, /auth/**, /external/auth/**, /sso/*
  # 开启内网服务调用鉴权(不允许越过gateway访问内网服务 保障服务安全)
  #check-same-token: true
  # token 有效期（单位：秒） 默认30天，-1 代表永久有效
  timeout: 1800
  # token 最低活跃频率（单位：秒），如果 token 超过此时间没有访问系统就会被冻结，默认-1 代表不限制，永不冻结
  #active-timeout: -1
  # 是否允许同一账号多地同时登录 （为 true 时允许一起登录, 为 false 时新登录挤掉旧登录）
  #is-concurrent: true
  # 在多人登录同一账号时，是否共用一个 token （为 true 时所有登录共用一个 token, 为 false 时每次登录新建一个 token）
  #is-share: true
  # token 风格（默认可取值：uuid、simple-uuid、random-32、random-64、random-128、tik）
  #token-style: uuid
  # 是否输出操作日志
  #is-log: true
  check-same-token: true


  # 安全配置
security:
  # 验证码
  captcha:
    # 是否开启验证码
    enabled: true
    # 验证码类型 math 数组计算 char 字符验证
    type: MATH
    # line 线段干扰 circle 圆圈干扰 shear 扭曲干扰
    category: CIRCLE
    # 数字验证码位数
    numberLength: 1
    # 字符验证码长度
    charLength: 4

# 用户配置
user:
  password:
    # 密码最大错误次数
    maxRetryCount: 15
    # 密码锁定时间（默认10分钟）
    lockTime: 10

justauth:
  enabled: true
  # 前端外网访问地址
  address: http://localhost:80
  type:
    #pai平台对接
    pai:
      server-url: http://114.255.170.237:8086/pai
      client-id: policy_manage_test
      client-secret: fk9lr3710u7iklxzqy6bsakbyi7x36e6
      redirect-uri: http://localhost
      sso-context-path: /pai-sso
      api-context-path: /pai-api
      token-url: /login/token
      user-info: /v1/sdk/user
      user-info-list: /v1/sdk/user/list/all
      org-tree-url: /v1/sdk/org/tree
      log-out-url: /login/logout
    tz-province:
      server-url: https://tzsyslpt.zwfw.taizhou.gov.cn/tzs-tyrz
      client-id: tzsjj-yqlb
      client-secret: 4P7ByloTY474
      redirect-uri: http://localhost
      token-url: /ticket/token
      user-info: /token/user
      log-out-url: 

logback:
  log:
    level: info
    path: /home/xshl/logs/auth

license:
  subject: license
  publicAlias: publicCert
  storePass: public_Xshl2024
  licensePath: /home/license.lic
  publicKeysStorePath: /home/publicCerts.keystore ', '6e3de8ad739a0a7825ef2ac20596f470', '2010-05-05 00:00:00', '2024-10-18 16:07:22.231', NULL, '192.168.10.2', 'I         ', '704f0050-72fe-4572-8e7d-40eb1e58aecd', '');
INSERT INTO "his_config_info" VALUES (0, 22, 'user-center.yaml', 'DEFAULT_GROUP', '', '#端口配置
server:
  port: 8100   #固定端口
  forward-headers-strategy: none  #
  
spring:
  datasource: 
    dynamic:
      # 设置默认的数据源或者数据源组,默认值即为 master
      primary: master
      datasource:
        # 主库数据源
        master:
          type: com.zaxxer.hikari.HikariDataSource
          driver-class-name: org.postgresql.Driver
          url: jdbc:postgresql://192.168.20.48:5432/bsp-user?useUnicode=true&characterEncoding=utf8&useSSL=true&autoReconnect=true&reWriteBatchedInserts=true
          username: root
          password: 123456

  ################### redis 单机版 start ##########################
  redis:
    host: 192.168.20.48
    port: 6379
    password: xshl2023
    timeout: 6000
    database: 8
    lettuce:
      pool:
        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException
        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
      shutdown-timeout: 100ms
################### redis 单机版 end ##########################
#    cluster:
#      nodes: 130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #192.168.3.157:7000,192.168.3.158:7000,192.168.3.159:7000,192.168.3.157:7001,192.168.3.158:7001,192.168.3.159:7001
#    timeout: 1000 # 连接超时时间（毫秒）
#    lettuce:
#      pool:
#        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
#        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
#        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException
#        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
#      shutdown-timeout: 100ms

mybatis-plus:
  # 不支持多包, 如有需要可在注解配置 或 提升扫包等级
  # 例如 com.**.**.mapper
  mapperPackage: com.xshl.bsp.**.mapper
  # 对应的 XML 文件位置
  mapperLocations: classpath*:mappers/**/*Mapper.xml
  # 实体扫描，多个package用逗号或者分号分隔
  typeAliasesPackage: com.xshl.bsp.**.domain
  global-config:
    dbConfig:
      # 主键类型
      # AUTO 自增 NONE 空 INPUT 用户输入 ASSIGN_ID 雪花 ASSIGN_UUID 唯一 UUID
      # 如需改为自增 需要将数据库表全部设置为自增
      idType: ASSIGN_ID

logging:
  level:
    io.swagger.models.parameters.AbstractSerializableParameter: info #忽略swagger中的错误信息
    com.xshl.bsp: info
#配置日志输出
logback:
  log:
    level: INFO
    path: /home/xshl/logs/user-center


#设置最大超时时间
ribbon:  
  ServerListRefreshInterval: 10  #刷新服务列表源的间隔时间
  OkToRetryOnAllOperations: true
  MaxAutoRetries: 1
  MaxAutoRetriesNextServer: 1
  ReadTimeout: 16000  
  ConnectTimeout: 16000 

gdzw:
  tokenUrl: a

environment: dev

sa-token:
  #忽略的路径
  pathIgnores: /user/**, dept/**
  # token 有效期（单位：秒） 默认30天，-1 代表永久有效
  #timeout: 2592000
  # token 最低活跃频率（单位：秒），如果 token 超过此时间没有访问系统就会被冻结，默认-1 代表不限制，永不冻结
  #active-timeout: -1
  # 是否允许同一账号多地同时登录 （为 true 时允许一起登录, 为 false 时新登录挤掉旧登录）
  #is-concurrent: true
  # 在多人登录同一账号时，是否共用一个 token （为 true 时所有登录共用一个 token, 为 false 时每次登录新建一个 token）
  #is-share: true
  # token 风格（默认可取值：uuid、simple-uuid、random-32、random-64、random-128、tik）
  #token-style: uuid
  # 是否输出操作日志
  #is-log: true

flow:
  companyId: b482a6393faefd53783f9d093cd4ddff
  sync: true
 ', '2726e107b651bcbd6a90cc406f976178', '2010-05-05 00:00:00', '2024-10-18 16:07:22.231', NULL, '192.168.10.2', 'I         ', '704f0050-72fe-4572-8e7d-40eb1e58aecd', '');
INSERT INTO "his_config_info" VALUES (3, 23, 'auth.yaml', 'DEFAULT_GROUP', '', '#端口配置
server:
  port: 8000   #固定端口
  forward-headers-strategy: none  #客户端请求头获取策略

spring:
  datasource: 
    dynamic:
      # 设置默认的数据源或者数据源组,默认值即为 master
      primary: master
      datasource:
        # 主库数据源
        master:
          type: com.zaxxer.hikari.HikariDataSource
          driver-class-name: org.postgresql.Driver
          url: jdbc:postgresql://192.168.20.48:5432/bsp-user?useUnicode=true&characterEncoding=utf8&useSSL=true&autoReconnect=true&reWriteBatchedInserts=true
          username: root
          password: 123456
#       oracle:
#          type: ${spring.datasource.type}
#          driverClassName: oracle.jdbc.OracleDriver
#          url: ${datasource.system-oracle.url}
#          username: ${datasource.system-oracle.username}
#          password: ${datasource.system-oracle.password}
#        postgres:
#          type: ${spring.datasource.type}
#          driverClassName: org.postgresql.Driver
#          url: ${datasource.system-postgres.url}
#          username: ${datasource.system-postgres.username}
#          password: ${datasource.system-postgres.password}

  ################### redis 单机版 start ##########################
  redis:
    host: 192.168.20.48
    port: 6379
    password: xshl2023
    timeout: 6000
    database: 8
    lettuce:
      pool:
        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException
        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
      shutdown-timeout: 100ms
################### redis 单机版 end ##########################
#    cluster:
#      nodes: 130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #192.168.3.157:7000,192.168.3.158:7000,192.168.3.159:7000,192.168.3.157:7001,192.168.3.158:7001,192.168.3.159:7001
#    timeout: 1000 # 连接超时时间（毫秒）
#    lettuce:
#      pool:
#        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
#        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
#        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException
#        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
#      shutdown-timeout: 100ms

mybatis-plus:
  # 不支持多包, 如有需要可在注解配置 或 提升扫包等级
  # 例如 com.**.**.mapper
  mapperPackage: com.xshl.bsp.**.mapper
  # 对应的 XML 文件位置
  mapperLocations: classpath*:mappers/**/*Mapper.xml
  # 实体扫描，多个package用逗号或者分号分隔
  typeAliasesPackage: com.xshl.bsp.**.domain
  global-config:
    dbConfig:
      # 主键类型
      # AUTO 自增 NONE 空 INPUT 用户输入 ASSIGN_ID 雪花 ASSIGN_UUID 唯一 UUID
      # 如需改为自增 需要将数据库表全部设置为自增
      idType: ASSIGN_ID

logging:
  level:
    io.swagger.models.parameters.AbstractSerializableParameter: info #忽略swagger中的错误信息
    com.xshl.bsp.user.dao: info

#spring-security配置
# security:
#   oauth2:
#     ignored: /users-anon/**, /doc.html, /document.html, /users/save
#     token:
#       store:
#         type: redis

#设置最大超时时间
ribbon:  
  ServerListRefreshInterval: 10  #刷新服务列表源的间隔时间
  OkToRetryOnAllOperations: true
  MaxAutoRetries: 1
  MaxAutoRetriesNextServer: 1
  ReadTimeout: 16000  
  ConnectTimeout: 16000 


gdzw:
  tokenUrl: a

environment: dev

sa-token:
  #忽略的路径
  pathIgnores: /code/**, /auth/**, /external/auth/**, /sso/*
  # 开启内网服务调用鉴权(不允许越过gateway访问内网服务 保障服务安全)
  #check-same-token: true
  # token 有效期（单位：秒） 默认30天，-1 代表永久有效
  timeout: 1800
  # token 最低活跃频率（单位：秒），如果 token 超过此时间没有访问系统就会被冻结，默认-1 代表不限制，永不冻结
  #active-timeout: -1
  # 是否允许同一账号多地同时登录 （为 true 时允许一起登录, 为 false 时新登录挤掉旧登录）
  #is-concurrent: true
  # 在多人登录同一账号时，是否共用一个 token （为 true 时所有登录共用一个 token, 为 false 时每次登录新建一个 token）
  #is-share: true
  # token 风格（默认可取值：uuid、simple-uuid、random-32、random-64、random-128、tik）
  #token-style: uuid
  # 是否输出操作日志
  #is-log: true
  check-same-token: true


  # 安全配置
security:
  # 验证码
  captcha:
    # 是否开启验证码
    enabled: true
    # 验证码类型 math 数组计算 char 字符验证
    type: MATH
    # line 线段干扰 circle 圆圈干扰 shear 扭曲干扰
    category: CIRCLE
    # 数字验证码位数
    numberLength: 1
    # 字符验证码长度
    charLength: 4

# 用户配置
user:
  password:
    # 密码最大错误次数
    maxRetryCount: 15
    # 密码锁定时间（默认10分钟）
    lockTime: 10

justauth:
  enabled: true
  # 前端外网访问地址
  address: http://localhost:80
  type:
    #pai平台对接
    pai:
      server-url: http://114.255.170.237:8086/pai
      client-id: policy_manage_test
      client-secret: fk9lr3710u7iklxzqy6bsakbyi7x36e6
      redirect-uri: http://localhost
      sso-context-path: /pai-sso
      api-context-path: /pai-api
      token-url: /login/token
      user-info: /v1/sdk/user
      user-info-list: /v1/sdk/user/list/all
      org-tree-url: /v1/sdk/org/tree
      log-out-url: /login/logout
    tz-province:
      server-url: https://tzsyslpt.zwfw.taizhou.gov.cn/tzs-tyrz
      client-id: tzsjj-yqlb
      client-secret: 4P7ByloTY474
      redirect-uri: http://localhost
      token-url: /ticket/token
      user-info: /token/user
      log-out-url: 

logback:
  log:
    level: info
    path: /home/xshl/logs/auth

license:
  subject: license
  publicAlias: publicCert
  storePass: public_Xshl2024
  licensePath: /home/license.lic
  publicKeysStorePath: /home/publicCerts.keystore ', '6e3de8ad739a0a7825ef2ac20596f470', '2010-05-05 00:00:00', '2024-10-21 09:39:49.117', 'nacos', '192.168.10.2', 'U         ', '876aed9e-d385-4cb1-9b39-63a28eaf0737', '');
INSERT INTO "his_config_info" VALUES (0, 24, 'common.yaml', 'DEFAULT_GROUP', '', 'spring:
  cloud:
    nacos:
      discovery:
        server-addr: 192.168.20.48:8848
        namespace: 876aed9e-d385-4cb1-9b39-63a28eaf0737  #命名空间 代指某个环境
  sentinel:
    transport:
      # 指定sentinel 控制台的地址
      dashboard: 192.168.20.94:8080
    eager: true
  jackson:
    mapper:
      ALLOW_EXPLICIT_PROPERTY_RENAMING: true
    deserialization:
      READ_DATE_TIMESTAMPS_AS_NANOSECONDS: false
    serialization:
      WRITE_DATE_TIMESTAMPS_AS_NANOSECONDS: false
      WRITE_DATES_AS_TIMESTAMPS: true
# api接口加密
api-decrypt:
  # 是否开启全局接口加密
  enabled: false
  # AES 加密头标识
  headerFlag: encrypt-key
  # 响应加密公钥 非对称算法的公私钥 如：SM2，RSA 使用者请自行更换
  # 对应前端解密私钥 MIIBVAIBADANBgkqhkiG9w0BAQEFAASCAT4wggE6AgEAAkEAmc3CuPiGL/LcIIm7zryCEIbl1SPzBkr75E2VMtxegyZ1lYRD+7TZGAPkvIsBcaMs6Nsy0L78n2qh+lIZMpLH8wIDAQABAkEAk82Mhz0tlv6IVCyIcw/s3f0E+WLmtPFyR9/WtV3Y5aaejUkU60JpX4m5xNR2VaqOLTZAYjW8Wy0aXr3zYIhhQQIhAMfqR9oFdYw1J9SsNc+CrhugAvKTi0+BF6VoL6psWhvbAiEAxPPNTmrkmrXwdm/pQQu3UOQmc2vCZ5tiKpW10CgJi8kCIFGkL6utxw93Ncj4exE/gPLvKcT+1Emnoox+O9kRXss5AiAMtYLJDaLEzPrAWcZeeSgSIzbL+ecokmFKSDDcRske6QIgSMkHedwND1olF8vlKsJUGK3BcdtM8w4Xq7BpSBwsloE=
  publicKey: MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAJnNwrj4hi/y3CCJu868ghCG5dUj8wZK++RNlTLcXoMmdZWEQ/u02RgD5LyLAXGjLOjbMtC+/J9qofpSGTKSx/MCAwEAAQ==
  # 请求解密私钥 非对称算法的公私钥 如：SM2，RSA 使用者请自行更换
  # 对应前端加密公钥 MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAKoR8mX0rGKLqzcWmOzbfj64K8ZIgOdHnzkXSOVOZbFu/TJhZ7rFAN+eaGkl3C4buccQd/EjEsj9ir7ijT7h96MCAwEAAQ==
  privateKey: MIIBVAIBADANBgkqhkiG9w0BAQEFAASCAT4wggE6AgEAAkEAqhHyZfSsYourNxaY7Nt+PrgrxkiA50efORdI5U5lsW79MmFnusUA355oaSXcLhu5xxB38SMSyP2KvuKNPuH3owIDAQABAkAfoiLyL+Z4lf4Myxk6xUDgLaWGximj20CUf+5BKKnlrK+Ed8gAkM0HqoTt2UZwA5E2MzS4EI2gjfQhz5X28uqxAiEA3wNFxfrCZlSZHb0gn2zDpWowcSxQAgiCstxGUoOqlW8CIQDDOerGKH5OmCJ4Z21v+F25WaHYPxCFMvwxpcw99EcvDQIgIdhDTIqD2jfYjPTY8Jj3EDGPbH2HHuffvflECt3Ek60CIQCFRlCkHpi7hthhYhovyloRYsM+IS9h/0BzlEAuO0ktMQIgSPT3aFAgJYwKpqRYKlLDVcflZFCKY7u3UP8iWi1Qw0Y=

sa-token:
  #jwt秘钥
  jwt-secret-key: abcdefghijklmnopqrstuvwxyz
  # token 名称（同时也是 cookie 名称）
  token-name: Authorization
  #如果是单体服务，这里设置为false，这个是校验服务访问是否从网关进入
  check-same-token: true
  autoRenew: true
  timeout: 1800', '650afdb60258cebd5316c3cacc25c1e7', '2010-05-05 00:00:00', '2024-10-25 11:18:46.423', NULL, '192.168.10.171', 'I         ', 'da36facd-d730-409b-ba05-f6f57a5f1edc', '');
INSERT INTO "his_config_info" VALUES (0, 25, 'gateway.yaml', 'DEFAULT_GROUP', '', 'server:
  port: 9200 #端口
   
spring:
  cloud:
    gateway:
      requestLog: true
      discovery:
        locator:
          lowerCaseServiceId: true
          enabled: true
      routes:
       - id: api-user
         uri: lb://user-center
         order: 8001
         predicates:
         - Path=/api-user/**   
         filters:
         - StripPrefix=1 
       - id: api-auth
         uri: lb://auth
         order: 8002
         predicates:
         - Path=/api-auth/**
         filters:
         - PreserveHostHeader
         - StripPrefix=1  
       - id: api-file
         uri: lb://file
         order: 8003
         predicates:
         - Path=/api-file/**    
       - id: api-system
         uri: lb://system
         order: 8008
         predicates:
         - Path=/api-system/**
         filters:
         - StripPrefix=1 
  datasource: 
    dynamic:
      # 设置默认的数据源或者数据源组,默认值即为 master
      primary: master
      datasource:
        # 主库数据源
        master:
          type: com.zaxxer.hikari.HikariDataSource
          driver-class-name: org.postgresql.Driver
          url: jdbc:postgresql://192.168.20.48:5432/bsp-user?useUnicode=true&characterEncoding=utf8&useSSL=true&autoReconnect=true&reWriteBatchedInserts=true
          username: root
          password: 123456              

################### mysq end ##########################
  redis:
################### redis 单机版 start ########################## 
    host: 192.168.20.48
    port: 6379
    password: xshl2023
    timeout: 6000
    database: 8
    lettuce:
      pool:
        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException  
        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
      shutdown-timeout: 100ms
################### redis 单机版 end ##########################   
#    cluster:
#      nodes: 130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #192.168.3.157:7000,192.168.3.158:7000,192.168.3.159:7000,192.168.3.157:7001,192.168.3.158:7001,192.168.3.159:7001
#    timeout: 1000 # 连接超时时间（毫秒）
#    lettuce:
#      pool:
#        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
#        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
#        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException  
#        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
#      shutdown-timeout: 100ms
  
mybatis-plus:
  # 不支持多包, 如有需要可在注解配置 或 提升扫包等级
  # 例如 com.**.**.mapper
  mapperPackage: com.xshl.bsp.**.mapper
  # 对应的 XML 文件位置
  mapperLocations: classpath*:mappers/**/*Mapper.xml
  # 实体扫描，多个package用逗号或者分号分隔
  typeAliasesPackage: com.xshl.bsp.**.domain
  global-config:
    dbConfig:
      # 主键类型
      # AUTO 自增 NONE 空 INPUT 用户输入 ASSIGN_ID 雪花 ASSIGN_UUID 唯一 UUID
      # 如需改为自增 需要将数据库表全部设置为自增
      idType: ASSIGN_ID


sa-token:
  #忽略的路径
  pathIgnores: /code/**, /auth/**, /test/**, /external/auth/getUserInfo, /external/embed/detail/**, /home/page/**, /matter/info/export, /sys/carousel/list, /entrepreneur/theory/list
  jwt-secret-key: abcdefghijklmnopqrstuvwxyz
  # 开启内网服务调用鉴权(不允许越过gateway访问内网服务 保障服务安全)
  #check-same-token: true
  # token 有效期（单位：秒） 默认30天，-1 代表永久有效
  timeout: 86400
  # token 最低活跃频率（单位：秒），如果 token 超过此时间没有访问系统就会被冻结，默认-1 代表不限制，永不冻结
  #active-timeout: -1
  # 是否允许同一账号多地同时登录 （为 true 时允许一起登录, 为 false 时新登录挤掉旧登录）
  #is-concurrent: true
  # 在多人登录同一账号时，是否共用一个 token （为 true 时所有登录共用一个 token, 为 false 时每次登录新建一个 token）
  #is-share: true
  # token 风格（默认可取值：uuid、simple-uuid、random-32、random-64、random-128、tik）
  #token-style: uuid
  # 是否输出操作日志
  #is-log: true

security:
  # 防止XSS攻击
  xss:
    enabled: true
    excludeUrls:
      - /api-user/notice
      - /flow/**
      - /tqt/api-flow/flow/**
      - /api-flow/flow/**
  # 不校验白名单
  ignore:
    whites: 
      - /api-auth/code
      - /api-auth/auth/**
      - /resource/sms/code
      - /*/v3/api-docs
      - /*/v2/api-docs
      - /*/error
      - /csrf
      - /doc.html
      - /webjars/**
      - /swagger-resources/**
      - /api-system/external/embed/detail/**
      - /api-auth/external/auth/**
      - /api-auth/sso/**
      - /api-system/home/page/**
      - /api-policy/home/page/**
      - /api-file/home/page/**
      - /api-policy/matter/info/export
      - /api-system/external/embed/detail/**
      - /api-quartz/test/**
      - /api-flow/login/**
      - /api-system/sys/carousel/list
      - /api-policy/entrepreneur/theory/list

swagger:
  enable: true
  butler:
    api-docs-path:  /v2/api-docs
    auto-generate-from-scg-routes: true
    ignore-routes:  api-eureka,api-generator,api-baidu

ribbon:
  ReadTimeout: 90000
  ConnectTimeout: 90000
  MaxAutoRetries: 0
  MaxAutoRetriesNextServer: 1
  OkToRetryOnAllOperations: false

feign:
  sentinel:
    enabled: true  #为feign整合sentinel

corsUrls: "*"', '548b501948c3a5a27412b85995157790', '2010-05-05 00:00:00', '2024-10-25 11:18:46.423', NULL, '192.168.10.171', 'I         ', 'da36facd-d730-409b-ba05-f6f57a5f1edc', '');
INSERT INTO "his_config_info" VALUES (0, 26, 'user-center.yaml', 'DEFAULT_GROUP', '', '#端口配置
server:
  port: 8100   #固定端口
  forward-headers-strategy: none  #
  
spring:
  datasource: 
    dynamic:
      # 设置默认的数据源或者数据源组,默认值即为 master
      primary: master
      datasource:
        # 主库数据源
        master:
          type: com.zaxxer.hikari.HikariDataSource
          driver-class-name: org.postgresql.Driver
          url: jdbc:postgresql://192.168.20.48:5432/bsp-user?useUnicode=true&characterEncoding=utf8&useSSL=true&autoReconnect=true&reWriteBatchedInserts=true
          username: root
          password: 123456

  ################### redis 单机版 start ##########################
  redis:
    host: 192.168.20.48
    port: 6379
    password: xshl2023
    timeout: 6000
    database: 8
    lettuce:
      pool:
        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException
        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
      shutdown-timeout: 100ms
################### redis 单机版 end ##########################
#    cluster:
#      nodes: 130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #192.168.3.157:7000,192.168.3.158:7000,192.168.3.159:7000,192.168.3.157:7001,192.168.3.158:7001,192.168.3.159:7001
#    timeout: 1000 # 连接超时时间（毫秒）
#    lettuce:
#      pool:
#        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
#        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
#        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException
#        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
#      shutdown-timeout: 100ms

mybatis-plus:
  # 不支持多包, 如有需要可在注解配置 或 提升扫包等级
  # 例如 com.**.**.mapper
  mapperPackage: com.xshl.bsp.**.mapper
  # 对应的 XML 文件位置
  mapperLocations: classpath*:mappers/**/*Mapper.xml
  # 实体扫描，多个package用逗号或者分号分隔
  typeAliasesPackage: com.xshl.bsp.**.domain
  global-config:
    dbConfig:
      # 主键类型
      # AUTO 自增 NONE 空 INPUT 用户输入 ASSIGN_ID 雪花 ASSIGN_UUID 唯一 UUID
      # 如需改为自增 需要将数据库表全部设置为自增
      idType: ASSIGN_ID

logging:
  level:
    io.swagger.models.parameters.AbstractSerializableParameter: info #忽略swagger中的错误信息
    com.xshl.bsp: info
#配置日志输出
logback:
  log:
    level: INFO
    path: /home/xshl/logs/user-center


#设置最大超时时间
ribbon:  
  ServerListRefreshInterval: 10  #刷新服务列表源的间隔时间
  OkToRetryOnAllOperations: true
  MaxAutoRetries: 1
  MaxAutoRetriesNextServer: 1
  ReadTimeout: 16000  
  ConnectTimeout: 16000 

gdzw:
  tokenUrl: a

environment: dev

sa-token:
  #忽略的路径
  pathIgnores: /user/**, dept/**
  # token 有效期（单位：秒） 默认30天，-1 代表永久有效
  #timeout: 2592000
  # token 最低活跃频率（单位：秒），如果 token 超过此时间没有访问系统就会被冻结，默认-1 代表不限制，永不冻结
  #active-timeout: -1
  # 是否允许同一账号多地同时登录 （为 true 时允许一起登录, 为 false 时新登录挤掉旧登录）
  #is-concurrent: true
  # 在多人登录同一账号时，是否共用一个 token （为 true 时所有登录共用一个 token, 为 false 时每次登录新建一个 token）
  #is-share: true
  # token 风格（默认可取值：uuid、simple-uuid、random-32、random-64、random-128、tik）
  #token-style: uuid
  # 是否输出操作日志
  #is-log: true

flow:
  companyId: b482a6393faefd53783f9d093cd4ddff
  sync: true
 ', '2726e107b651bcbd6a90cc406f976178', '2010-05-05 00:00:00', '2024-10-25 11:18:46.423', NULL, '192.168.10.171', 'I         ', 'da36facd-d730-409b-ba05-f6f57a5f1edc', '');
INSERT INTO "his_config_info" VALUES (0, 27, 'auth.yaml', 'DEFAULT_GROUP', '', '#端口配置
server:
  port: 8000   #固定端口
  forward-headers-strategy: none  #客户端请求头获取策略

spring:
  datasource: 
    dynamic:
      # 设置默认的数据源或者数据源组,默认值即为 master
      primary: master
      datasource:
        # 主库数据源
        master:
          type: com.zaxxer.hikari.HikariDataSource
          driver-class-name: org.postgresql.Driver
          url: jdbc:postgresql://192.168.20.48:5432/bsp-user?useUnicode=true&characterEncoding=utf8&useSSL=true&autoReconnect=true&reWriteBatchedInserts=true
          username: root
          password: 123456
#       oracle:
#          type: ${spring.datasource.type}
#          driverClassName: oracle.jdbc.OracleDriver
#          url: ${datasource.system-oracle.url}
#          username: ${datasource.system-oracle.username}
#          password: ${datasource.system-oracle.password}
#        postgres:
#          type: ${spring.datasource.type}
#          driverClassName: org.postgresql.Driver
#          url: ${datasource.system-postgres.url}
#          username: ${datasource.system-postgres.username}
#          password: ${datasource.system-postgres.password}

  ################### redis 单机版 start ##########################
  redis:
    host: 192.168.20.48
    port: 6379
    password: xshl2023
    timeout: 6000
    database: 8
    lettuce:
      pool:
        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException
        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
      shutdown-timeout: 100ms
################### redis 单机版 end ##########################
#    cluster:
#      nodes: 130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #192.168.3.157:7000,192.168.3.158:7000,192.168.3.159:7000,192.168.3.157:7001,192.168.3.158:7001,192.168.3.159:7001
#    timeout: 1000 # 连接超时时间（毫秒）
#    lettuce:
#      pool:
#        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
#        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
#        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException
#        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
#      shutdown-timeout: 100ms
', '3198c595ea4f8c4ddb3ec6423ef4ca72', '2010-05-05 00:00:00', '2024-10-25 11:18:46.423', NULL, '192.168.10.171', 'I         ', 'da36facd-d730-409b-ba05-f6f57a5f1edc', '');
INSERT INTO "his_config_info" VALUES (20, 28, 'common.yaml', 'DEFAULT_GROUP', '', 'spring:
  cloud:
    nacos:
      discovery:
        server-addr: 192.168.20.48:8848
        namespace: 876aed9e-d385-4cb1-9b39-63a28eaf0737  #命名空间 代指某个环境
  sentinel:
    transport:
      # 指定sentinel 控制台的地址
      dashboard: 192.168.20.94:8080
    eager: true
  jackson:
    mapper:
      ALLOW_EXPLICIT_PROPERTY_RENAMING: true
    deserialization:
      READ_DATE_TIMESTAMPS_AS_NANOSECONDS: false
    serialization:
      WRITE_DATE_TIMESTAMPS_AS_NANOSECONDS: false
      WRITE_DATES_AS_TIMESTAMPS: true
# api接口加密
api-decrypt:
  # 是否开启全局接口加密
  enabled: false
  # AES 加密头标识
  headerFlag: encrypt-key
  # 响应加密公钥 非对称算法的公私钥 如：SM2，RSA 使用者请自行更换
  # 对应前端解密私钥 MIIBVAIBADANBgkqhkiG9w0BAQEFAASCAT4wggE6AgEAAkEAmc3CuPiGL/LcIIm7zryCEIbl1SPzBkr75E2VMtxegyZ1lYRD+7TZGAPkvIsBcaMs6Nsy0L78n2qh+lIZMpLH8wIDAQABAkEAk82Mhz0tlv6IVCyIcw/s3f0E+WLmtPFyR9/WtV3Y5aaejUkU60JpX4m5xNR2VaqOLTZAYjW8Wy0aXr3zYIhhQQIhAMfqR9oFdYw1J9SsNc+CrhugAvKTi0+BF6VoL6psWhvbAiEAxPPNTmrkmrXwdm/pQQu3UOQmc2vCZ5tiKpW10CgJi8kCIFGkL6utxw93Ncj4exE/gPLvKcT+1Emnoox+O9kRXss5AiAMtYLJDaLEzPrAWcZeeSgSIzbL+ecokmFKSDDcRske6QIgSMkHedwND1olF8vlKsJUGK3BcdtM8w4Xq7BpSBwsloE=
  publicKey: MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAJnNwrj4hi/y3CCJu868ghCG5dUj8wZK++RNlTLcXoMmdZWEQ/u02RgD5LyLAXGjLOjbMtC+/J9qofpSGTKSx/MCAwEAAQ==
  # 请求解密私钥 非对称算法的公私钥 如：SM2，RSA 使用者请自行更换
  # 对应前端加密公钥 MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAKoR8mX0rGKLqzcWmOzbfj64K8ZIgOdHnzkXSOVOZbFu/TJhZ7rFAN+eaGkl3C4buccQd/EjEsj9ir7ijT7h96MCAwEAAQ==
  privateKey: MIIBVAIBADANBgkqhkiG9w0BAQEFAASCAT4wggE6AgEAAkEAqhHyZfSsYourNxaY7Nt+PrgrxkiA50efORdI5U5lsW79MmFnusUA355oaSXcLhu5xxB38SMSyP2KvuKNPuH3owIDAQABAkAfoiLyL+Z4lf4Myxk6xUDgLaWGximj20CUf+5BKKnlrK+Ed8gAkM0HqoTt2UZwA5E2MzS4EI2gjfQhz5X28uqxAiEA3wNFxfrCZlSZHb0gn2zDpWowcSxQAgiCstxGUoOqlW8CIQDDOerGKH5OmCJ4Z21v+F25WaHYPxCFMvwxpcw99EcvDQIgIdhDTIqD2jfYjPTY8Jj3EDGPbH2HHuffvflECt3Ek60CIQCFRlCkHpi7hthhYhovyloRYsM+IS9h/0BzlEAuO0ktMQIgSPT3aFAgJYwKpqRYKlLDVcflZFCKY7u3UP8iWi1Qw0Y=

sa-token:
  #jwt秘钥
  jwt-secret-key: abcdefghijklmnopqrstuvwxyz
  # token 名称（同时也是 cookie 名称）
  token-name: Authorization
  #如果是单体服务，这里设置为false，这个是校验服务访问是否从网关进入
  check-same-token: true
  autoRenew: true
  timeout: 1800', '650afdb60258cebd5316c3cacc25c1e7', '2010-05-05 00:00:00', '2024-10-25 11:19:34.234', 'nacos', '192.168.10.171', 'U         ', 'da36facd-d730-409b-ba05-f6f57a5f1edc', '');
INSERT INTO "his_config_info" VALUES (21, 29, 'gateway.yaml', 'DEFAULT_GROUP', '', 'server:
  port: 9200 #端口
   
spring:
  cloud:
    gateway:
      requestLog: true
      discovery:
        locator:
          lowerCaseServiceId: true
          enabled: true
      routes:
       - id: api-user
         uri: lb://user-center
         order: 8001
         predicates:
         - Path=/api-user/**   
         filters:
         - StripPrefix=1 
       - id: api-auth
         uri: lb://auth
         order: 8002
         predicates:
         - Path=/api-auth/**
         filters:
         - PreserveHostHeader
         - StripPrefix=1  
       - id: api-file
         uri: lb://file
         order: 8003
         predicates:
         - Path=/api-file/**    
       - id: api-system
         uri: lb://system
         order: 8008
         predicates:
         - Path=/api-system/**
         filters:
         - StripPrefix=1 
  datasource: 
    dynamic:
      # 设置默认的数据源或者数据源组,默认值即为 master
      primary: master
      datasource:
        # 主库数据源
        master:
          type: com.zaxxer.hikari.HikariDataSource
          driver-class-name: org.postgresql.Driver
          url: jdbc:postgresql://192.168.20.48:5432/bsp-user?useUnicode=true&characterEncoding=utf8&useSSL=true&autoReconnect=true&reWriteBatchedInserts=true
          username: root
          password: 123456              

################### mysq end ##########################
  redis:
################### redis 单机版 start ########################## 
    host: 192.168.20.48
    port: 6379
    password: xshl2023
    timeout: 6000
    database: 8
    lettuce:
      pool:
        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException  
        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
      shutdown-timeout: 100ms
################### redis 单机版 end ##########################   
#    cluster:
#      nodes: 130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #192.168.3.157:7000,192.168.3.158:7000,192.168.3.159:7000,192.168.3.157:7001,192.168.3.158:7001,192.168.3.159:7001
#    timeout: 1000 # 连接超时时间（毫秒）
#    lettuce:
#      pool:
#        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
#        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
#        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException  
#        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
#      shutdown-timeout: 100ms
  
mybatis-plus:
  # 不支持多包, 如有需要可在注解配置 或 提升扫包等级
  # 例如 com.**.**.mapper
  mapperPackage: com.xshl.bsp.**.mapper
  # 对应的 XML 文件位置
  mapperLocations: classpath*:mappers/**/*Mapper.xml
  # 实体扫描，多个package用逗号或者分号分隔
  typeAliasesPackage: com.xshl.bsp.**.domain
  global-config:
    dbConfig:
      # 主键类型
      # AUTO 自增 NONE 空 INPUT 用户输入 ASSIGN_ID 雪花 ASSIGN_UUID 唯一 UUID
      # 如需改为自增 需要将数据库表全部设置为自增
      idType: ASSIGN_ID


sa-token:
  #忽略的路径
  pathIgnores: /code/**, /auth/**, /test/**, /external/auth/getUserInfo, /external/embed/detail/**, /home/page/**, /matter/info/export, /sys/carousel/list, /entrepreneur/theory/list
  jwt-secret-key: abcdefghijklmnopqrstuvwxyz
  # 开启内网服务调用鉴权(不允许越过gateway访问内网服务 保障服务安全)
  #check-same-token: true
  # token 有效期（单位：秒） 默认30天，-1 代表永久有效
  timeout: 86400
  # token 最低活跃频率（单位：秒），如果 token 超过此时间没有访问系统就会被冻结，默认-1 代表不限制，永不冻结
  #active-timeout: -1
  # 是否允许同一账号多地同时登录 （为 true 时允许一起登录, 为 false 时新登录挤掉旧登录）
  #is-concurrent: true
  # 在多人登录同一账号时，是否共用一个 token （为 true 时所有登录共用一个 token, 为 false 时每次登录新建一个 token）
  #is-share: true
  # token 风格（默认可取值：uuid、simple-uuid、random-32、random-64、random-128、tik）
  #token-style: uuid
  # 是否输出操作日志
  #is-log: true

security:
  # 防止XSS攻击
  xss:
    enabled: true
    excludeUrls:
      - /api-user/notice
      - /flow/**
      - /tqt/api-flow/flow/**
      - /api-flow/flow/**
  # 不校验白名单
  ignore:
    whites: 
      - /api-auth/code
      - /api-auth/auth/**
      - /resource/sms/code
      - /*/v3/api-docs
      - /*/v2/api-docs
      - /*/error
      - /csrf
      - /doc.html
      - /webjars/**
      - /swagger-resources/**
      - /api-system/external/embed/detail/**
      - /api-auth/external/auth/**
      - /api-auth/sso/**
      - /api-system/home/page/**
      - /api-policy/home/page/**
      - /api-file/home/page/**
      - /api-policy/matter/info/export
      - /api-system/external/embed/detail/**
      - /api-quartz/test/**
      - /api-flow/login/**
      - /api-system/sys/carousel/list
      - /api-policy/entrepreneur/theory/list

swagger:
  enable: true
  butler:
    api-docs-path:  /v2/api-docs
    auto-generate-from-scg-routes: true
    ignore-routes:  api-eureka,api-generator,api-baidu

ribbon:
  ReadTimeout: 90000
  ConnectTimeout: 90000
  MaxAutoRetries: 0
  MaxAutoRetriesNextServer: 1
  OkToRetryOnAllOperations: false

feign:
  sentinel:
    enabled: true  #为feign整合sentinel

corsUrls: "*"', '548b501948c3a5a27412b85995157790', '2010-05-05 00:00:00', '2024-10-25 11:20:32.143', 'nacos', '192.168.10.171', 'U         ', 'da36facd-d730-409b-ba05-f6f57a5f1edc', '');
INSERT INTO "his_config_info" VALUES (23, 30, 'auth.yaml', 'DEFAULT_GROUP', '', '#端口配置
server:
  port: 8000   #固定端口
  forward-headers-strategy: none  #客户端请求头获取策略

spring:
  datasource: 
    dynamic:
      # 设置默认的数据源或者数据源组,默认值即为 master
      primary: master
      datasource:
        # 主库数据源
        master:
          type: com.zaxxer.hikari.HikariDataSource
          driver-class-name: org.postgresql.Driver
          url: jdbc:postgresql://192.168.20.48:5432/bsp-user?useUnicode=true&characterEncoding=utf8&useSSL=true&autoReconnect=true&reWriteBatchedInserts=true
          username: root
          password: 123456
#       oracle:
#          type: ${spring.datasource.type}
#          driverClassName: oracle.jdbc.OracleDriver
#          url: ${datasource.system-oracle.url}
#          username: ${datasource.system-oracle.username}
#          password: ${datasource.system-oracle.password}
#        postgres:
#          type: ${spring.datasource.type}
#          driverClassName: org.postgresql.Driver
#          url: ${datasource.system-postgres.url}
#          username: ${datasource.system-postgres.username}
#          password: ${datasource.system-postgres.password}

  ################### redis 单机版 start ##########################
  redis:
    host: 192.168.20.48
    port: 6379
    password: xshl2023
    timeout: 6000
    database: 8
    lettuce:
      pool:
        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException
        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
      shutdown-timeout: 100ms
################### redis 单机版 end ##########################
#    cluster:
#      nodes: 130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #192.168.3.157:7000,192.168.3.158:7000,192.168.3.159:7000,192.168.3.157:7001,192.168.3.158:7001,192.168.3.159:7001
#    timeout: 1000 # 连接超时时间（毫秒）
#    lettuce:
#      pool:
#        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
#        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
#        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException
#        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
#      shutdown-timeout: 100ms
', '3198c595ea4f8c4ddb3ec6423ef4ca72', '2010-05-05 00:00:00', '2024-10-25 11:21:11.536', 'nacos', '192.168.10.171', 'U         ', 'da36facd-d730-409b-ba05-f6f57a5f1edc', '');
INSERT INTO "his_config_info" VALUES (22, 31, 'user-center.yaml', 'DEFAULT_GROUP', '', '#端口配置
server:
  port: 8100   #固定端口
  forward-headers-strategy: none  #
  
spring:
  datasource: 
    dynamic:
      # 设置默认的数据源或者数据源组,默认值即为 master
      primary: master
      datasource:
        # 主库数据源
        master:
          type: com.zaxxer.hikari.HikariDataSource
          driver-class-name: org.postgresql.Driver
          url: jdbc:postgresql://192.168.20.48:5432/bsp-user?useUnicode=true&characterEncoding=utf8&useSSL=true&autoReconnect=true&reWriteBatchedInserts=true
          username: root
          password: 123456

  ################### redis 单机版 start ##########################
  redis:
    host: 192.168.20.48
    port: 6379
    password: xshl2023
    timeout: 6000
    database: 8
    lettuce:
      pool:
        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException
        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
      shutdown-timeout: 100ms
################### redis 单机版 end ##########################
#    cluster:
#      nodes: 130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #130.75.131.237:7000,130.75.131.238:7000,130.75.131.239:7000,130.75.131.237:7001,130.75.131.238:7001,130.75.131.239:7001
#        #192.168.3.157:7000,192.168.3.158:7000,192.168.3.159:7000,192.168.3.157:7001,192.168.3.158:7001,192.168.3.159:7001
#    timeout: 1000 # 连接超时时间（毫秒）
#    lettuce:
#      pool:
#        max-active: 10 # 连接池最大连接数（使用负值表示没有限制）,如果赋值为-1，则表示不限制；如果pool已经分配了maxActive个jedis实例，则此时pool的状态为exhausted(耗尽)
#        max-idle: 8   # 连接池中的最大空闲连接 ，默认值也是8
#        max-wait: 100 # # 等待可用连接的最大时间，单位毫秒，默认值为-1，表示永不超时。如果超过等待时间，则直接抛出JedisConnectionException
#        min-idle: 2    # 连接池中的最小空闲连接 ，默认值也是0
#      shutdown-timeout: 100ms

mybatis-plus:
  # 不支持多包, 如有需要可在注解配置 或 提升扫包等级
  # 例如 com.**.**.mapper
  mapperPackage: com.xshl.bsp.**.mapper
  # 对应的 XML 文件位置
  mapperLocations: classpath*:mappers/**/*Mapper.xml
  # 实体扫描，多个package用逗号或者分号分隔
  typeAliasesPackage: com.xshl.bsp.**.domain
  global-config:
    dbConfig:
      # 主键类型
      # AUTO 自增 NONE 空 INPUT 用户输入 ASSIGN_ID 雪花 ASSIGN_UUID 唯一 UUID
      # 如需改为自增 需要将数据库表全部设置为自增
      idType: ASSIGN_ID

logging:
  level:
    io.swagger.models.parameters.AbstractSerializableParameter: info #忽略swagger中的错误信息
    com.xshl.bsp: info
#配置日志输出
logback:
  log:
    level: INFO
    path: /home/xshl/logs/user-center


#设置最大超时时间
ribbon:  
  ServerListRefreshInterval: 10  #刷新服务列表源的间隔时间
  OkToRetryOnAllOperations: true
  MaxAutoRetries: 1
  MaxAutoRetriesNextServer: 1
  ReadTimeout: 16000  
  ConnectTimeout: 16000 

gdzw:
  tokenUrl: a

environment: dev

sa-token:
  #忽略的路径
  pathIgnores: /user/**, dept/**
  # token 有效期（单位：秒） 默认30天，-1 代表永久有效
  #timeout: 2592000
  # token 最低活跃频率（单位：秒），如果 token 超过此时间没有访问系统就会被冻结，默认-1 代表不限制，永不冻结
  #active-timeout: -1
  # 是否允许同一账号多地同时登录 （为 true 时允许一起登录, 为 false 时新登录挤掉旧登录）
  #is-concurrent: true
  # 在多人登录同一账号时，是否共用一个 token （为 true 时所有登录共用一个 token, 为 false 时每次登录新建一个 token）
  #is-share: true
  # token 风格（默认可取值：uuid、simple-uuid、random-32、random-64、random-128、tik）
  #token-style: uuid
  # 是否输出操作日志
  #is-log: true

flow:
  companyId: b482a6393faefd53783f9d093cd4ddff
  sync: true
 ', '2726e107b651bcbd6a90cc406f976178', '2010-05-05 00:00:00', '2024-10-25 11:21:40.796', 'nacos', '192.168.10.171', 'U         ', 'da36facd-d730-409b-ba05-f6f57a5f1edc', '');
INSERT INTO "his_config_info" VALUES (20, 32, 'common.yaml', 'DEFAULT_GROUP', '', 'spring:
  cloud:
    nacos:
      discovery:
        server-addr: 172,21,136.27:8848
        namespace: da36facd-d730-409b-ba05-f6f57a5f1edc  #命名空间 代指某个环境
  sentinel:
    transport:
      # 指定sentinel 控制台的地址
      dashboard: 172,21,136.27:8080
    eager: true
  jackson:
    mapper:
      ALLOW_EXPLICIT_PROPERTY_RENAMING: true
    deserialization:
      READ_DATE_TIMESTAMPS_AS_NANOSECONDS: false
    serialization:
      WRITE_DATE_TIMESTAMPS_AS_NANOSECONDS: false
      WRITE_DATES_AS_TIMESTAMPS: true
# api接口加密
api-decrypt:
  # 是否开启全局接口加密
  enabled: false
  # AES 加密头标识
  headerFlag: encrypt-key
  # 响应加密公钥 非对称算法的公私钥 如：SM2，RSA 使用者请自行更换
  # 对应前端解密私钥 MIIBVAIBADANBgkqhkiG9w0BAQEFAASCAT4wggE6AgEAAkEAmc3CuPiGL/LcIIm7zryCEIbl1SPzBkr75E2VMtxegyZ1lYRD+7TZGAPkvIsBcaMs6Nsy0L78n2qh+lIZMpLH8wIDAQABAkEAk82Mhz0tlv6IVCyIcw/s3f0E+WLmtPFyR9/WtV3Y5aaejUkU60JpX4m5xNR2VaqOLTZAYjW8Wy0aXr3zYIhhQQIhAMfqR9oFdYw1J9SsNc+CrhugAvKTi0+BF6VoL6psWhvbAiEAxPPNTmrkmrXwdm/pQQu3UOQmc2vCZ5tiKpW10CgJi8kCIFGkL6utxw93Ncj4exE/gPLvKcT+1Emnoox+O9kRXss5AiAMtYLJDaLEzPrAWcZeeSgSIzbL+ecokmFKSDDcRske6QIgSMkHedwND1olF8vlKsJUGK3BcdtM8w4Xq7BpSBwsloE=
  publicKey: MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAJnNwrj4hi/y3CCJu868ghCG5dUj8wZK++RNlTLcXoMmdZWEQ/u02RgD5LyLAXGjLOjbMtC+/J9qofpSGTKSx/MCAwEAAQ==
  # 请求解密私钥 非对称算法的公私钥 如：SM2，RSA 使用者请自行更换
  # 对应前端加密公钥 MFwwDQYJKoZIhvcNAQEBBQADSwAwSAJBAKoR8mX0rGKLqzcWmOzbfj64K8ZIgOdHnzkXSOVOZbFu/TJhZ7rFAN+eaGkl3C4buccQd/EjEsj9ir7ijT7h96MCAwEAAQ==
  privateKey: MIIBVAIBADANBgkqhkiG9w0BAQEFAASCAT4wggE6AgEAAkEAqhHyZfSsYourNxaY7Nt+PrgrxkiA50efORdI5U5lsW79MmFnusUA355oaSXcLhu5xxB38SMSyP2KvuKNPuH3owIDAQABAkAfoiLyL+Z4lf4Myxk6xUDgLaWGximj20CUf+5BKKnlrK+Ed8gAkM0HqoTt2UZwA5E2MzS4EI2gjfQhz5X28uqxAiEA3wNFxfrCZlSZHb0gn2zDpWowcSxQAgiCstxGUoOqlW8CIQDDOerGKH5OmCJ4Z21v+F25WaHYPxCFMvwxpcw99EcvDQIgIdhDTIqD2jfYjPTY8Jj3EDGPbH2HHuffvflECt3Ek60CIQCFRlCkHpi7hthhYhovyloRYsM+IS9h/0BzlEAuO0ktMQIgSPT3aFAgJYwKpqRYKlLDVcflZFCKY7u3UP8iWi1Qw0Y=

sa-token:
  #jwt秘钥
  jwt-secret-key: abcdefghijklmnopqrstuvwxyz
  # token 名称（同时也是 cookie 名称）
  token-name: Authorization
  #如果是单体服务，这里设置为false，这个是校验服务访问是否从网关进入
  check-same-token: true
  autoRenew: true
  timeout: 1800', 'b9eefdf65676db0ebf05a9fdb55a3b94', '2010-05-05 00:00:00', '2024-10-25 13:56:28.756', 'nacos', '192.168.10.171', 'U         ', 'da36facd-d730-409b-ba05-f6f57a5f1edc', '');
COMMIT;

-- ----------------------------
-- Table structure for permissions
-- ----------------------------
DROP TABLE IF EXISTS "permissions" CASCADE;
CREATE TABLE "permissions" (
  "role" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" NOT NULL,
  "resource" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" NOT NULL,
  "action" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" NOT NULL
)
;

-- ----------------------------
-- Records of permissions
-- ----------------------------
BEGIN;
INSERT INTO "permissions" VALUES ('xshl', '704f0050-72fe-4572-8e7d-40eb1e58aecd:*:*', 'rw');
INSERT INTO "permissions" VALUES ('xshl', '876aed9e-d385-4cb1-9b39-63a28eaf0737:*:*', 'rw');
INSERT INTO "permissions" VALUES ('xshl', '98550eef-f559-4b75-8f5d-b27b73e4146c:*:*', 'rw');
INSERT INTO "permissions" VALUES ('xshl', 'da36facd-d730-409b-ba05-f6f57a5f1edc:*:*', 'rw');
COMMIT;

-- ----------------------------
-- Table structure for roles
-- ----------------------------
DROP TABLE IF EXISTS "roles" CASCADE;
CREATE TABLE "roles" (
  "username" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" NOT NULL,
  "role" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" NOT NULL
)
;

-- ----------------------------
-- Records of roles
-- ----------------------------
BEGIN;
INSERT INTO "roles" VALUES ('nacos', 'ROLE_ADMIN');
INSERT INTO "roles" VALUES ('xshl', 'xshl');
COMMIT;

-- ----------------------------
-- Table structure for tenant_capacity
-- ----------------------------
DROP TABLE IF EXISTS "tenant_capacity" CASCADE;
CREATE TABLE "tenant_capacity" (
  "id" "pg_catalog"."int8" NOT NULL DEFAULT nextval('tenant_capacity_id_seq'::regclass),
  "tenant_id" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" NOT NULL,
  "quota" "pg_catalog"."int4" NOT NULL,
  "usage" "pg_catalog"."int4" NOT NULL,
  "max_size" "pg_catalog"."int4" NOT NULL,
  "max_aggr_count" "pg_catalog"."int4" NOT NULL,
  "max_aggr_size" "pg_catalog"."int4" NOT NULL,
  "max_history_count" "pg_catalog"."int4" NOT NULL,
  "gmt_create" "pg_catalog"."timestamp" NOT NULL,
  "gmt_modified" "pg_catalog"."timestamp" NOT NULL
)
;
COMMENT ON COLUMN "tenant_capacity"."id" IS '主键ID';
COMMENT ON COLUMN "tenant_capacity"."tenant_id" IS 'Tenant ID';
COMMENT ON COLUMN "tenant_capacity"."quota" IS '配额，0表示使用默认值';
COMMENT ON COLUMN "tenant_capacity"."usage" IS '使用量';
COMMENT ON COLUMN "tenant_capacity"."max_size" IS '单个配置大小上限，单位为字节，0表示使用默认值';
COMMENT ON COLUMN "tenant_capacity"."max_aggr_count" IS '聚合子配置最大个数';
COMMENT ON COLUMN "tenant_capacity"."max_aggr_size" IS '单个聚合数据的子配置大小上限，单位为字节，0表示使用默认值';
COMMENT ON COLUMN "tenant_capacity"."max_history_count" IS '最大变更历史数量';
COMMENT ON COLUMN "tenant_capacity"."gmt_create" IS '创建时间';
COMMENT ON COLUMN "tenant_capacity"."gmt_modified" IS '修改时间';
COMMENT ON TABLE "tenant_capacity" IS '租户容量信息表';

-- ----------------------------
-- Records of tenant_capacity
-- ----------------------------
BEGIN;
COMMIT;

-- ----------------------------
-- Table structure for tenant_info
-- ----------------------------
DROP TABLE IF EXISTS "tenant_info" CASCADE;
CREATE TABLE "tenant_info" (
  "id" "pg_catalog"."int8" NOT NULL DEFAULT nextval('tenant_info_id_seq'::regclass),
  "kp" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" NOT NULL,
  "tenant_id" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "tenant_name" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "tenant_desc" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "create_source" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "gmt_create" "pg_catalog"."int8" NOT NULL,
  "gmt_modified" "pg_catalog"."int8" NOT NULL
)
;
COMMENT ON COLUMN "tenant_info"."id" IS 'id';
COMMENT ON COLUMN "tenant_info"."kp" IS 'kp';
COMMENT ON COLUMN "tenant_info"."tenant_id" IS 'tenant_id';
COMMENT ON COLUMN "tenant_info"."tenant_name" IS 'tenant_name';
COMMENT ON COLUMN "tenant_info"."tenant_desc" IS 'tenant_desc';
COMMENT ON COLUMN "tenant_info"."create_source" IS 'create_source';
COMMENT ON COLUMN "tenant_info"."gmt_create" IS '创建时间';
COMMENT ON COLUMN "tenant_info"."gmt_modified" IS '修改时间';
COMMENT ON TABLE "tenant_info" IS 'tenant_info';

-- ----------------------------
-- Records of tenant_info
-- ----------------------------
BEGIN;
INSERT INTO "tenant_info" VALUES (1, '1', '876aed9e-d385-4cb1-9b39-63a28eaf0737', 'base-dev', '本地开发环境', 'nacos', 1729222032928, 1729222032928);
INSERT INTO "tenant_info" VALUES (2, '1', '704f0050-72fe-4572-8e7d-40eb1e58aecd', 'base-test', '公司测试环境', 'nacos', 1729222047295, 1729222047295);
INSERT INTO "tenant_info" VALUES (3, '1', '98550eef-f559-4b75-8f5d-b27b73e4146c', 'base-pre', '预发布环境', 'nacos', 1729222062953, 1729222062953);
INSERT INTO "tenant_info" VALUES (4, '1', 'da36facd-d730-409b-ba05-f6f57a5f1edc', 'base-prd', '生产环境', 'nacos', 1729222073627, 1729222073627);
COMMIT;

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS "users" CASCADE;
CREATE TABLE "users" (
  "username" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" NOT NULL,
  "password" "pg_catalog"."varchar" COLLATE "pg_catalog"."default" NOT NULL,
  "enabled" "pg_catalog"."bool" NOT NULL
)
;

-- ----------------------------
-- Records of users
-- ----------------------------
BEGIN;
INSERT INTO "users" VALUES ('nacos', '$2a$10$EuWPZHzz32dJN7jexM34MOeYirDdFAZm2kuWj7VEOJhhZkDrxfvUu', 't');
INSERT INTO "users" VALUES ('xshl', '$2a$10$rZXXBSLHh5hhky6ZzpxFYufplHLHNZz87LGA5KZLM3BMpPpmDcNfS', 't');
COMMIT;

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "config_info_aggr_id_seq"
OWNED BY "config_info_aggr"."id";
SELECT setval('"config_info_aggr_id_seq"', 2, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "config_info_beta_id_seq"
OWNED BY "config_info_beta"."id";
SELECT setval('"config_info_beta_id_seq"', 2, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "config_info_id_seq"
OWNED BY "config_info"."id";
SELECT setval('"config_info_id_seq"', 29, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "config_info_tag_id_seq"
OWNED BY "config_info_tag"."id";
SELECT setval('"config_info_tag_id_seq"', 2, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "config_tags_relation_id_seq"
OWNED BY "config_tags_relation"."id";
SELECT setval('"config_tags_relation_id_seq"', 2, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "config_tags_relation_nid_seq"
OWNED BY "config_tags_relation"."nid";
SELECT setval('"config_tags_relation_nid_seq"', 2, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "group_capacity_id_seq"
OWNED BY "group_capacity"."id";
SELECT setval('"group_capacity_id_seq"', 2, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "his_config_info_nid_seq"
OWNED BY "his_config_info"."nid";
SELECT setval('"his_config_info_nid_seq"', 33, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "tenant_capacity_id_seq"
OWNED BY "tenant_capacity"."id";
SELECT setval('"tenant_capacity_id_seq"', 2, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "tenant_info_id_seq"
OWNED BY "tenant_info"."id";
SELECT setval('"tenant_info_id_seq"', 5, true);

-- ----------------------------
-- Indexes structure for table config_info
-- ----------------------------
CREATE UNIQUE INDEX "uk_configinfo_datagrouptenant" ON "config_info" USING btree (
  "data_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST,
  "group_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST,
  "tenant_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table config_info
-- ----------------------------
ALTER TABLE "config_info" ADD CONSTRAINT "config_info_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table config_info_aggr
-- ----------------------------
CREATE UNIQUE INDEX "uk_configinfoaggr_datagrouptenantdatum" ON "config_info_aggr" USING btree (
  "data_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST,
  "group_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST,
  "tenant_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST,
  "datum_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table config_info_aggr
-- ----------------------------
ALTER TABLE "config_info_aggr" ADD CONSTRAINT "config_info_aggr_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table config_info_beta
-- ----------------------------
CREATE UNIQUE INDEX "uk_configinfobeta_datagrouptenant" ON "config_info_beta" USING btree (
  "data_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST,
  "group_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST,
  "tenant_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table config_info_beta
-- ----------------------------
ALTER TABLE "config_info_beta" ADD CONSTRAINT "config_info_beta_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table config_info_tag
-- ----------------------------
CREATE UNIQUE INDEX "uk_configinfotag_datagrouptenanttag" ON "config_info_tag" USING btree (
  "data_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST,
  "group_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST,
  "tenant_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST,
  "tag_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table config_info_tag
-- ----------------------------
ALTER TABLE "config_info_tag" ADD CONSTRAINT "config_info_tag_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table config_tags_relation
-- ----------------------------
CREATE INDEX "idx_tenant_id" ON "config_tags_relation" USING btree (
  "tenant_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE UNIQUE INDEX "uk_configtagrelation_configidtag" ON "config_tags_relation" USING btree (
  "id" "pg_catalog"."int8_ops" ASC NULLS LAST,
  "tag_name" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST,
  "tag_type" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table config_tags_relation
-- ----------------------------
ALTER TABLE "config_tags_relation" ADD CONSTRAINT "config_tags_relation_pkey" PRIMARY KEY ("nid");

-- ----------------------------
-- Indexes structure for table group_capacity
-- ----------------------------
CREATE UNIQUE INDEX "uk_group_id" ON "group_capacity" USING btree (
  "group_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table group_capacity
-- ----------------------------
ALTER TABLE "group_capacity" ADD CONSTRAINT "group_capacity_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table his_config_info
-- ----------------------------
CREATE INDEX "idx_did" ON "his_config_info" USING btree (
  "data_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
CREATE INDEX "idx_gmt_create" ON "his_config_info" USING btree (
  "gmt_create" "pg_catalog"."timestamp_ops" ASC NULLS LAST
);
CREATE INDEX "idx_gmt_modified" ON "his_config_info" USING btree (
  "gmt_modified" "pg_catalog"."timestamp_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table his_config_info
-- ----------------------------
ALTER TABLE "his_config_info" ADD CONSTRAINT "his_config_info_pkey" PRIMARY KEY ("nid");

-- ----------------------------
-- Indexes structure for table permissions
-- ----------------------------
CREATE UNIQUE INDEX "uk_role_permission" ON "permissions" USING btree (
  "role" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST,
  "resource" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST,
  "action" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Indexes structure for table roles
-- ----------------------------
CREATE UNIQUE INDEX "uk_username_role" ON "roles" USING btree (
  "username" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST,
  "role" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Indexes structure for table tenant_capacity
-- ----------------------------
CREATE UNIQUE INDEX "uk_tenant_id" ON "tenant_capacity" USING btree (
  "tenant_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table tenant_capacity
-- ----------------------------
ALTER TABLE "tenant_capacity" ADD CONSTRAINT "tenant_capacity_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table tenant_info
-- ----------------------------
CREATE UNIQUE INDEX "uk_tenant_info_kptenantid" ON "tenant_info" USING btree (
  "kp" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST,
  "tenant_id" COLLATE "pg_catalog"."default" "pg_catalog"."text_ops" ASC NULLS LAST
);
