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

 Date: 02/12/2024 11:18:19
*/


-- ----------------------------
-- Table structure for biz_data_type
-- ----------------------------
DROP TABLE IF EXISTS "public"."biz_data_type";
CREATE TABLE "public"."biz_data_type" (
  "id" "pg_catalog"."int8" NOT NULL,
  "name" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "code" "pg_catalog"."varchar" COLLATE "pg_catalog"."default",
  "sort_index" "pg_catalog"."int4",
  "type" "pg_catalog"."int4"
)
;
COMMENT ON COLUMN "public"."biz_data_type"."id" IS '主键';
COMMENT ON COLUMN "public"."biz_data_type"."name" IS '名称';
COMMENT ON COLUMN "public"."biz_data_type"."code" IS '编码';
COMMENT ON COLUMN "public"."biz_data_type"."sort_index" IS '排序值';
COMMENT ON COLUMN "public"."biz_data_type"."type" IS '类型1:业务域 2主题域';
COMMENT ON TABLE "public"."biz_data_type" IS '数据所属分类表';

-- ----------------------------
-- Records of biz_data_type
-- ----------------------------
INSERT INTO "public"."biz_data_type" VALUES (1855180489614303234, '公共服务', '01', NULL, 1);
INSERT INTO "public"."biz_data_type" VALUES (1855183720394399746, '政务办公', '02', NULL, 1);
INSERT INTO "public"."biz_data_type" VALUES (1855657760276037633, '公共安全', '03', NULL, 1);
INSERT INTO "public"."biz_data_type" VALUES (1855657797513068546, '能源环境', '04', NULL, 1);
INSERT INTO "public"."biz_data_type" VALUES (1855657849572769794, '信息产业', '05', NULL, 1);
INSERT INTO "public"."biz_data_type" VALUES (1856520085648334849, '经济发展', '06', NULL, 1);
INSERT INTO "public"."biz_data_type" VALUES (1856520114651947010, '教育文化', '07', NULL, 1);
INSERT INTO "public"."biz_data_type" VALUES (1856520148105715713, '农村农业', '08', NULL, 1);
INSERT INTO "public"."biz_data_type" VALUES (1856520179583967233, '金融服务', '09', NULL, 1);
INSERT INTO "public"."biz_data_type" VALUES (1856520207832604674, '文化娱乐', '10', NULL, 1);
INSERT INTO "public"."biz_data_type" VALUES (1856520240694976513, '社保就业', '11', NULL, 1);
INSERT INTO "public"."biz_data_type" VALUES (1856520267765014529, '医疗卫生', '12', NULL, 1);
INSERT INTO "public"."biz_data_type" VALUES (1856520296160452610, '法律服务', '13', NULL, 1);
INSERT INTO "public"."biz_data_type" VALUES (1856520323821887490, '交通运输', '14', NULL, 1);
INSERT INTO "public"."biz_data_type" VALUES (1856520359850958849, '市场监管', '15', NULL, 1);
INSERT INTO "public"."biz_data_type" VALUES (1856520390091890689, '财税金融', '16', NULL, 1);
INSERT INTO "public"."biz_data_type" VALUES (1856520427131789314, '地理空间', '17', NULL, 1);
INSERT INTO "public"."biz_data_type" VALUES (1856520466889596930, '气象服务', '18', NULL, 1);
INSERT INTO "public"."biz_data_type" VALUES (1856520494471340033, '科技创新', '19', NULL, 1);
INSERT INTO "public"."biz_data_type" VALUES (1856520524917792770, '信用信息', '20', NULL, 1);
INSERT INTO "public"."biz_data_type" VALUES (1855184922087661570, '市场主体登记注册', '01', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1855658020763287554, '市场主体信用监管', '03', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1855658055324352513, '反垄断与反不正当竞争', '04', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1855658083879174146, '价格调控', '05', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1855185047098892289, '消费者权益保护', '02', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538292926779394, '网络交易监督', '06', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538293191020546, '广告监督', '07', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538293224574978, '质量监管', '08', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538293253935106, '食品安全', '09', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538293279100929, '特种设备安全', '10', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538293300072450, '计量标准', '11', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538293325238274, '知识产权', '12', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538293350404098, '认证认可与检验检测', '13', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538293509787650, '民营经济', '14', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538293543342082, '行政审批', '15', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538293564313602, '科技与信息化', '16', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538293627228162, '综合执法稽查', '17', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538293723697153, '经济犯罪', '18', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538293769834498, '治安管理', '19', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538293790806018, '出入境', '20', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538293811777537, '经济文化保护', '21', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538293862109186, '森林资源', '22', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538293887275009, '工程建设', '23', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538293920829442, '公路养护', '24', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538293941800962, '道路运输', '25', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538293971161089, '水路交通', '26', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538293996326914, '审计监管', '27', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538294021492737, '信访管理', '28', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538294067630081, '自然资源开发利用', '29', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538294105378817, '国土空间生态修复', '30', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538294130544642, '地质勘察', '31', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538294151516161, '矿产管理', '32', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538294172487681, '地质灾害防治', '33', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538294197653505, '自然资源确权登记', '34', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538294218625025, '国土空间用途管制', '35', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538294252179457, '国土空间规划', '36', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538294277345282, '耕地保护', '37', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538294306705410, '政策法规', '38', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538294323482625, '住房改革和保障', '39', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538294361231361, '市场监管', '40', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538294390591489, '住房公积金', '41', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538294415757314, '建筑管理', '42', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538294445117441, '城市建设与管理', '43', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538294470283266, '村镇建设', '44', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538294499643394, '景观园林', '45', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538294533197826, '离退休人员管理', '46', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538294558363650, '医政管理', '47', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538294583529474, '应急管理', '48', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538294617083906, '基层医疗卫生', '49', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538294646444033, '科技教育', '50', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538294675804161, '药物政策与药械临床使用监测评价', '51', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538294705164290, '老龄健康', '52', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538294730330114, '妇幼健康', '53', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538294755495937, '职业健康', '54', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538294793244674, '人口监测与家庭发展', '55', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538294818410498, '预防保健', '56', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538294847770626, '医疗保健', '57', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538294881325058, '水文水资源', '58', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538294906490882, '河湖管理保护', '59', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538294931656705, '水土保持', '60', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538294956822530, '农村水利', '61', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538294981988354, '移民管理', '62', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538295011348482, '旱灾害防御', '63', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538295036514306, '气象观测与网络', '64', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538295061680129, '气象科技与预报', '65', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538295086845954, '发展战略与规划', '66', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538295112011777, '经济体制综合改革', '67', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538295132983298, '固定资产投资', '68', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538295166537729, '利用外资和境外投资', '69', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538295191703553, '开发区与总部经济', '70', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538295225257986, '地区经济', '71', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538295258812417, '县域经济发展', '72', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538295288172546, '农村经济', '73', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538295313338370, '基础设施发展', '74', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538295338504193, '产业发展', '75', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538295388835841, '数字经济发展', '76', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538295418195970, '创新与高技术发展', '77', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538295447556098, '社会发展', '78', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538295476916226, '就业收入分配与消费', '79', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538295502082050, '经济贸易', '80', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538295523053570, '财政金融与信用建设', '81', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538295552413697, '重点项目管理', '82', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538295581773825, '民族地区经济', '83', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538295611133954, '营商环境优化', '84', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538295636299778, '粮食和物资储备', '85', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538295665659906, '电力', '86', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538295690825730, '煤炭', '87', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538295707602946, '石油天然气', '88', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538295749545985, '新能源和可再生能源', '89', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538295774711810, '工业要素', '90', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538295795683330, '产业园区', '91', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538295825043458, '技术改造', '92', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538295850209281, '装备工业', '93', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538295887958017, '汽车产业', '94', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538295908929537, '电子信息', '95', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538295938289665, '大数据与信息化', '96', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538295963455489, '软件与信息服务业', '97', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538295992815618, '信息安全与网络发展', '98', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538296026370049, '材料工业', '99', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538296068313089, '医药产业', '100', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538296089284609, '化工产业', '101', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538296110256129, '轻工纺织', '102', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538296139616258, '盐业', '103', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538296160587777, '农产品加工', '104', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538296189947905, '生产性服务业', '105', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538296227696641, '环境和资源综合利用', '106', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538296257056769, '创业促进与服务体系', '107', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538296286416897, '产业金融', '108', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538296319971330, '无线电监督检查', '109', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538296349331458, '无线电频率台站管理', '110', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538296382885889, '对外经济合作', '111', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538296420634626, '基础教育', '112', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538296445800449, '高等教育', '113', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538296500326401, '民族教育', '114', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538296546463745, '职业教育', '115', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538296571629570, '校外教育', '116', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538296605184002, '语言文字与教材', '117', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538296634544129, '教师工作', '118', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538296672292866, '体育卫生与艺术教育', '119', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538296735207425, '科学技术与研究生教育', '120', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538296760373250, '高校学生工作', '121', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538296798121986, '教育考试', '122', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538296823287810, '教育评估', '123', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538296848453633, '学校国有资产与教育装备', '124', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538296873619458, '教育考试命题', '125', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538296898785282, '学生资助', '126', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538296932339714, '学生信息咨询与就业指导', '127', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538297007837186, '教育对外交流', '128', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538297041391618, '招生考试指导', '129', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538297062363138, '科技监督与诚信', '130', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538297100111874, '科技重大专项', '131', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538297125277698, '民族团结促进', '132', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538297146249217, '教育科技与民族语言文字', '133', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538297183997954, '宗教业务', '134', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538297221746690, '汉传佛教道教伊斯兰教', '135', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538297255301122, '天主教基督教', '136', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538297288855553, '藏传佛教', '137', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538297334992897, '社会组织', '138', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538297855086594, '社会救助', '139', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538297888641025, '区划地名', '140', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538297909612546, '社会事务', '141', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538297930584066, '社会福利', '142', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538297955749889, '老龄工作', '143', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538297976721409, '养老服务与事业发展', '144', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538297997692930, '儿童保障', '145', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538298022858754, '慈善事业', '146', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538298048024578, '婚育保障', '147', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538298081579010, '殡葬服务', '148', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538298110939138, '司法鉴定', '149', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538298131910657, '人民调解', '150', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538298157076482, '律师事务', '151', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538298186436610, '基层法律服务', '152', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538298228379650, '公证机构', '153', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538298249351169, '法律援助', '154', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538298282905601, '社区矫正', '155', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538298316460034, '普法与依法治理', '156', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538298350014465, '法律职业资格', '157', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538298387763201, '行政执法协调', '158', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538298417123330, '监狱与戒毒', '159', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538298446483457, '资产评估', '160', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538298471649281, '会计事务', '161', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538298509398017, '采购投诉', '162', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538298542952450, '财政国库支付', '163', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538298576506881, '预算编审', '164', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538298601672705, '收费票据', '165', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538298622644226, '债券发行', '166', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538298681364482, '预算绩效评价', '167', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538298727501825, '国有金融资本运营评价', '168', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538298773639169, '社会保险基金', '169', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538298798804993, '社会保障', '170', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538298874302465, '自然生态保护', '171', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538298899468290, '水生态环境', '172', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538298920439809, '大气环境', '173', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538298945605633, '农村生态环境', '174', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538298995937281, '土壤生态环境', '175', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538299033686018, '固体废物与化学品', '176', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538299054657537, '核设施与辐射源安全', '177', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538299092406273, '生态环境监测', '178', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538299117572097, '种植业与农药肥料', '179', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538299142737921, '畜牧兽医', '180', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538299176292354, '饲料兽药', '181', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538299197263873, '渔业渔政', '182', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538299230818305, '特色产业', '183', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538299255984130, '乡村建设', '184', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538299293732865, '农村社会事业', '185', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538299335675905, '农村合作经济', '186', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538299356647425, '农村宅基地', '187', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538299377618946, '家庭农场', '188', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538299411173378, '农村监测帮扶', '189', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538299440533506, '农村脱贫', '190', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538299541196801, '农产品质量与品牌培育', '191', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538299566362626, '农村种业', '192', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538299608305665, '农业机械', '193', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538299637665793, '农田建设', '194', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538299662831618, '农业资源环境', '195', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538299683803138, '服务贸易与商贸服务业', '196', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538299708968961, '贸易经济', '197', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538299734134786, '国际交流合作', '198', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538299763494914, '资源再利用流通', '199', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538299788660737, '对外经济贸易', '200', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538299813826561, '法规与贸易救济', '201', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538299830603777, '艺术文化', '202', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538299855769602, '非物质文化遗产', '203', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538299880935426, '宣传推广', '204', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538299914489857, '退役军人拥军优抚', '205', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538299943849985, '退役军人就业创业', '206', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538299973210113, '退役军人褒奖纪念', '207', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538299998375937, '退役军人权益维护', '208', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538300019347457, '综合减灾', '209', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538300052901889, '救援协调', '210', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538300086456321, '火灾防治', '211', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538300107427841, '水旱灾害', '212', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538300124205058, '地震与地质灾害', '213', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538300166148097, '危险化学品', '214', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538300182925313, '非煤矿山', '215', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538300220674050, '煤炭管理', '216', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538300241645569, '煤矿管理', '217', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538300271005697, '救灾与物资', '218', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538300308754434, '群众体育', '219', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538300329725954, '竞技体育', '220', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538300384251905, '青少年体育', '221', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538300409417729, '体育产业', '222', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538300434583553, '体育经济', '223', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538300463943682, '核算统计', '224', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538300493303809, '人员就业', '225', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538300518469634, '野生动植物与湿地', '226', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538300539441153, '自然保护地', '227', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538300593967106, '栖息地', '228', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538300623327234, '草原', '229', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538300652687361, '国有林场与种苗', '230', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538300677853186, '传媒机构', '231', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538300703019009, '网络视听节目', '232', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538300728184833, '安全传输', '233', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538300749156354, '媒体融合', '234', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538300786905090, '电视剧', '235', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538300862402561, '待遇保障', '236', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538300883374081, '医药服务', '237', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538300929511426, '医药价格与招标采购', '238', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538300963065857, '基金监管', '239', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538301101477890, '地质矿产', '240', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538301139226625, '地质灾害', '241', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538301164392450, '生态地质环境', '242', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538301189558273, '核地质与核应急', '243', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538301227307009, '国有资产', '244', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538301269250050, '中医药', '245', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538301298610178, '文物保护', '246', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538301332164609, '博物馆', '247', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538301386690562, '革命文物', '248', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538301432827906, '药品注册', '249', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538301453799426, '药品生产', '250', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538301487353857, '药品流通', '251', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538301558657025, '医疗器械', '252', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538301583822849, '化妆品', '253', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538301613182977, '教育矫治', '254', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538301650931713, '医疗康复', '255', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538301680291842, '货物和劳务', '256', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538301713846273, '企业所得', '257', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538301747400705, '个人所得', '258', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538301772566529, '财产与行为', '259', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538301806120961, '资源和环境', '260', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538301835481090, '社会保险', '261', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538301873229826, '纳税服务', '262', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538301898395650, '征管和科技发展', '263', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538301923561474, '国际税收', '264', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538301994864642, '普遍服务', '265', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538302498181122, '监测预报', '266', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538302644981761, '震害防御', '267', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538302670147585, '纪检监察审计', '268', NULL, 2);
INSERT INTO "public"."biz_data_type" VALUES (1856538302695313410, '减灾救助', '269', NULL, 2);

-- ----------------------------
-- Primary Key structure for table biz_data_type
-- ----------------------------
ALTER TABLE "public"."biz_data_type" ADD CONSTRAINT "biz_data_type_pkey" PRIMARY KEY ("id");
